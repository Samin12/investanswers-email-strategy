# Goal: InvestAnswers Trading Research Repo

Created: 2026-06-11T23:14:51Z
Updated: 2026-06-12 — Phase 1 (archive) and Phase 2 (analysis) complete.

## Primary objective

**Trade like James.** Replicate the InvestAnswers decision system — concentration in top-0.3% assets, pre-defined buy zones, options-as-income, tax-first exits, cash-before-opportunity — at our own scale and risk, using this repo as the source of truth.

The full goal definition, the reverse-engineered playbook, current price ranges, and the action plan live in [`STRATEGY.md`](STRATEGY.md).

## Phase status

1. ✅ **Archive** — 345 emails exported (May 5 – Jun 11, 2026) in raw `.eml`, cleaned markdown, and metadata JSON, with manifests.
2. ✅ **Analysis** — 16-agent extraction + deep research complete: 87 trades, 235 levels, 182 rules, 23 portfolio snapshots, model/framework research, James background research. See `analysis/extracted/` and `STRATEGY.md`.
3. ⬜ **Monitor** — non-executing cron: parse new InvestAnswers emails daily → classify (Trade Alert / Portfolio / Levels / Nuggets) → Telegram digest with the rule that fired.
4. ⬜ **Journal** — `analysis/trade-journal.md`: log every action as date / asset / action / level / rule / James's corresponding move.
5. ⬜ **Refresh loop** — re-run extraction weekly over new emails; keep the STRATEGY.md §5 ranges table current.

## Hard boundary

No autonomous trading execution is enabled in this phase. This repo is for archiving, research, learning, alerting, and strategy development first.
