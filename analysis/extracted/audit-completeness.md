Spot-check complete — I read 10 emails in depth (2 portfolio, the LEAPS/cash-raising email, both TA emails, the tax email, the LEAPS-coming-due email, Weekly Nuggets, and all 13 trade-alert bodies). Final report:

# Completeness Critic Report — InvestAnswers Corpus (345 emails, May 5–Jun 11 2026)

## Verified counts

**(a) 13 IA Trade Alerts — CONFIRMED.** All 13 exist by filename and all contain real trades: 05-06 (AMD 6/18 $420C sold @$40), 05-12 (covered half AMD hedge @$42), 05-20 Delayed (bought back ALAB Jun-5 $225C @~$51), 05-21 (INFQ entry $14.61), 05-26 (covered GOOG $385C: sold $15–16, bought back $9), 05-29 ×3 (PANW sold $273.51, RIOT $27.49, KEEL $5.42), 06-05 ×2 (closed ALAB short calls; TSLA synthetic long @$390.69 — 380C/390P, 924 DTE, $40 debit, BE $420), 06-08 (Real Estate Liquidity — sold 5/9 of commercial RE), 06-10 (TSLA add @$384, $34 debit, BE $414), 06-11 (STM sold $74.25 → rotating into SPCX). Note: two bodies sit at different line offsets (May 12, May 20) — easy for a naive extractor to read as empty.

**(b) 6 portfolio snapshots — CONFIRMED** (May 12, May 15 "Portfolio Mgt Time", May 19, May 26, Jun 2, Jun 9). **Major caveat:** the May 12 allocation table is an *image* — text contains only commentary (TSLA >51%, crypto 28%). Jun 9 has the full text table (TSLA 53.5%, AI ≈75%, crypto 22.4%, line-item %s). If extraction was text-only, the May 12 (and possibly other) snapshots are partial.

**(c) TA/Weekly Edge — only 2 such emails exist** (May 16 Recap, May 30 TA Summary/TAlpha), each carrying ~20–25 levels (ALAB $264/$300, PLTR $129/$100/$160/$200, GOOGL $400/$350/340–350, MU ~$625/~$750, ARM $220–230/$180/~$160, NVDA 200/190/185, TSLA 450/400, BTC 70–75k, SOL 90/97–100, MSTR ~150, S&P 7,500, oil ~87, AVGO 500s). 235 total levels corpus-wide is plausible — these two alone hold ~45.

## What the four categories (trades/levels/rules/frameworks) MISS entirely

1. **The cash-raising campaign as a timeline** — the single most important narrative arc: out of cash (May 6) → aggressive covered calls + oil/Avis shorts (May 15) → STM called away at $55 → PANW/RIOT/KEEL liquidations (May 29) → 5/9 of commercial real estate sold (Jun 8) → STM sold (Jun 11), all driven by the **June 12 TSLA LEAP conversion bill** and SPCX IPO allocation. Individual trades get captured; the causal campaign does not.
2. **Standing options book / structure inventory** — TSLA LEAPS strike ladder (140/150/160/175 + 220s Dec 2027/28 + 300s Dec 2028), expiry schedule (Jun & Dec 2026), the "mattress" concept (exercise → cash cushion → sell puts), and which hedges are open at any moment (AMD half, ALAB half, GOOG, STM). A trade-event list loses position state.
3. **Tax intelligence** — "convert a LEAP = no capital-gains tax," the 53% short-term SF rate math, re-entry break-even concept (sell AMD $450 → must re-enter <$306), and the **Google Sheets tax decision-maker model link** (05-08 email). The April tax bill that caused the whole cash crunch.
4. **SPCX IPO event thread** — $1.75T valuation, orders placed at $135, allocation scarcity anecdotes, 2030 target $1,527/share (11.3x), $920M/month GOOGL compute deal, SATS-as-proxy rule ($100 yes / $120 no).
5. **Catalyst calendar & analyst data** — NVDA earnings May 20, PANW earnings Jun 2, PANW PT raises (Benchmark $270 / Wedbush $300 / BTIG $268), TSLA >$650-by-August stock-split speculation.
6. **Precise position-sizing fractions** (RIOT = 0.00375 of portfolio, TSLA add = 0.00484) and allocation deltas between snapshots — not "price levels."
7. **Image-embedded data** — May 12 portfolio table and TA chart screenshots are unrecoverable from text_md at all.

## 5 most strategically important emails

1. `2026-05-15_003625_Portfolio-Mgt-Time....-LEAPS-Conversions-and-Raising-Cash_19e29102fc109150_f53c4b19.md` — the Rosetta stone for a month of trades: LEAPS conversion math, cash crunch origin, every cash-raising lever.
2. `2026-06-09_144052_IA-Portfolio-June-9-2026_19eacd454f75fa8e_e34a308f.md` — fullest text-readable portfolio table + hedge status + forward plan (SPCX, CLSK limits, STM call-away).
3. `2026-05-30_022159_TA-Summary-The-Weekly-Edge-TAlpha-May-2529-2026-Everything-Extended_19e76b038638942c_1205a8af.md` — densest level map + semis→SaaS rotation thesis + trades noted.
4. `2026-06-11_174602_IA-Weekly-Nuggets-June-2-11-2026_19eb7ca8d20e9a1e_0edf20df.md` — SPCX IPO playbook, BTC-vs-AI rotation thesis, TSLA $650 target, STRC breakeven <$90.
5. `2026-05-08_013352_IA-Capital-Gains-Tax-Decision-Maker-to-sell-or-not-to-sell_19e05384112264fc_6a2c6d22.md` — the reusable tax model (with live spreadsheet link) that governs every sell decision in the corpus.

Directory: `/Users/saminmacmini/Projects/investanswers-email-strategy/emails/text_md`