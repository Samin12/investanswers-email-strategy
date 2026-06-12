# Trade Journal

Every autonomous trade, trade alert, explicit no-trade decision, and later outcome review gets logged here. Never delete or rewrite history; corrections get a new row referencing the older row.

**Purpose (James's own endorsed loop):** "Feed your trade journal into an AI tutor and review trades objectively so you never repeat the same mistakes."

## Log

| timestamp_et | asset | action | qty_or_notional | order_type | limit | options_risk_note | rule_cited | James_move_or_source | alpaca_order_id | status | rationale | outcome |
|---|---|---|---:|---|---:|---|---|---|---|---|---|---|
| 2026-06-12 00:43 ET | — | JOURNAL UPDATED | — | — | — | — | AUTONOMOUS_PORTFOLIO_MANAGER.md | Samin authorized autonomous PM mode | — | setup | Replaced proposal-only journal with autonomous execution journal. | Baseline: see STRATEGY.md §5 and triggers.json. |
| 2026-06-12 setup | — | POLICY UPDATED | — | — | — | Options allowed only with max-loss/breakeven/collateral note; no debt/margin debit/naked risk | AGENT_INSTRUCTIONS.md §0/§3/§4 | Samin enabled options/LEAPS/covered calls | — | setup | Updated mandate: portfolio is agent-managed; tools may include options as long as worst-case exposure is covered. | Future option rows must fill `options_risk_note`. |

## Review cadence

- **Every scheduled check:** append to `analysis/check-log.md` even if no trade is placed.
- **Every order:** append here with Alpaca order ID, source rule, and rationale before/after notification.
- **Weekly:** mark outcomes on open rows; note which rules fired correctly vs. produced bad trades.
- **Quarterly:** re-evaluate the 3–5 name basket and write a short retro — what worked, what failed, what to change.
