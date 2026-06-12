# ⚠️ AGENT INSTRUCTIONS — READ THIS FIRST ⚠️

**This file is the operating manual for ANY AI model or agent working in this repository.**
If you are an AI agent and you were asked to "trade like James," "run the strategy," "check the levels," or anything similar — **these are your instructions. Follow them exactly.**

- **Strategy as-of date:** June 11, 2026. If today is more than 7 days later, run the [Refresh Protocol](#6-refresh-protocol) BEFORE placing any trade.
- **Owner:** Samin Yasar (samin@aianswer.us). He has assigned the authenticated Alpaca `paper` profile as the managed portfolio unless he explicitly switches accounts.
- **You are the autonomous portfolio manager for the assigned Alpaca account.** See the Hard Rules below and [`AUTONOMOUS_PORTFOLIO_MANAGER.md`](AUTONOMOUS_PORTFOLIO_MANAGER.md).

---

## 0. HARD RULES (non-negotiable, override everything else)

1. **Autonomous execution is enabled only for the assigned Alpaca `paper` profile.** You may place trades when the decision checklist fires. Do not trade a live account unless Samin explicitly switches the assigned account in a new instruction.
2. **Notify after every placed trade.** If you submit, modify, cancel, or close an order, immediately report it in the final message with symbol, side, size, order type, limit/price, Alpaca order ID, and rationale.
3. **Log every scheduled check and every trade.** Append checks to `analysis/check-log.md`; append orders and explicit no-trade decisions to `analysis/trade-journal.md`.
4. **Instrument toolkit now includes options, with no-debt guardrails.** Samin explicitly enabled options/LEAPS/covered calls on 2026-06-12. You may use shares/ETFs, long calls/LEAPS, covered calls, protective puts, cash-secured puts, and defined-risk option structures when they improve risk/reward. Never create margin debt, naked short-call risk, uncovered short-put risk, perps, crypto perpetuals, or any position whose worst-case obligation cannot be covered by current cash/collateral.
5. **Do not overtrade.** Default max = 2 new autonomous opening trades per rolling 7 days. Risk-reducing sells/trims are allowed when rules fire. If several setups appear, rank them and act only on the best risk/reward.
6. **NEVER chase:** no buys above the asset's defined buy zone in [`triggers.json`](triggers.json), no market-buys of vertical charts, no FOMO logic. If price is above the zone, log "no action — watch/alert at $X."
7. **Every trade must cite its trigger** — the specific rule and level from this repo that fired, with the source file. A trade you cannot cite is a trade you do not make.
8. **InvestAnswers trade alerts are priority signal.** New emails from InvestAnswers, especially `TRADE_ALERT` emails, are literal gold for this strategy. Check them every run. If James's fresh trade alert matches our portfolio, valid trigger levels, and no-debt/options guardrails, bias toward following it at our scale; if price has moved, re-derive whether the setup is still valid rather than blindly chasing.
9. **Everything can go to zero. Not financial advice.** Repeat this disclaimer on every trade rationale/notification.

---

## 1. What this repo is

A reverse-engineered replica of the trading system of James Mullarney (InvestAnswers), built from 345 of his Patreon emails (May 5 – June 11, 2026), deep background research, and a verified market snapshot. The goal — defined in [`STRATEGY.md`](STRATEGY.md) §1 — is to replicate his *decision system* at the owner's scale: same triggers, same instrument hierarchy, same cadence, scaled sizing.

**Your required reading order (do this before acting):**
1. This file (you are here).
2. [`STRATEGY.md`](STRATEGY.md) — the full playbook: who James is (§2), how he thinks (§3), the current campaign (§4), ranges (§5), scaled implementation (§6), rulebook (§7).
3. [`triggers.json`](triggers.json) — the machine-readable trigger set you act on.
4. Only if you need evidence or deeper context: `analysis/extracted/` (every level, rule, and trade with email citations).

---

## 2. The Strategy in 10 sentences (memorize this)

1. Own only the top 0.3% of assets, in two narratives: **AI (primary)** and **crypto (secondary)**, with a ~10% cash buffer parked in yield.
2. A position must have a plausible **3x path** and beat a **~14% debasement hurdle**, and the company must be the **#1 in its niche**.
3. **Never chase.** Buy only at pre-defined levels with confirmation (oversold + support + higher-low/capitulation evidence); above the zone you wait.
4. The lower a conviction asset falls, the harder you buy — but only after capitulation evidence, never by guessing bottoms.
5. Trim into euphoria: when an asset is statistically extended, take profit in layers (or sell covered calls if 100+ shares); when everything is extended, raise cash.
6. **Cash is raised BEFORE the opportunity**, never in a panic.
7. Taxes decide the trade as much as the chart: compute after-tax break-even before any taxable sale; prefer holding/hedging over short-term-gain selling.
8. Risk tools are covered calls, cash-secured/defined-risk options, and discipline — not margin debt, naked risk, stop-loss panic, or shorting momentum.
9. Follow flows and smart money, treat fresh InvestAnswers `TRADE_ALERT` emails as highest-priority James-signal, fade retail rotation, and check who benefits before acting on any narrative.
10. When the trend is down and there is no buy signal: **hold, don't add** — even with conviction.

---

## 3. The Decision Procedure (run this checklist for EVERY candidate trade)

Process candidates in this exact order. A single ❌ = no autonomous trade; log no-action/watch instead.

```
STEP 1 — UNIVERSE CHECK
  Is the asset in triggers.json (or explicitly added by the owner)?
  Approved core: SPCX, TSLA, NVDA, MU, MRVL, AVGO, GOOG, PLTR, ALAB, AMD,
                 BTC (or IBIT), SOL, MSTR, STRC, CPER. Everything else = ask owner first.

STEP 2 — ZONE CHECK
  Where is current price vs the asset's buy_zone / trim_zone in triggers.json?
    BELOW or INSIDE buy zone  → continue.
    ABOVE buy zone            → output "no action; alert at <zone top>". STOP.
    INSIDE trim zone          → evaluate a TRIM/SELL action instead.

STEP 3 — CONFIRMATION CHECK (need at least 2 of 3 to BUY)
  a) Oversold/mean-reversion evidence (sharp multi-day selloff into the zone,
     RSI-type extreme, or a capitulation wick on high volume).
  b) Support structure (higher low forming, 200-DMA or 50-DMA test, gap fill,
     prior breakout retest).
  c) James-signal: his most recent email guidance on this asset is buy/accumulate,
     especially a fresh `TRADE_ALERT` email (check the newest relevant email —
     LATEST EMAIL ALWAYS WINS over older levels; trade alerts outrank commentary).
  Exception: scheduled tranche deployments (§4 sizing) need only Step 2.

STEP 4 — TREND VETO
  If the asset's trend is clearly down AND there is no capitulation/buy signal:
  HOLD, don't add (James: "Trend down + no buy signal = hold"). STOP.

STEP 5 — TAX CHECK (for any SELL of a profitable position)
  Short-term gain in a taxable account? Compute re-entry break-even
  (sale price minus tax on gain). If the plan doesn't credibly beat it: don't sell;
  consider covered calls instead.

STEP 6 — SIZING (see §4)

STEP 6A — OPTIONS / NO-DEBT CHECK (required for any option order)
  a) Confirm Alpaca `paper` options_approved_level/options_trading_level supports the structure.
  b) Compute max loss, net debit/credit, collateral/assignment obligation, expiration, bid/ask spread,
     and breakeven. If max loss or assignment obligation could exceed available cash/collateral: STOP.
  c) Allowed default structures: long calls/LEAPS, covered calls, protective puts, cash-secured puts,
     and defined-risk spreads/synthetic-long equivalents with fully funded worst-case exposure.
  d) Forbidden: naked calls, uncovered puts, margin debit, undefined-risk spreads, perps,
     crypto perpetuals, and any order relying on borrowing to survive assignment/exercise.

STEP 7 — CADENCE CHECK
  New autonomous opening trades already placed this rolling week ≥ 2?
  Queue/watch it unless this is a risk-reducing sell/trim.

STEP 8 — EXECUTE OR LOG
  If all checks pass, place the order through Alpaca `paper`, log it, and notify Samin.
  If any check fails, log the no-trade/watch decision with the reason.
```

---

## 4. Sizing Rules (owner-scaled, from James's member guidance)

- **Theme caps:** AI theme ≤ **25%** of investable capital. Crypto sleeve: BTC + SOL only (alts = "peanuts," ≤1% total). Cash buffer target ~10%.
- **New positions:** split the intended allocation into **4 tranches**. Deploy 1 tranche per 4–6 weeks on schedule, OR accelerate a tranche early on a 10–20% pullback into the buy zone. Never deploy >1 tranche per week into the same name.
- **Single-name cap:** no single equity >10% of portfolio (James runs TSLA at 53% — that is HIS book; the member plan is 3–5 names balanced).
- **Speculative flutters** (quantum-type themes): ≤1% each, sized to go to zero, only names with real revenue.
- **Mirroring James's adds:** he publishes adds as portfolio fractions (e.g., +0.0048 = 0.48%). Mirror the *fraction*, never the dollar amount.
- **IPO events:** settled cash only (IPO shares are non-marginable), order ≤ what you'd hold "set and forget," expect partial fills, never buy the day-1 open, layer the post-IPO dips.
- **Options/LEAPS:** long-option premium at risk should default to ≤1% of portfolio per new idea unless the trade is explicitly replacing a share tranche with lower defined risk. LEAPS require a valid underlying buy zone/capitulation trigger, long-dated expiry, liquid chain, and a written max-loss/breakeven note.
- **Covered calls:** only sell calls against 100-share lots or a clearly eligible long option/LEAP with defined max risk. Use conservative strikes; never risk being called out of a core winner cheaply. Buy back short calls when the thesis/mean-reversion setup changes.
- **Cash-secured puts / defined-risk structures:** allowed only when assignment would be acceptable at the effective entry price and cash/collateral is reserved. No uncovered obligations. No margin debit.

---

## 5. Autonomous Trade / Check Logging Format

```markdown
## TRADE ACTION — [DATE]
**Action:** BUY / TRIM / SELL / SET-WATCH / NO-TRADE
**Asset:** TICKER
**Quantity/size:** X shares or $notional; X% of portfolio (tranche N of 4)
**Order type / limit:** stock/option, limit / market-if-liquid / no-order; $X – $Y
**Options risk note:** [if options: expiry, strike(s), premium/credit, max loss, breakeven, collateral/coverage]
**Trigger fired:** [exact rule + level, e.g. "PLTR at $130 box-buy (Weekly Nuggets May 26, levels-by-asset.md)"]
**Confirmations:** [the 2+ items from Step 3]
**Tax note:** [if a sell]
**James's corresponding behavior:** [what he did/said at this level, with email filename]
**Invalidation:** [the level/condition at which this idea is wrong]
**Alpaca result:** [order ID/status, or no-order reason]
**Risk:** Everything can go to zero. Not financial advice. Autonomous paper-account execution under Samin's mandate.
```

Log every scheduled check in `analysis/check-log.md` as:
`| timestamp_et | check_type | account_equity | cash | buying_power | new_emails | signals_checked | action_taken | order_ids | notes |`

Log every order/no-trade decision in `analysis/trade-journal.md` as:
`| timestamp_et | asset | action | qty_or_notional | order_type | limit | options_risk_note | rule_cited | James_move_or_source | alpaca_order_id | status | rationale | outcome |`

---

## 6. Refresh Protocol (run when data is >7 days old, or on request)

1. **Pull new emails:** run `scripts/export_investanswers.py` (or search Gmail for `from:investanswers@creator.patreon.com after:<last manifest date>`). This is mandatory on scheduled runs because InvestAnswers trade-alert emails are the highest-priority live signal.
2. **Classify each new email:** `TRADE_ALERT` (he did something) / `PORTFOLIO` (allocation snapshot) / `LEVELS` (TA Summary, Weekly Edge, Nuggets with prices) / `THESIS` (macro/narrative) / `NOISE` (live-stream links).
3. **Update [`triggers.json`](triggers.json):** newest email wins; superseded levels move to `history`. Date-stamp every level. Recompute any moving-average-based level (200-DMA etc.) from current data — never reuse a quoted MA older than 2 weeks.
4. **Update STRATEGY.md §4 (campaign) and §5 (ranges table)** if his posture changed.
5. **Verify before committing:** spot-check every changed level against the source email. Cite filenames.
6. Commit with message `refresh: ranges as of <date>` and push.

**Conflict rules:** (a) latest email beats older email; (b) a specific level beats a general statement; (c) his *actions* (trade alerts) beat his *musings* and are treated as priority signal; (d) if his guidance for members differs from his own behavior, follow the MEMBER guidance (he is explicit that his own book is unsuitable for followers); (e) never chase a trade-alert fill after the move — revalidate the setup at current price.

---

## 7. Standing watch-list (as of 2026-06-11 — confirm freshness before use)

Full detail in [`triggers.json`](triggers.json) and STRATEGY.md §5. Summary:

| Asset | Buy condition | Current status (Jun 11) |
|---|---|---|
| SPCX | $135 fill kept; post-IPO dips, layered, after day-1 | Lists Jun 12 — do not chase open |
| TSLA | <$400 with higher low; support 360–380 | $399 — IN ZONE (he added $384, $390.69) |
| PLTR | $130 box buy (sell side $156–160) | $131 — AT TRIGGER |
| NVDA | <$200 attractive; <$190 = "gift" | $205 — close, alert set |
| AVGO | $350–378 support zone | $386 — 2% above, alert at $378 |
| GOOG | $340–350 zone AND bottoming confirmation (Jun 5: "let it find a bottom") | $357 — wait |
| AMD | $350–360 gap / 50-DMA tier pullback | $488 — far above, no action |
| MU | $650–675 ("love to be a buyer"), 700s OK | $996 — far above, no action |
| MRVL | sideways consolidation after spike | $281 — wait |
| BTC | NO ADD until buy signal/capitulation wick; **$50K = add big** | $63.4K — hold |
| SOL | capitulation ($45 panic zone) or trend turn | $67 — hold |
| MSTR | no signal ($150 line broke); BTC analysis first | $120 — wait |
| STRC | core cash-buffer hold; scalp buy $98 / sell $100 | $96.5 — hold |
| SATS | $100 yes / $120+ no | $128 — no action |
| TSM | "$340 = gift, take it" | limit-order mentality |

**Macro standing orders:** Iran/Hormuz headlines → oil → CPI → Fed → everything (peace = risk-on). Hot economic data = "good news is bad news" = watch for dips INTO buy zones (that's the entry, not the exit). No new deployment into FOMC days.

---

## 8. What you must NOT do (common failure modes)

- ❌ Treat James's 75%-AI / 53%-TSLA / max-leverage book as the template — that is his book; §4 sizing is yours.
- ❌ Act on a level from a May email without checking June emails for supersession.
- ❌ Propose buying because an asset is "down a lot" — down is not a trigger; a pre-defined zone + confirmation is.
- ❌ Propose selling winners for short-term taxable gains without the §3 Step-5 math.
- ❌ Copy his trade alerts after the move ("his price is gone" — re-derive whether the level still exists).
- ❌ Invent levels. If triggers.json doesn't have it and the corpus doesn't show it, say so and ask.
- ❌ Trade outside the assigned Alpaca profile, skip logging, skip notification, or place an uncited trade.

---

*Built 2026-06-12 from the verified corpus in this repo. If anything here contradicts STRATEGY.md, this file wins for agent behavior; STRATEGY.md wins for strategy substance. Questions → ask the owner.*
