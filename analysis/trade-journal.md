# Trade Journal

Every autonomous trade, trade alert, explicit no-trade decision, and later outcome review gets logged here. Never delete or rewrite history; corrections get a new row referencing the older row.

**Purpose (James's own endorsed loop):** "Feed your trade journal into an AI tutor and review trades objectively so you never repeat the same mistakes."

## Log

| timestamp_et | asset | action | qty_or_notional | order_type | limit | rule_cited | James_move_or_source | alpaca_order_id | status | rationale | outcome |
|---|---|---|---:|---|---:|---|---|---|---|---|---|
| 2026-06-12 00:43 ET | — | JOURNAL UPDATED | — | — | — | AUTONOMOUS_PORTFOLIO_MANAGER.md | Samin authorized autonomous PM mode | — | setup | Replaced proposal-only journal with autonomous execution journal. | Baseline: see STRATEGY.md §5 and triggers.json. |

## Review cadence

- **Every scheduled check:** append to `analysis/check-log.md` even if no trade is placed.
- **Every order:** append here with Alpaca order ID, source rule, and rationale before/after notification.
- **Weekly:** mark outcomes on open rows; note which rules fired correctly vs. produced bad trades.
- **Quarterly:** re-evaluate the 3–5 name basket and write a short retro — what worked, what failed, what to change.
