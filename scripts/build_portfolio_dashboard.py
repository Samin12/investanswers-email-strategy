#!/usr/bin/env python3
"""Build the public InvestAnswers/Alpaca portfolio dashboard from real local data.

Inputs are the sanitized portfolio-manager snapshots and durable markdown logs.
No credentials or account IDs are read or written. Output is a static here.now-ready
site under public/.
"""
from __future__ import annotations

import html
import json
import re
import subprocess
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state" / "portfolio_manager"
PUBLIC = ROOT / "public"
CHECK_LOG = ROOT / "analysis" / "check-log.md"
TRADE_JOURNAL = ROOT / "analysis" / "trade-journal.md"
LATEST_URL = ROOT / "state" / "portfolio_manager" / "dashboard_latest_url.txt"


def dec(value, default="0") -> Decimal:
    try:
        if value is None or value == "":
            return Decimal(default)
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return Decimal(default)


def money(value) -> str:
    return f"${float(dec(value)):,.2f}"


def pct(value) -> str:
    return f"{float(dec(value) * Decimal('100')):,.2f}%"


def load_json(path: Path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def parse_ts(raw: str) -> datetime | None:
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw)
    except ValueError:
        pass
    # snapshot_20260612_141931_EDT_manual.json
    m = re.search(r"snapshot_(\d{8})_(\d{6})", raw)
    if m:
        return datetime.strptime("".join(m.groups()), "%Y%m%d%H%M%S")
    return None


def load_alpaca_portfolio_history(period: str = "6M", timeframe: str = "1D") -> dict:
    """Return sanitized multi-month Alpaca portfolio history for the public chart.

    Uses the Alpaca CLI paper profile and stores only timestamp/equity/P&L series.
    If Alpaca is unavailable, the dashboard falls back to local snapshots.
    """
    try:
        proc = subprocess.run(
            [
                "alpaca",
                "--profile",
                "paper",
                "account",
                "portfolio",
                "--period",
                period,
                "--timeframe",
                timeframe,
                "--jq",
                ".",
            ],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            timeout=90,
            check=True,
        )
        raw = json.loads(proc.stdout)
    except Exception as exc:
        return {"ok": False, "error": type(exc).__name__, "period": period, "timeframe": timeframe, "points": []}

    timestamps = raw.get("timestamp") or []
    equities = raw.get("equity") or []
    profit_loss = raw.get("profit_loss") or []
    profit_loss_pct = raw.get("profit_loss_pct") or []
    points: list[dict] = []
    for i, ts_raw in enumerate(timestamps):
        equity = dec(equities[i] if i < len(equities) else None)
        # Alpaca returns zero rows for days before the paper account was funded.
        # Hide those so the chart is a real multi-month performance curve, not a fake zero baseline.
        if equity <= 0:
            continue
        try:
            ts = datetime.fromtimestamp(int(ts_raw), tz=timezone.utc).astimezone()
        except Exception:
            continue
        points.append(
            {
                "timestamp": ts.isoformat(timespec="seconds"),
                "timestamp_short": ts.strftime("%b %-d"),
                "equity": float(equity),
                "profit_loss": float(dec(profit_loss[i] if i < len(profit_loss) else None)),
                "profit_loss_pct": float(dec(profit_loss_pct[i] if i < len(profit_loss_pct) else None)),
            }
        )
    return {
        "ok": bool(points),
        "period": period,
        "timeframe": timeframe,
        "base_value": raw.get("base_value"),
        "base_value_asof": raw.get("base_value_asof"),
        "points": points,
    }


