# Goal: InvestAnswers Trading Research Repo

Created: 2026-06-11T23:14:51Z

## Primary objective

Make this repository the source of truth for the InvestAnswers / James-inspired trading research system before doing deeper analysis or cron automation.

## Immediate scope

1. Export all Gmail messages from `investanswers@creator.patreon.com` into this repo.
2. Preserve each email in three forms:
   - raw `.eml` for auditability,
   - cleaned markdown for reading/LLM analysis,
   - structured metadata JSON for indexing.
3. Generate repository-level manifests and summaries.
4. Commit the corpus and scripts to local git.
5. Only after the repo is complete, analyze the corpus for James-style indicators, thesis patterns, risk rules, and alert behavior.
6. Only after analysis, set up a non-executing monitor/alert cron job.

## Hard boundary

No autonomous trading execution is enabled in this phase. This repo is for archiving, research, learning, alerting, and strategy development first.
