# Trading Like James — Goal & Strategy
**InvestAnswers (James Mullarney) replication system**
*Built from 345 emails (May 5 – June 11, 2026), deep research on James, and live market data as of June 11, 2026 market close.*

> **Disclaimer:** Research document and autonomous paper-account operating manual, not generic financial advice. James's own words apply doubly here: "My goals are not your goals. This is a VERY AGGRESSIVE PORTFOLIO." and "NOT FINANCIAL ADVICE — EVERYTHING CAN GO TO ZERO." Per [GOAL.md](GOAL.md), Samin has enabled autonomous execution for the assigned Alpaca `paper` profile only.
>
> **🤖 If you are an AI agent tasked with running this strategy:** this document is the strategy *substance*; your binding *operating procedure* (hard rules, decision checklist, sizing, autonomous order/no-trade format, refresh protocol) is [`AGENT_INSTRUCTIONS.md`](AGENT_INSTRUCTIONS.md), with the machine-readable levels in [`triggers.json`](triggers.json). Read those first.

---

## 1. The Goal

**Replicate James's *decision system*, not his fills.** By the time a trade alert email arrives, his price is usually gone. The edge is not copying him with a lag — it's internalizing his playbook so the same triggers produce the same actions in our account, at our scale, ideally before or simultaneously with his alerts.

Measurable definition of "trading exactly like James":

