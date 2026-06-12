# Trade Journal

Every autonomous trade, trade alert, explicit no-trade decision, and later outcome review gets logged here. Never delete or rewrite history; corrections get a new row referencing the older row.

**Purpose (James's own endorsed loop):** "Feed your trade journal into an AI tutor and review trades objectively so you never repeat the same mistakes."

## Log

| timestamp_et | asset | action | qty_or_notional | order_type | limit | options_risk_note | rule_cited | James_move_or_source | alpaca_order_id | status | rationale | outcome |
|---|---|---|---:|---|---:|---|---|---|---|---|---|---|
| 2026-06-12 00:43 ET | — | JOURNAL UPDATED | — | — | — | — | AUTONOMOUS_PORTFOLIO_MANAGER.md | Samin authorized autonomous PM mode | — | setup | Replaced proposal-only journal with autonomous execution journal. | Baseline: see STRATEGY.md §5 and triggers.json. |
| 2026-06-12 setup | — | POLICY UPDATED | — | — | — | Options allowed only with max-loss/breakeven/collateral note; no debt/margin debit/naked risk | AGENT_INSTRUCTIONS.md §0/§3/§4 | Samin enabled options/LEAPS/covered calls | — | setup | Updated mandate: portfolio is agent-managed; tools may include options as long as worst-case exposure is covered. | Future option rows must fill `options_risk_note`. |
| 2026-06-12 13:56 ET | SPCX/TSLA/SATS | NO-TRADE / SET-WATCH | — | no order | — | No option order; no margin/debt allowed; cash $197.37 vs 10% buffer target ~$1.38K | triggers.json SPCX day-1 never chase; TSLA buy below 400; SATS small stab only below 100 | 2026-06-12 SPCX IPO update, IA TSLA buy at $395, Options Sweep on TSLA, SATS proxy email | — | watch | Fresh IA signal is bullish but current prices fail no-chase/cash guardrails: SPCX ~173.66 above IPO/mean-reversion zone, TSLA ~402 above below-400 zone, SATS ~112.84 above <$100 level. | Watch SPCX $140-$135 retest, TSLA <$400/higher-low or 380-395; no autonomous order placed. |
| 2026-06-12 14:03 ET | SPCX/TSLA/PLTR/watchlist | NO-TRADE / SET-WATCH | — | no order | — | No option order; options level 3 verified; max loss/collateral N/A; no margin/debt allowed; cash $197.37 is below 10% buffer target | triggers.json SPCX day-1 never chase; TSLA below-400 stacking zone; PLTR ~$130 box buy subject to cash/sizing guardrails; AVGO/NVDA/SATS/BTC/SOL/MSTR wait rules | Latest IA: 2026-06-12 SPCX IPO update + IA TSLA $395 trade alert + TSLA sweep + SOL recovery; no new emails in this run | — | watch | Fresh TSLA/SPCX signal is bullish, but current prices and cash veto autonomous adds: SPCX ~$172.95 above IPO/mean-reversion zone, TSLA ~$402.92 above <$400 trigger, PLTR ~$128.15 in zone but account already holds PLTR and cash is below buffer. | Watch SPCX $140-$135 retest, TSLA <$400/higher-low or 380-395, PLTR only if cash buffer restored; no autonomous order placed. |

## Review cadence

- **Every scheduled check:** append to `analysis/check-log.md` even if no trade is placed.
- **Every order:** append here with Alpaca order ID, source rule, and rationale before/after notification.
- **Weekly:** mark outcomes on open rows; note which rules fired correctly vs. produced bad trades.
- **Quarterly:** re-evaluate the 3–5 name basket and write a short retro — what worked, what failed, what to change.
