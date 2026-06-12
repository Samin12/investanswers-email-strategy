# InvestAnswers Email Strategy Repo

**AI agents: your operating manual is [`AGENT_INSTRUCTIONS.md`](AGENT_INSTRUCTIONS.md). Read it in full before doing anything in this repo.** It defines the hard rules (no autonomous trade execution, proposals only, max 2/week, never chase), the decision checklist, sizing, the proposal output format, and the refresh protocol.

Quick map:
- [`AGENT_INSTRUCTIONS.md`](AGENT_INSTRUCTIONS.md) — how an agent must operate (binding).
- [`triggers.json`](triggers.json) — machine-readable buy/trim/alert levels (check `as_of`; refresh if >7 days old).
- [`STRATEGY.md`](STRATEGY.md) — the full strategy: James's playbook, current campaign, ranges, rulebook.
- [`GOAL.md`](GOAL.md) — phase status.
- `analysis/extracted/` — evidence base (every trade/level/rule cited to a source email).
- `emails/text_md/` — the 345-email corpus (May 5 – Jun 11, 2026).

Conflict rule: AGENT_INSTRUCTIONS.md governs agent behavior; STRATEGY.md governs strategy substance; the newest email in `emails/` beats both on price levels.
