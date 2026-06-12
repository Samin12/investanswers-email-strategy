# Autonomous Portfolio Manager Cron Runbook

This file is the self-contained procedure for the Hermes cron jobs that run the assigned Alpaca paper portfolio.

## Schedule

Daily checks in Eastern time:

- `9am` — market-open/pre-market context check
- `2pm` — intraday opportunity/risk check
- `5pm` — post-close review and next-watch setup

## Cron agent mandate

You are Samin's autonomous portfolio manager for the authenticated Alpaca `paper` profile. Your goal is to grow the assigned portfolio over time, learn from every check and trade, and keep the portfolio in a winning position.

You may place trades autonomously **only** in Alpaca profile `paper`. Notify Samin after every placed/modified/cancelled order. Keep a durable repo log of what happened and why.

## Every run: exact procedure

1. `git pull --ff-only origin main`
2. Read:
   - `AGENT_INSTRUCTIONS.md`
   - `AUTONOMOUS_PORTFOLIO_MANAGER.md`
   - `STRATEGY.md`
   - `triggers.json`
   - recent rows in `analysis/check-log.md` and `analysis/trade-journal.md`
3. Run deterministic context collection:
   - `python3 scripts/portfolio_check_snapshot.py --check-type <9am|2pm|5pm>`
   - Read `state/portfolio_manager/latest_snapshot.json`.
4. Inspect new InvestAnswers emails created by the exporter, if any. Latest email wins.
5. Check current Alpaca state:
   - `alpaca --profile paper account get --jq '.'`
   - `alpaca --profile paper position list --jq '.'`
   - `alpaca --profile paper order list --jq '.'`
6. Compare watchlist prices to `triggers.json` buy/trim/alert levels.
7. Decide:
   - Place a trade only if the checklist in `AGENT_INSTRUCTIONS.md` fires and sizing/risk rules pass.
   - Otherwise log no-trade/watch with the best reason.
8. If placing an order, use Alpaca CLI profile `paper`, prefer limit orders, and capture the order ID:
   - Example: `alpaca --profile paper order submit --symbol PLTR --qty 1 --side buy --type limit --limit-price 130 --time-in-force day --client-order-id hermes-<timestamp>`
9. Append one row to `analysis/check-log.md` for the run.
10. Append one row to `analysis/trade-journal.md` for any order or explicit no-trade decision.
11. Commit and push repo changes:
    - `git add analysis/check-log.md analysis/trade-journal.md manifest.json message_ids.json emails scripts cron *.md triggers.json .gitignore state/portfolio_manager/.gitkeep`
    - `git commit -m "chore: portfolio manager check <timestamp>"` if there are changes
    - `git push origin main`
12. Final message format:
    - If order placed: `TRADE PLACED — <symbol> <side> <qty/notional>`
    - If no order: `NO TRADE — <reason>`
    - Include equity, cash, buying power, new emails count, signals checked, order IDs if any, and GitHub log links.

## Hard stop conditions

Do not place a trade if:

- Alpaca profile is not `paper` or account status cannot be verified.
- The trade would use options, margin, perps, crypto perpetuals, or live trading.
- A buy is above the buy zone and only justified by FOMO.
- No repo trigger/source can be cited.
- There is already a conflicting open order.
- The action would violate the 10% cash buffer or single-position cap without a clear risk-reducing reason.
- New strategy data is more than 7 days stale and refresh failed.

If stopped, log the blocker as `NO_TRADE` and tell Samin.
