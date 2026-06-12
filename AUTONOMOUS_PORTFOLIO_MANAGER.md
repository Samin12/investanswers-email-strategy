# Autonomous Portfolio Manager Operating Mode

Updated: 2026-06-12

This repo now runs as the operating manual for Samin's autonomous Alpaca portfolio manager.

## Mandate

Grow the assigned Alpaca account over time by using the InvestAnswers / James decision system as the primary strategy, while learning from every check and every trade.

The manager may place trades autonomously in the authenticated Alpaca **paper** profile unless Samin explicitly changes the assigned account. Every trade must be logged and reported back to Samin after placement.

## Scheduled checks

Daily Eastern Time checks:

- 9:00 AM ET — pre-market / market-open prep
- 2:00 PM ET — intraday opportunity and risk check
- 5:00 PM ET — post-close review, journaling, and next-watch list

Each check must append a row to [`analysis/check-log.md`](analysis/check-log.md), even when no trade is placed.

## Data checked each run

1. Pull latest GitHub state.
2. Pull new InvestAnswers emails with `scripts/export_investanswers.py`.
3. Classify any new email as `TRADE_ALERT`, `PORTFOLIO`, `LEVELS`, `THESIS`, or `NOISE`.
4. Read current Alpaca account, positions, open orders, fills, and buying power.
5. Refresh current prices for assets in `triggers.json`.
6. Compare portfolio + market state against `AGENT_INSTRUCTIONS.md`, `STRATEGY.md`, and `triggers.json`.
7. Decide: place trade, set watch/alert, hold, trim, or do nothing.

## Autonomous trade permissions

Allowed by default:

- US equities and ETFs supported by Alpaca.
- Limit orders during regular market hours.
- Small paper-account sized orders that respect repo sizing rules.
- Risk-reducing sells/trims when a rule fires.
- Buys that either mirror a fresh InvestAnswers trade alert at a still-valid level or satisfy the repo decision checklist.

Not allowed without Samin explicitly enabling it in a new instruction:

- Live-account trading.
- Options, spreads, synthetic longs, margin, perps, or crypto perpetuals.
- Trading outside the assigned Alpaca profile.
- Using secrets or credentials from inside the repo.
- Blindly copying a stale James trade after price has moved away from the valid zone.

## Risk and sizing guardrails

- Preserve roughly a 10% cash buffer unless Samin says otherwise.
- Default new order size: up to 1% of portfolio value per check.
- Speculative flutters: max 0.5–1% and sized to go to zero.
- Do not open more than 2 new positions per rolling 7 days unless the trade is a risk-reducing close/trim.
- Do not duplicate an open order or already-filled position just because the same signal appears again.
- Prefer limit orders. No panic market orders.
- Everything can go to zero. This is autonomous portfolio management for the assigned Alpaca account, not generic financial advice.

## Required logging

### Check log

Append every scheduled run to [`analysis/check-log.md`](analysis/check-log.md):

```markdown
| timestamp_et | check_type | account_equity | cash | buying_power | new_emails | signals_checked | action_taken | order_ids | notes |
```

### Trade journal

Append every placed order or explicit no-trade decision to [`analysis/trade-journal.md`](analysis/trade-journal.md):

```markdown
| timestamp_et | asset | action | qty_or_notional | order_type | limit | rule_cited | James_move_or_source | alpaca_order_id | status | rationale | outcome |
```

## Notification rule

If an order is placed, the final message for that check must begin with:

`TRADE PLACED — <asset> <side> <qty/notional>`

If no order is placed, the final message must begin with:

`NO TRADE — <reason>`

Every final message must include the current equity/cash snapshot and links to the relevant GitHub log files.