def load_snapshots() -> list[dict]:
    snapshots = []
    for path in sorted(STATE.glob("snapshot_*.json")):
        data = load_json(path)
        if not isinstance(data, dict):
            continue
        ts = parse_ts(data.get("timestamp_et") or path.name)
        acct = data.get("account") or {}
        positions = data.get("positions") or []
        equity = dec(acct.get("equity") or acct.get("portfolio_value"))
        cash = dec(acct.get("cash"))
        long_mv = sum(dec(p.get("market_value")) for p in positions if isinstance(p, dict))
        snapshots.append({
            "timestamp": data.get("timestamp_et") or path.name,
            "timestamp_short": ts.strftime("%b %-d %H:%M") if ts else data.get("timestamp_et", path.name),
            "sort_key": ts.isoformat() if ts else path.name,
            "check_type": data.get("check_type"),
            "equity": float(equity),
            "cash": float(cash),
            "long_market_value": float(long_mv),
            "position_count": len(positions),
            "new_email_count": data.get("new_email_count_estimate", 0),
            "path": path.name,
        })
    snapshots.sort(key=lambda x: x["sort_key"])
    # Deduplicate same timestamp/path edge cases.
    unique = []
    seen = set()
    for row in snapshots:
        key = (row["timestamp"], row["check_type"], row["equity"], row["cash"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(row)
    return unique


def parse_markdown_table(path: Path) -> list[dict]:
    if not path.exists():
        return []
    lines = path.read_text().splitlines()
    table_lines = [line for line in lines if line.startswith("|") and not re.match(r"^\|[-:| ]+\|$", line)]
    if not table_lines:
        return []
    header = [h.strip() for h in table_lines[0].strip("|").split("|")]
    rows = []
    for line in table_lines[1:]:
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < len(header):
            cells += [""] * (len(header) - len(cells))
        row = dict(zip(header, cells))
        # Drop markdown separator accidentally included or empty rows.
        if row.get(header[0], "").startswith("---"):
            continue
        rows.append(row)
    return rows


def clean_md(text: str) -> str:
    text = text or ""
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = text.replace("**", "").replace("—", "-")
    return text


def summarize_reasons(latest: dict, trades: list[dict], checks: list[dict]) -> list[str]:
    reasons: list[str] = []
    acct = latest.get("account") or {}
    positions = latest.get("positions") or []
    equity = dec(acct.get("equity") or acct.get("portfolio_value"))
    cash = dec(acct.get("cash"))
    if equity:
        cash_pct = cash / equity
        if cash_pct >= Decimal("0.095"):
            reasons.append(f"Cash buffer restored to {float(cash_pct * 100):.1f}% after the latest ALAB trim.")
        else:
            reasons.append(f"Cash is only {float(cash_pct * 100):.1f}%, below the 10% target, so new adds need extra discipline.")
        biggest = max((p for p in positions if isinstance(p, dict)), key=lambda p: dec(p.get("market_value")), default=None)
        if biggest:
            weight = dec(biggest.get("market_value")) / equity
            reasons.append(f"Largest position is {biggest.get('symbol')} at {float(weight * 100):.1f}%, so concentration is still the main rebalance risk.")
    if trades:
        last = trades[-1]
        action = clean_md(last.get("action", ""))
        asset = clean_md(last.get("asset", ""))
        outcome = clean_md(last.get("outcome", ""))
        reasons.append(f"Latest journal decision: {action} on {asset}. {outcome[:150]}")
    elif checks:
        last = checks[-1]
        reasons.append(f"Latest check: {clean_md(last.get('action_taken', 'watch'))}.")
    return reasons[:3]


def build_data() -> dict:
    latest = load_json(STATE / "latest_snapshot.json") or {}
    snapshots = load_snapshots()
    portfolio_history = load_alpaca_portfolio_history()
    history_points = portfolio_history.get("points") or []
    if not history_points:
        history_points = snapshots
    checks = parse_markdown_table(CHECK_LOG)
    trades = parse_markdown_table(TRADE_JOURNAL)
    acct = latest.get("account") or {}
    positions = latest.get("positions") or []
    equity = dec(acct.get("equity") or acct.get("portfolio_value"))
    invested_base = dec(portfolio_history.get("base_value") if isinstance(portfolio_history, dict) else None)
    if invested_base <= 0 and history_points:
        invested_base = dec(history_points[0].get("equity"))
    overall_gain = equity - invested_base if invested_base > 0 else Decimal("0")
    overall_gain_pct = (overall_gain / invested_base) if invested_base > 0 else Decimal("0")
    enriched_positions = []
    for p in positions:
        if not isinstance(p, dict):
            continue
        mv = dec(p.get("market_value"))
        cost = dec(p.get("cost_basis"))
        weight = (mv / equity) if equity else Decimal("0")
        enriched_positions.append({
            "symbol": p.get("symbol"),
            "qty": float(dec(p.get("qty"))),
            "current_price": float(dec(p.get("current_price"))),
            "avg_entry_price": float(dec(p.get("avg_entry_price"))),
            "market_value": float(mv),
            "cost_basis": float(cost),
            "weight": float(weight),
            "unrealized_pl": float(dec(p.get("unrealized_pl"))),
            "unrealized_plpc": float(dec(p.get("unrealized_plpc"))),
            "change_today": float(dec(p.get("change_today"))),
        })
    enriched_positions.sort(key=lambda p: p["market_value"], reverse=True)

    prices = latest.get("prices") or {}
    watch = []
    watch_levels = {
        "SPCX": "Buy zone $140 -> $135 retest; no day-1 chase.",
        "TSLA": "Interested under $400, better $380-$395 with confirmation.",
        "SATS": "Only interesting near <$100.",
        "PLTR": "~$130 box zone, but size/cash rules still matter.",
        "NVDA": "Below $200 is preferred entry zone.",
        "AVGO": "$350-$378 support zone; above zone = wait.",
    }
    for sym, note in watch_levels.items():
        price = None
        raw = prices.get(sym)
        if isinstance(raw, dict):
            price = raw.get("price")
        watch.append({"symbol": sym, "price": price, "rule": note})

    return {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "source": "Alpaca paper profile + InvestAnswers strategy repo logs",
        "latest_url": LATEST_URL.read_text().strip() if LATEST_URL.exists() else "",
        "account": {
            "equity": float(equity),
            "cash": float(dec(acct.get("cash"))),
            "buying_power": float(dec(acct.get("buying_power"))),
            "long_market_value": float(dec(acct.get("long_market_value"))),
            "options_buying_power": float(dec(acct.get("options_buying_power"))),
            "timestamp_et": latest.get("timestamp_et"),
            "check_type": latest.get("check_type"),
            "cash_pct": float((dec(acct.get("cash")) / equity) if equity else Decimal("0")),
            "invested_base": float(invested_base),
            "overall_gain": float(overall_gain),
            "overall_gain_pct": float(overall_gain_pct),
        },
        "positions": enriched_positions,
        "snapshots": snapshots,
        "history": history_points,
        "history_meta": portfolio_history,
        "checks": checks[-20:],
        "trades": trades[-20:],
        "watch": watch,
        "reasons": summarize_reasons(latest, trades, checks),
    }


def html_page(data: dict) -> str:
    data_json = json.dumps(data, separators=(",", ":"))
    generated = html.escape(data["generated_at"])
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>InvestAnswers Portfolio PM Dashboard</title>
  <script src=\"https://cdn.plot.ly/plotly-2.35.2.min.js\"></script>
  <style>
    :root {{ color-scheme: light; --bg:#FAF7F0; --paper:#FFFDF8; --panel:#FFFFFF; --ink:#191919; --muted:#6F6760; --line:#E8DED2; --green:#4F8F64; --red:#B85C5C; --gold:#B88746; --blue:#526E8F; --purple:#8B6F9F; --clay:#CC785C; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font-family: Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif; background:var(--bg); color:var(--ink); }}
    main {{ width:min(1180px, 94vw); margin:0 auto; padding:30px 0 58px; }}
    .hero {{ display:flex; gap:20px; justify-content:space-between; align-items:flex-end; flex-wrap:wrap; margin-bottom:18px; }}
    .eyebrow {{ color:var(--clay); font-size:12px; letter-spacing:.12em; text-transform:uppercase; font-weight:750; }}
    h1 {{ margin:8px 0 8px; font-size:clamp(30px, 5vw, 54px); letter-spacing:-.045em; line-height:.98; font-weight:820; }}
    .sub {{ color:var(--muted); max-width:760px; line-height:1.55; }}
    .grid {{ display:grid; grid-template-columns:repeat(12,1fr); gap:14px; }}
    .card {{ grid-column:span 12; background:var(--panel); border:1px solid var(--line); border-radius:18px; padding:18px; box-shadow: 0 12px 32px rgba(54, 45, 38, .08); }}
    .metric {{ grid-column:span 3; min-height:126px; }}
    .wide {{ grid-column:span 8; }} .side {{ grid-column:span 4; }} .half {{ grid-column:span 6; }}
    .label {{ color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.1em; font-weight:800; }}
    .value {{ font-size:32px; font-weight:900; letter-spacing:-.04em; margin-top:12px; }}
    .delta {{ margin-top:8px; color:var(--muted); font-size:13px; }}
    .green {{ color:var(--green); }} .red {{ color:var(--red); }} .gold {{ color:var(--gold); }} .blue {{ color:var(--blue); }}
    .chart {{ height:380px; }} #allocChart {{ height:430px; }}
    table {{ width:100%; border-collapse:collapse; font-size:14px; }}
    th,td {{ text-align:left; border-bottom:1px solid var(--line); padding:12px 8px; white-space:nowrap; }}
    th {{ color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.08em; }}
    tr:last-child td {{ border-bottom:0; }}
    .pill {{ display:inline-flex; align-items:center; border:1px solid var(--line); background:var(--paper); border-radius:999px; padding:6px 10px; font-size:12px; color:var(--muted); gap:6px; }}
    .stack {{ display:flex; flex-direction:column; gap:12px; }}
    .reason {{ padding:12px 14px; background:var(--paper); border:1px solid var(--line); border-radius:14px; color:var(--ink); line-height:1.45; }}
    .timeline {{ display:flex; flex-direction:column; gap:10px; max-height:520px; overflow:auto; padding-right:4px; }}
    .event {{ border-left:3px solid var(--clay); background:var(--paper); border-radius:14px; padding:11px 12px; }}
    .event strong {{ display:block; margin-bottom:5px; }}
    .event small {{ color:var(--muted); }}
    .watch {{ display:grid; grid-template-columns:90px 90px 1fr; gap:10px; align-items:center; border-bottom:1px solid var(--line); padding:10px 0; }}
    .watch:last-child {{ border-bottom:0; }}
    footer {{ color:var(--muted); font-size:12px; margin-top:18px; line-height:1.5; }}
    a {{ color:var(--blue); }}
    @media (max-width: 860px) {{ .metric,.wide,.side,.half {{ grid-column:span 12; }} table {{ font-size:12px; }} th,td {{ padding:9px 5px; }} .chart,#allocChart {{ height:330px; }} .watch {{ grid-template-columns:70px 80px 1fr; }} }}
  </style>
</head>
<body>
<main>
  <section class=\"hero\">
    <div>
      <div class=\"eyebrow\">Alpaca paper · InvestAnswers PM</div>
      <h1>Portfolio dashboard</h1>
      <div class=\"sub\">Simple, light portfolio ledger built from real Alpaca paper data plus the strategy repo. The performance chart uses multi-month daily Alpaca portfolio history, not just today's snapshots.</div>
    </div>
    <div class=\"pill\">Generated {generated}</div>
  </section>

  <section class=\"grid\">
    <div class=\"card metric\"><div class=\"label\">Overall return</div><div class=\"value\" id=\"mOverallReturn\">--</div><div class=\"delta\" id=\"mOverallGain\"></div></div>
    <div class=\"card metric\"><div class=\"label\">Equity</div><div class=\"value\" id=\"mEquity\">--</div><div class=\"delta\" id=\"mEquityDelta\"></div></div>
    <div class=\"card metric\"><div class=\"label\">Cash buffer</div><div class=\"value\" id=\"mCash\">--</div><div class=\"delta\" id=\"mCashPct\"></div></div>
    <div class=\"card metric\"><div class=\"label\">Latest PM call</div><div class=\"value\" style=\"font-size:21px\" id=\"mCall\">--</div><div class=\"delta\">Trade/watch/rebalance ledger</div></div>

    <div class=\"card wide\"><div class=\"label\">Growth / fall over months</div><div class=\"delta\" id=\"historyMeta\"></div><div id=\"equityChart\" class=\"chart\"></div></div>
    <div class=\"card side\"><div class=\"label\">Allocation</div><div id=\"allocChart\"></div></div>

    <div class=\"card half\"><div class=\"label\">What changed / why it matters</div><div class=\"stack\" id=\"reasons\"></div></div>
    <div class=\"card half\"><div class=\"label\">Watch levels</div><div id=\"watchList\"></div></div>

    <div class=\"card\"><div class=\"label\">Positions</div><div style=\"overflow:auto\"><table id=\"positionsTable\"></table></div></div>
    <div class=\"card wide\"><div class=\"label\">Position P/L</div><div id=\"plChart\" class=\"chart\"></div></div>
    <div class=\"card side\"><div class=\"label\">Trade / decision timeline</div><div class=\"timeline\" id=\"timeline\"></div></div>
  </section>
  <footer>Data source: sanitized Alpaca paper snapshots + repo logs only. No account numbers, credentials, or secrets are embedded. Everything can go to zero. Not financial advice.</footer>
</main>
<script id=\"dashboard-data\" type=\"application/json\">{data_json}</script>
<script>
const data = JSON.parse(document.getElementById('dashboard-data').textContent);
const fmt = new Intl.NumberFormat('en-US', {{style:'currency', currency:'USD'}});
const pct = v => `${{(v*100).toFixed(1)}}%`;
const color = getComputedStyle(document.documentElement);
const green = color.getPropertyValue('--green').trim(), red = color.getPropertyValue('--red').trim(), blue = color.getPropertyValue('--blue').trim(), gold = color.getPropertyValue('--gold').trim(), purple = color.getPropertyValue('--purple').trim();

function latestCall() {{
  const trades = data.trades || [];
  const last = trades[trades.length - 1];
  if (!last) return 'Watch / setup';
  return `${{last.action || 'Decision'}}`;
}}
function firstLastDelta(rows) {{
  if (!rows || rows.length < 2) return '';
  const first = rows[0].equity, last = rows[rows.length-1].equity;
  const d = last - first;
  const pc = first ? d/first : 0;
  return `${{d >= 0 ? '+' : ''}}${{fmt.format(d)}} (${{pc >= 0 ? '+' : ''}}${{(pc*100).toFixed(2)}}%) since first history point`;
}}
document.getElementById('mEquity').textContent = fmt.format(data.account.equity || 0);
document.getElementById('mEquityDelta').textContent = `${{(data.positions || []).length}} open positions · ${{firstLastDelta(data.history || data.snapshots || [])}}`;
document.getElementById('mOverallReturn').textContent = `${{((data.account.overall_gain_pct || 0) * 100).toFixed(2)}}%`;
document.getElementById('mOverallReturn').className = `value ${{numClass(data.account.overall_gain || 0)}}`;
document.getElementById('mOverallGain').textContent = `${{data.account.overall_gain >= 0 ? '+' : ''}}${{fmt.format(data.account.overall_gain || 0)}} since ${{fmt.format(data.account.invested_base || 0)}} base invested`;
const histMeta = data.history_meta || {{}};
document.getElementById('historyMeta').textContent = histMeta.ok ? `${{histMeta.period}} daily Alpaca portfolio history · starts ${{histMeta.base_value_asof || 'first funded day'}}` : 'Fallback: local check snapshots only';
document.getElementById('mCash').textContent = fmt.format(data.account.cash || 0);
document.getElementById('mCashPct').textContent = `${{pct(data.account.cash_pct || 0)}} of equity · target ~10%`;
document.getElementById('mCall').textContent = latestCall();

document.getElementById('reasons').innerHTML = (data.reasons || []).map(r => `<div class=\"reason\">${{escapeHtml(r)}}</div>`).join('');
document.getElementById('watchList').innerHTML = (data.watch || []).map(w => `<div class=\"watch\"><strong>${{escapeHtml(w.symbol)}}</strong><span class=\"pill\">${{w.price ? fmt.format(w.price) : 'n/a'}}</span><span>${{escapeHtml(w.rule)}}</span></div>`).join('');

function escapeHtml(s) {{ return String(s ?? '').replace(/[&<>\"]/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}}[c])); }}
function numClass(v) {{ return v >= 0 ? 'green' : 'red'; }}

const rows = data.positions || [];
document.getElementById('positionsTable').innerHTML = `<thead><tr><th>Symbol</th><th>Qty</th><th>Price</th><th>Value</th><th>Weight</th><th>Cost</th><th>Unrealized</th><th>Today</th></tr></thead><tbody>` + rows.map(p => `<tr><td><strong>${{p.symbol}}</strong></td><td>${{p.qty.toFixed(4)}}</td><td>${{fmt.format(p.current_price)}}</td><td>${{fmt.format(p.market_value)}}</td><td>${{pct(p.weight)}}</td><td>${{fmt.format(p.cost_basis)}}</td><td class=\"${{numClass(p.unrealized_pl)}}\">${{fmt.format(p.unrealized_pl)}} · ${{pct(p.unrealized_plpc)}}</td><td class=\"${{numClass(p.change_today)}}\">${{pct(p.change_today)}}</td></tr>`).join('') + `</tbody>`;

const snaps = data.history || data.snapshots || [];
const x = snaps.map(s => s.timestamp_short || s.timestamp);
Plotly.newPlot('equityChart', [
  {{x, y: snaps.map(s => s.equity), name:'Equity', mode:'lines', line:{{color:blue, width:3}}, fill:'tozeroy', fillcolor:'rgba(82,110,143,.10)'}},
  {{x, y: snaps.map(s => s.profit_loss || 0), name:'Daily P/L', mode:'lines', yaxis:'y2', line:{{color:gold, width:1.7, dash:'dot'}}}}
], {{paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{{color:'#191919'}}, margin:{{l:55,r:18,t:20,b:55}}, hovermode:'x unified', yaxis:{{gridcolor:'#E8DED2', tickprefix:'$'}}, yaxis2:{{overlaying:'y', side:'right', showgrid:false, tickprefix:'$', zeroline:false}}, xaxis:{{gridcolor:'#E8DED2', rangeslider:{{visible:true}}}}, legend:{{orientation:'h'}}}}, {{responsive:true, displaylogo:false}});

Plotly.newPlot('allocChart', [{{labels: rows.map(p=>p.symbol), values: rows.map(p=>p.market_value), type:'pie', hole:.58, textinfo:'label+percent', marker:{{colors:[blue,'#7C8F66','#B88746','#CC785C','#8B6F9F','#A76E5E','#6F8795']}}}}], {{paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{{color:'#191919'}}, margin:{{l:10,r:10,t:20,b:20}}, showlegend:false}}, {{responsive:true, displaylogo:false}});

Plotly.newPlot('plChart', [{{x: rows.map(p=>p.symbol), y: rows.map(p=>p.unrealized_pl), type:'bar', marker:{{color: rows.map(p => p.unrealized_pl >= 0 ? green : red)}}}}], {{paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{{color:'#191919'}}, margin:{{l:55,r:18,t:20,b:55}}, yaxis:{{gridcolor:'#E8DED2', tickprefix:'$'}}, xaxis:{{gridcolor:'#E8DED2'}}}}, {{responsive:true, displaylogo:false}});

const events = [...(data.trades || [])].reverse().slice(0, 12);
document.getElementById('timeline').innerHTML = events.map(e => `<div class=\"event\"><strong>${{escapeHtml(e.timestamp_et || '')}} · ${{escapeHtml(e.asset || '')}}</strong><div>${{escapeHtml(e.action || '')}} · ${{escapeHtml(e.status || '')}}</div><small>${{escapeHtml(e.rationale || e.outcome || '').slice(0,260)}}</small></div>`).join('');
</script>
</body>
</html>"""


def main() -> int:
    PUBLIC.mkdir(parents=True, exist_ok=True)
    data = build_data()
    (PUBLIC / "dashboard-data.json").write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    (PUBLIC / "index.html").write_text(html_page(data))
    print(json.dumps({
        "public_dir": str(PUBLIC),
        "index": str(PUBLIC / "index.html"),
        "data": str(PUBLIC / "dashboard-data.json"),
        "generated_at": data["generated_at"],
        "equity": data["account"]["equity"],
        "cash": data["account"]["cash"],
        "overall_gain_pct": data["account"]["overall_gain_pct"],
        "overall_gain": data["account"]["overall_gain"],
        "positions": len(data["positions"]),
        "snapshots": len(data["snapshots"]),
        "history_points": len(data["history"]),
        "history_period": (data.get("history_meta") or {}).get("period"),
        "trades": len(data["trades"]),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