1. **Same book structure, scaled.** Two-narrative concentration (AI primary, crypto secondary) with a yield-bearing cash buffer — at percentages chosen for our risk (see §6; he explicitly tells members NOT to run his 75% AI / max-leverage book).
2. **Same triggers.** Every buy/trim/hedge happens at a pre-defined level from his framework (§5 ranges table), never on impulse. "Know your exit before you enter."
3. **Same instruments hierarchy.** Shares first → covered calls once 100+ shares → LEAPS/synthetic longs only at capitulation extremes (his rule for members: don't copy the spreads at all until proven).
4. **Same cadence.** 1–2 trades per week maximum. He's explicit that overtrading is how retail loses.
5. **Tracked.** Every action logged in this repo against the rule that justified it, so we can audit whether we're actually trading like him or just feeling like we are.

---

## 2. Who we are copying (read this honestly)

James Mullarney, Irish-born, SF Bay Area, ~577K YouTube subs. Runs daily livestreams + the Patreon whose emails fill this repo. Quant-flavored: proprietary indicators (Mean Reversion "MR" oscillator, Confluence model, Optimized Trend, ATR/LILO level tiers — the IADSS suite), TABI Bitcoin top/bottom model, power-law/quantile BTC models, Monte Carlo "Retire On" compounding models.

**Track record, both sides:**
- **Hits:** early Solana (2021), BTC ETF cycle front-run, Tesla at ~$200 pre-run, the 2023→2026 crypto→AI rotation (IA13 created summer 2025 — MU/MRVL/ALAB gains since "smoked" his decade-long BTC stack), 2024 self-scorecard 81.5%.
- **Misses:** missed the Nov 2021 top, **sold his entire SOL stack near the post-FTX bottom** (~$10–13, before a 20x), shilled FTX/BlockFi/Celsius-era platforms, "Retire on ETH by 2030"-era marketing. His claimed institutional-finance background is disputed (#RektAnswers campaign); the verifiable career is Silicon Valley marketing analytics.
- **2026:** admitted "We expected Q1 to be bad. Not quite this bad" on BTC, and that he misjudged how fast AI would damage software stocks.

**Implication:** copy the *system* (it's coherent, disciplined, risk-aware) — but never suspend judgment because "James said so." He is best when buying pre-defined dips in conviction names and monetizing extension; he is historically worst at cycle tops and at capitulating near bottoms of assets he's lost faith in.

---

## 3. The James Operating System (how he thinks)

Seven pillars, each directly evidenced in the corpus (`analysis/extracted/` has full citations):

### 3.1 Extreme concentration in the top 0.3%
"86 of ~30,000 US stocks created half of all net wealth — be in the top 0.3%." Two narratives only: **AI (primary) + Crypto (secondary)**, with tiny "edge trades" around the core (long copper, short oil, short AVIS). Winner-takes-most: own the #1 (MU over SNDK/Hynix; Visa-not-Mastercard logic; INTC rejected outright). Even 50–60 positions is "ludicrous" to him — a fund manager with 100+ left him incredulous; focus IS the edge. A play must offer a plausible **3x** (TSLA to $4.5T: yes; NVDA to $16.5T: no) and beat his **~14% global fiat debasement hurdle**.

### 3.2 Asymmetry through long-dated options, bought only at extremes
- **LEAPS doctrine:** "I buy LEAPS on companies I want to own long term and the lower they go the harder I go. I always convert unless thesis changes." Bought only at capitulation (TSLA $106, NVDA $88 day); never near ATHs ("DO NOT BUY LEAPS NEAR ATHs"); accept 60% option drawdowns; convert at expiry (**no capital-gains tax on conversion** — the stock is acquired cheap, tax drag avoided).
- **Synthetic longs:** sell long-dated put + buy long-dated call for tiny net debit. Live examples: TSLA Jun 5 (380C/390P 2028, $40 debit, BE $420) and Jun 10 (380C/390P 2028, $34 debit, BE $414) — "throw down $30 to make $270." Short put bought back "for pennies" when deep OTM.
- **The loop ("build a bag, build a mattress"):** stock/LEAPS bag → margin collateral → sell covered calls at MR tops (20–45 DTE), sell puts at MR bottoms → income funds the next dip-buy. "The money's in the selling, not the buying."

### 3.3 Never chase — buy pre-defined dips, trim into euphoria
- Buy only on pullbacks **with confirmation**: MR oversold + Confluence buy signal + trend evidence (higher low, 200-DMA test/reclaim, ATR tier 4–5 zones, gap fills). "Don't chase. Replace."
- Trim/hedge when extended: LILO/ATR tiers 8–10, MR +2.5/+3 spikes, 9 straight green weeks → sell covered calls, take profits, raise cash. He sold PANW/RIOT/KEEL the same week his TA said "Everything Extended."
- "The real money will be made by those who buy the dips instead of chasing the vertical moves."
- Crash protocol: "Don't catch falling knives... wait for a massive high-volume capitulation wick and sideways consolidation, then deploy surgically in pre-defined buy zones." But when his level hits, he acts *into* fear: "This is a DARK STORM but that is when I NORMALLY BUY" (TSLA $390.69, Friday selloff).

### 3.4 Cash is a weapon, raised BEFORE the opportunity
Target ~10%+ buffer parked in yield (STRC at 11.5% vs T-bills); below that with markets at ATHs = "makes me nervous, will be selling positions." May–June 2026 was a masterclass: tax-bill cash crunch → $500K+ covered-call premium harvest → short oil/AVIS profits → STM sold outright at $74.25 on Jun 11 (he had planned to let the $55 covered call assign, then sold into the spike instead) → PANW $273.51 / RIOT $27.49 / KEEL $5.42 exits → sold 5/9 of his commercial real estate — all to fund the June TSLA LEAP conversion bill and SpaceX IPO orders. Counter-lesson he admitted (Rule #111): cash pressure forced bad covered-call trades on ALAB that cost him ~12% of that position — "never let cash pressure force trades you wouldn't normally make."

### 3.5 Taxes decide the trade as much as the chart
Sell decisions run through after-tax math: short-term gains at ~53% (SF) mean an AMD bought at $180 and sold at $450 must be re-bought below $306 to beat holding. LEAP conversion > LEAP sale (no tax event). Tax-free accounts trim freely; taxable accounts hedge with calls instead of selling. "If you are tax free, do it. Don't do it if you have to pay 54%."

### 3.6 Data over narrative; fade retail, follow smart money and flows
"No mon, no fun" — flows set price ($1BN into BTC ETFs ≈ +3% BTC). Follow government money (quantum funding → INFQ same-day). Trust capital allocators over X sentiment (Liquidity Summit "GO LONG ELON" vs bearish retail). Check who benefits before acting on any narrative ("follow the money behind every narrative"). Retail "capitulates at the bottom and rotates into the hot area at the top, years too late" — he treats the current BTC→AI retail rotation as exactly that, even while *he* rides AI ("ride the faster horse... if there is a big tank in crypto, IA will jump in").

### 3.7 Risk management = covered calls and discipline, not puts
Hedging is selling calls against winners (puts are "an EXPENSIVE form of insurance"). Only hedge when the optimized trend rolls over — "never jump in front of a freight train." If a hedge is run over, buy it back even at a loss. Speculative themes get a "flutter" sized to go to zero (INFQ at $14.61). Pure form always (no tokenized pre-IPO synthetics). Never lock up capital (rejected SpaceX/Anduril SPVs at 2/20 + lockups — Rule #112). Discipline beats intelligence (Rule #108); default answer to any new buy is **no**.

---

## 4. The Current Campaign (what James is actually doing RIGHT NOW)

As of June 11, 2026, every move serves one campaign: **maximum liquidity into the SpaceX IPO (June 12) + stacking TSLA under $400 + waiting for BTC capitulation.**

**Market state (June 11 close):** S&P 7,394 (+1.75%), Nasdaq 25,810 (+2.54%) after a -7.1% peak-to-trough selloff (Jun 5–10: hot jobs report, AVGO guidance miss, Iran escalation). May CPI **4.2%** (oil-driven; core 2.9%); market pricing possible Fed **hikes** (first ~Oct); 10Y 4.46%; WTI $85.84 after Iran de-escalation headlines. James's read: Fed can't control oil-driven inflation ("they only destroy demand"); peace = oil down = relief; AI deflation is the offset; stay long the trend but **don't deploy into extension** — "sniper rifles ready" for a choppy summer.

**His book (June 9 snapshot):** AI ≈ 75% — TSLA 53.5%, NVDA 6.1%, MU 3.3%, ALAB 3.2%, MRVL 2.8%, AMD 1.5%, SATS 1.4%, AVGO 1.1%, GOOG 0.9%, PLTR 0.8%, EOSE 0.7%, CPER 0.8%. Crypto ≈ 22.4% — MSTR 10.1%, BTC 5.7%, SOL 3.3%, IBIT 2%, CLSK 1.3%. Cash buffer (STRC) 8.8%.

**Active intentions he has stated:**
1. **SPCX:** all orders in at **$135** (~80% of buying power rule; expects small fills). "Retire-on bag" target: 655 shares ≈ $88K. Will NOT chase the open ("Avoid the IPO Trap"); will layer on post-IPO dips over the bumpy first ~90 days; options strategies only after it settles. Holds: cheap at $1.75T; ~$2.6T first-year ceiling ("returns paltry first year"); **$1,527/share by 2030 (11.3x)** on his $18.45T EV model. Street: Oppenheimer $190 PT, New Street $165; Polymarket implies ~$2.17T day-1 close (~+23%).
2. **TSLA:** convert the deep-ITM June LEAPS (strikes $140–175) into stock — the bill the whole cash campaign funded. Keep adding synthetic longs "the more it dips" under $400. Don't rotate TSLA into SPCX beyond a few percent — "TSLA has more upside near term." Targets: $650 in a year, split talk at $650, $500→$700 on breakout, $4.5T cap long-term.
3. **BTC:** hold, don't add — "trend still down and no buy signal yet" despite 200-WMA touch ($62K), supply-in-loss bottom signal (10.5M coins), and cheapest-4%-of-history power-law reading. **$50K = "add big time."** A reclaim with ATR buy signal = re-engage. Diminishing-returns ceiling next cycle maybe $150K.
4. **Housekeeping:** sell limits working (CLSK), STM sold at $74.25, SATS only a buy at $100 (not $120+), STRC held (breakeven <$90, bi-weekly dividends "like a salary").

---

## 5. The Ranges — what to watch RIGHT NOW (June 11, 2026)

His levels vs. June 11 closing prices. **Action column = what his system says to do at that level, not a recommendation.**

| Asset | Now (Jun 11) | His buy zone / trigger | His trim/exit zone | His targets | System action right now |
|---|---|---|---|---|---|
| **SPCX** | $135 IPO, lists Jun 12 | $135 IPO print; post-IPO dips, layered | — | Street $165–190; his $1,527 by 2030 | Take IPO fill; do NOT chase the open; layer dips over 90 days; options later |
| **TSLA** | $399.15 | **<$400 stacking zone** (higher lows); $360–380 support; synthetic-long adds ($34–40 debit, BE $414–420) | MR spike ~+2.5 → CCs (rare) | >$450 = 3rd leg; $500→$700; $650/1yr; $2,000 long-term | At/below $400 = he's a buyer. He added at $384 (Jun 10) and $390.69 (Jun 5) |
| **BTC** | $63,449 | 200-WMA $62K = good R/R *but no ATR buy signal* → **hold, don't add**; **$50K = add big** | Next-cycle ceiling ~$150K if diminishing returns persist | 12-mo EV $117.5K (range $96–139K) | Watch for capitulation wick or trend flip; 200-DMA reclaim = liftoff regime (last quoted $82.5K on May 12–13; MA is downward-sloping — recompute before setting alerts) |
| **NVDA** | $204.87 | **<$200 attractive** (alerts 200/190/185); <$190 = "absolute gift" | fails his 3x test — no adds beyond core | $282 street consensus | One MR leg down from a screaming buy; he holds 6.1% |
| **MU** | $995.87 | **$650–675 "love to be a buyer"**; 700s OK (ATR L5 ~$750) | parabolic — no chase | His $1,250/2030 ("sandbagged"); UBS $1,650; Jensen $3,000 | Far above buy zone — wait. Hold to 2028 if owned |
| **MRVL** | $280.71 | Wait for **sideways consolidation** (post +37% S&P-add spike) | — | "Next trillion-$ company" (Jensen); ~5x runway | No chase. Hold to 2028 plan if owned |
| **AVGO** | $385.57 | **$350–378 heavy support** = buy zone (long-term zone $350–380) | — | continuation to "the 500s" | ~2% above the buy zone — accumulate only on a dip to ≤$378 |
| **AMD** | $488.45 | Tier 4/5 pullback only; gap ~$350–360; "let it find the 50-day" | $455–500 = LILO 9–10 trim zone | Mizuho $615 | No chase at $488; buyer ~$350–360 (gap fill / ATR L5) or tier-4/5 pullback to the 50-day |
| **GOOG** | $356.56 | **$340–350 entry zone** (gap + 50-DMA) | $400 ATH resistance — CC strike territory | — | Above the zone, and latest call (Jun 5) is wait: uptrend broke at $380 — "let it roll over and find a bottom before jumping in" |
| **PLTR** | $131.08 | **$130 box buy**; LEAP setup: $120-strike 18-mo when <$130; deeper $100–110 | $156–160 box sell; 200-day ~$160 | break $160 opens $200 | At his buy trigger NOW — box trade active (bias caution after 200-DMA rejection) |
| **MSTR** | $120.15 | $150 was "line in the sand" — **broken** = no signal | — | $300 when BTC >$120K | Wait. BTC TA first, MSTR second. NAV premium "never coming back" |
| **SOL** | $66.79 | Added 15% at $80 (May); **$45 = deep-value panic buy**; perp-tempting at $70 | $97–100 then $110 resistance | $1,000 ≈5-yr structural-demand model | Hold; add only at capitulation or trend turn. BTC+SOL only; alts = "peanuts" |
| **STRC** | $96.49 | Scalp: **buy $98 / sell $100** (~10 days); core: yield 11.5% | — | par $100 (ATM caps upside) | Hold as the cash buffer; >4 months in = "already winning"; his BE <$90 |
| **SATS** | $128.13 | **$100 = worth a stab; $120+ = no** | — | TD Cowen $155 | Above his max entry — do nothing |
| **ARM** | — | ATR L5 ~$270 pullback; $300 "psychological" bounce | extended +75%/30d | — | No entry until pullback |
| **TSM** | — | "**A gift at $340 — take it**" | — | — | Limit-order mentality |
| **IBIT** | $36.05 | proxy for BTC rules above | — | — | Same as BTC |
| **CLSK** | $16.17 | — | **sell limits set** (his) | — | He's exiting via limits — not an add |
| **Copper (CPER)** | ~$6.50/lb spot (Jun 2 email — not in the Jun 11 snapshot) | owns since 2025 | — | **$13/lb** | Hold the edge trade |
| **S&P 500** | 7,394 | 5–10% pullbacks to 200-DMA = healthy | 9 green weeks = trim signal (was) | Yardeni 8,250 EOY; 10,000/2030 | Post-purge chop = sniper season, not risk-off |

**Standing macro triggers:** Iran/Hormuz headlines drive oil → CPI → Fed → everything (peace = buy signal for risk). June 16–17 FOMC (Warsh, ~98% hold priced). "Good news is bad news" regime — hot data = yield spike = AI-multiple compression = his buy-the-dip window.

---

## 6. Our Implementation (scaled, not cloned)

James's own member guidance, repeated constantly, is the bridge between his book and ours:

1. **Allocation:** Cap the AI theme at **15–25% of investable capital** (his number for members — he runs 75% "because this is literally my job"). Crypto sleeve: BTC + SOL only. Keep ~10% cash buffer in yield.
2. **Entry mechanics:** Split any new allocation into **4 tranches over 3–6 months**; deploy a tranche on schedule or accelerate on 10–20% pullbacks into the §5 buy zones. Never market-buy a vertical chart.
3. **Two clean paths (his words):** Path A = 3–5 highest-conviction names (from: TSLA, NVDA, MU, MRVL, AVGO, GOOGL, PLTR, ALAB + SPCX); Path B = 100+ shares of 1–2 names + monthly covered calls. **No synthetic longs/spreads until the share-level system is running profitably** — he explicitly tells members not to copy his leverage.
4. **Cadence:** Max 1–2 trades/week. Re-evaluate the basket quarterly, not daily. Set price alerts at the §5 levels and stop watching charts.
5. **Sizing language:** He publishes adds as portfolio fractions (e.g., +0.0048 TSLA). Mirror proportionally: his 0.5% add ≈ our 0.5% add.
6. **Email-driven workflow (the repo's edge):**
   - **IA Trade Alert** → same-day review: what did he do, which rule fired, does the level still exist for us?
   - **IA Portfolio (weekly)** → drift check vs. our targets.
   - **TA Summary / Weekly Edge** → refresh the §5 ranges table.
   - **Weekly Nuggets** → thesis changes (e.g., "BTC next top maybe $150K" materially changes crypto sizing).
7. **Execution boundary (updated by Samin):** autonomous execution is enabled for the assigned Alpaca `paper` profile only; every order must be logged and reported. Options are enabled when useful, including LEAPS and covered calls, but the account must never go into debt: no margin debit, naked/undefined option risk, perps, crypto perpetuals, or live trading.

---

## 7. Rules of Engagement (the distilled rulebook)

The 20 rules that govern 90% of his decisions — fuller set in [analysis/extracted/rules.md](analysis/extracted/rules.md):

1. Be in the top 0.3% of assets; own the #1; a play needs a 3x path and must beat ~14% debasement.
2. Two narratives max; never all-in on one story (AI bubble odds are non-zero).
3. Know your exit before you enter. Default answer to any buy is NO.
4. Never chase; never FOMO; don't buy at resistance — buy pre-defined levels with confirmation or wait.
5. The lower a conviction asset goes, the harder you buy ("blood in the streets") — but only after capitulation evidence, never guessing bottoms ("don't catch falling knives").
6. Trim when others FOMO: extension tiers 8–10, MR +2.5/+3 → covered calls / layered sells / raise cash.
7. LEAPS only at extremes, only on 5-year-conviction names, always convert (tax-free), never near ATHs, keep conversion margin ready.
8. Sell puts at bottoms, sell calls at tops, 20–45 DTE; buy back shorts "for pennies" when deep OTM.
9. Never jump in front of a freight train: don't hedge rising trends; buy back overrun hedges at a loss rather than losing the core position.
10. Puts are expensive insurance — hedge with covered calls instead.
11. Taxes before trades: conversion > sale; compute the re-entry break-even before any taxable sale.
12. Always keep cash (~10%+, parked in yield); raise it BEFORE the opportunity, never under panic pressure (Rule #111).
13. Trim losers ruthlessly, let winners ride (Rule #107 — conviction without courage is catastrophe).
14. Clear out dust positions; focus is the edge.
15. Speculative flutters sized to zero; in a hot theme pick the name with real revenue.
16. 80% of IPOs break price — only play the rare exception, layer in (IPO shares are non-marginable at Schwab/Fidelity: 100% settled cash required), expect a bumpy 90 days, "get on the train" at strategic valuation.
17. Rotate proxies into the real thing when it lists (STM/SATS → SPCX).
18. Follow flows and smart money; fade retail rotation; check who benefits from every narrative.
19. Never lock up capital; pure form always (no SPVs, no tokenized synthetics, no 2/20).
20. Discipline beats intelligence: boring strategy, ride the faster horse, and when the trend is down with no buy signal — hold, don't add. (For non-professionals he prescribes 1–2 trades/week max; his own alert cadence runs hotter.)

---

## 8. Immediate Action List (week of June 11–19, 2026)

1. **June 12 — SPCX lists.** If allocated at $135: hold the bag, no day-1 adds. If not allocated: do nothing at the open; define layer levels on the post-IPO dip (his framework: bumpy 90 days; $135-area re-entries are the gift scenario; Polymarket implies ~$166 day-1 close).
2. **TSLA <$400:** this IS his active buy zone (adds at $384–390 this week). Tranche entries per §6; breakout >$450 changes posture from accumulate to hold.
3. **PLTR ~$130:** the one §5 name sitting at its buy trigger right now. AVGO ($385.57) is ~2% above its $350–378 zone — alert at $378. GOOG at $356 is above its $340–350 zone and his latest call (Jun 5) is to let it find a bottom first.
4. **BTC:** no add until ATR-style buy signal / capitulation wick despite the bottom signals stacking. Alert set at **$50K (add big)** and on a 200-DMA reclaim (~$82K).
5. **FOMC June 16–17:** no deployment into the print; "good news is bad news" — a hawkish spike into his levels is the entry, not the exit.
6. **Run the autonomous monitor/manager** (GOAL.md phase 4): cron that parses new InvestAnswers emails daily → classifies (Trade Alert / Portfolio / Levels / Nuggets) → checks Alpaca portfolio and levels → places a trade only if the checklist fires → Telegram digest with the order/no-trade reason.
7. **Maintain the trade journal and check log** (`analysis/trade-journal.md`, `analysis/check-log.md`): every order/no-trade decision and every scheduled check gets logged. He endorses exactly this loop ("feed your trade journal into an AI tutor and review objectively").

---

## 9. Source Map

| Question | File |
|---|---|
| Every trade he made (87) | [analysis/extracted/trade-log.md](analysis/extracted/trade-log.md) |
| Every level by asset (235 across 54 assets) | [analysis/extracted/levels-by-asset.md](analysis/extracted/levels-by-asset.md) |
| All 182 rules with citations | [analysis/extracted/rules.md](analysis/extracted/rules.md) |
| His models (TABI, OCTA, IA13, IADSS/MR, Retire On, synthetic longs) | [analysis/extracted/research-frameworks-research.md](analysis/extracted/research-frameworks-research.md) |
| Who James is + track record + criticisms | [analysis/extracted/research-james-profile.md](analysis/extracted/research-james-profile.md) |
| Market snapshot used for §5 (Jun 11, 2026) | [analysis/extracted/research-market-levels.md](analysis/extracted/research-market-levels.md) |
| Portfolio evolution May 5 → Jun 9 | [analysis/extracted/portfolio-snapshots.md](analysis/extracted/portfolio-snapshots.md) |
| Macro views timeline | [analysis/extracted/macro-views.md](analysis/extracted/macro-views.md) |
| Psychology quotes | [analysis/extracted/notable-quotes.md](analysis/extracted/notable-quotes.md) |
| Extraction completeness audit | [analysis/extracted/audit-completeness.md](analysis/extracted/audit-completeness.md) |
| Raw structured extraction (JSON) | `analysis/extracted/raw_extracts.json` |
