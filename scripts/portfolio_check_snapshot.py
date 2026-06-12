#!/usr/bin/env python3
"""Collect deterministic context for the autonomous portfolio-manager cron.

This script deliberately does not place trades. It gathers account, positions,
orders, latest market prices, and new-email export state so the Hermes cron
agent can make/log the autonomous decision with the repo instructions loaded.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "state" / "portfolio_manager"
PROFILE = "paper"
EASTERN = ZoneInfo("America/New_York")


def run(cmd: list[str], *, cwd: Path = ROOT, check: bool = False) -> dict:
    proc = subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True)
    result = {
        "cmd": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }
    if check and proc.returncode != 0:
        raise RuntimeError(json.dumps(result, indent=2))
    return result


def json_cmd(cmd: list[str], default):
    res = run(cmd)
    if res["returncode"] != 0 or not res["stdout"]:
        return {"error": res}
    try:
        return json.loads(res["stdout"])
    except json.JSONDecodeError:
        return {"parse_error": res}


def load_manifest_count() -> int:
    path = ROOT / "manifest.json"
    if not path.exists():
        return 0
    try:
        data = json.loads(path.read_text())
    except Exception:
        return 0
    if isinstance(data, list):
        return len(data)
    if isinstance(data, dict):
        for key in ("messages", "items", "emails"):
            value = data.get(key)
            if isinstance(value, list):
                return len(value)
        value = data.get("count")
        if isinstance(value, int):
            return value
    return 0


def asset_symbols() -> list[str]:
    data = json.loads((ROOT / "triggers.json").read_text())
    assets = sorted((data.get("assets") or {}).keys())
    # Symbols Alpaca stock data understands by default. BTC/SOL need crypto endpoints;
    # keep them in the strategy, but don't fail the snapshot on them.
    skip = {"BTC", "SOL"}
    return [s for s in assets if s not in skip]


def collect_prices(symbols: list[str]) -> dict:
    prices = {}
    for symbol in symbols:
        data = json_cmd([
            "alpaca", "--profile", PROFILE, "data", "latest-trade",
            "--symbol", symbol, "--jq", "."
        ], default={})
        price = None
        if isinstance(data, dict):
            price = (((data.get("trade") or {}).get("p")))
        prices[symbol] = {"price": price, "raw": data}
    return prices


def sanitize_account(account):
    if not isinstance(account, dict):
        return account
    keep = [
        "status", "currency", "portfolio_value", "equity", "last_equity",
        "cash", "buying_power", "regt_buying_power", "daytrading_buying_power",
        "non_marginable_buying_power", "long_market_value", "short_market_value",
        "maintenance_margin", "initial_margin", "multiplier", "shorting_enabled",
        "options_approved_level", "options_trading_level", "options_buying_power",
    ]
    return {k: account.get(k) for k in keep if k in account}


def sanitize_positions(positions):
    if not isinstance(positions, list):
        return positions
    keep = [
        "symbol", "asset_class", "exchange", "side", "qty", "qty_available",
        "avg_entry_price", "current_price", "lastday_price", "market_value",
        "cost_basis", "unrealized_pl", "unrealized_plpc",
        "unrealized_intraday_pl", "unrealized_intraday_plpc", "change_today",
    ]
    return [{k: row.get(k) for k in keep if k in row} for row in positions if isinstance(row, dict)]


def sanitize_orders(orders):
    if not isinstance(orders, list):
        return orders
    keep = [
        "id", "client_order_id", "symbol", "asset_class", "side", "qty",
        "notional", "type", "time_in_force", "limit_price", "stop_price",
        "status", "submitted_at", "filled_at", "filled_qty", "filled_avg_price",
        "order_class", "extended_hours",
    ]
    return [{k: row.get(k) for k in keep if k in row} for row in orders if isinstance(row, dict)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-type", default="manual", choices=["manual", "9am", "2pm", "5pm", "setup"])
    parser.add_argument("--skip-export", action="store_true", help="Do not run scripts/export_investanswers.py")
    args = parser.parse_args()

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    before_count = load_manifest_count()
    export_result = None
    if not args.skip_export:
        export_result = run([sys.executable, "scripts/export_investanswers.py"])
    after_count = load_manifest_count()

    account_raw = json_cmd(["alpaca", "--profile", PROFILE, "account", "get", "--jq", "."], default={})
    positions_raw = json_cmd(["alpaca", "--profile", PROFILE, "position", "list", "--jq", "."], default=[])
    orders_raw = json_cmd(["alpaca", "--profile", PROFILE, "order", "list", "--jq", "."], default=[])
    account = sanitize_account(account_raw)
    positions = sanitize_positions(positions_raw)
    orders = sanitize_orders(orders_raw)
    symbols = asset_symbols()
    prices = collect_prices(symbols)

    now_et = datetime.now(EASTERN)
    snapshot = {
        "timestamp_et": now_et.isoformat(timespec="seconds"),
        "check_type": args.check_type,
        "repo": str(ROOT),
        "profile": PROFILE,
        "manifest_count_before": before_count,
        "manifest_count_after": after_count,
        "new_email_count_estimate": max(0, after_count - before_count),
        "export_result": export_result,
        "account": account,
        "positions": positions,
        "open_orders": orders,
        "symbols_checked": symbols,
        "prices": prices,
    }

    out = STATE_DIR / "latest_snapshot.json"
    stamp = now_et.strftime("%Y%m%d_%H%M%S_%Z")
    hist = STATE_DIR / f"snapshot_{stamp}_{args.check_type}.json"
    text = json.dumps(snapshot, indent=2, sort_keys=True)
    out.write_text(text + "\n")
    hist.write_text(text + "\n")

    summary = {
        "timestamp_et": snapshot["timestamp_et"],
        "check_type": args.check_type,
        "new_email_count_estimate": snapshot["new_email_count_estimate"],
        "equity": account.get("equity") if isinstance(account, dict) else None,
        "cash": account.get("cash") if isinstance(account, dict) else None,
        "buying_power": account.get("buying_power") if isinstance(account, dict) else None,
        "options_buying_power": account.get("options_buying_power") if isinstance(account, dict) else None,
        "options_approved_level": account.get("options_approved_level") if isinstance(account, dict) else None,
        "options_trading_level": account.get("options_trading_level") if isinstance(account, dict) else None,
        "position_count": len(positions) if isinstance(positions, list) else None,
        "open_order_count": len(orders) if isinstance(orders, list) else None,
        "snapshot_file": str(out),
        "history_file": str(hist),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
