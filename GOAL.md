# Goal: InvestAnswers Trading Research Repo

Created: 2026-06-11T23:14:51Z
Updated: 2026-06-12 — Phase 1 (archive) and Phase 2 (analysis) complete.

## Primary objective

**Trade like James.** Replicate the InvestAnswers decision system — concentration in top-0.3% assets, pre-defined buy zones, options-as-income, tax-first exits, cash-before-opportunity — at our own scale and risk, using this repo as the source of truth.

The full goal definition, the reverse-engineered playbook, current price ranges, and the action plan live in [`STRATEGY.md`](STRATEGY.md).

## Phase status

1. ✅ **Archive** — 345 emails exported (May 5 – Jun 11, 2026) in raw `.eml`, cleaned markdown, and metadata JSON, with manifests.
2. ✅ **Analysis** — 16-agent extraction + deep research complete: 87 trades, 235 levels, 182 rules, 23 portfolio snapshots, model/framework research, James background research. See `analysis/extracted/` and `STRATEGY.md`.
3. ✅ **Autonomous PM mode** — Samin authorized the agent to manage the assigned Alpaca paper account autonomously, notify after trades, and log every check/trade.
4. ⬜ **Scheduled checks** — daily 9:00, 14:00, and 17:00 ET crons: parse new InvestAnswers emails → classify → check portfolio/levels → trade if the checklist fires → Telegram summary.
5. ⬜ **Journal + check log** — `analysis/trade-journal.md` logs orders/no-trade decisions; `analysis/check-log.md` logs every scheduled check.
6. ⬜ **Refresh loop** — re-run extraction weekly over new emails; keep the STRATEGY.md §5 ranges table current.

## Operating boundary

Autonomous execution is enabled for the authenticated Alpaca `paper` profile only, under [`AUTONOMOUS_PORTFOLIO_MANAGER.md`](AUTONOMOUS_PORTFOLIO_MANAGER.md). Live-account trading, options, spreads, margin, perps, and crypto perpetuals remain disabled unless Samin explicitly enables them later.
