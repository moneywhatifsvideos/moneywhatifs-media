# Idea bank (rolling)

Each idea gives the title, the hook, the twist or reveal, why it should work, and (for data ideas) the source. Production runs mark an idea **USED (date)** when they make it. Keep about 60 open ideas at most. Trending ideas carry a "use by" date; delete them once it has passed.

Added 21 Nov 2026 unless stated; the "Added 28 Nov" blocks come from research/2026-11-28.md. Facts come from this week's report (research/2026-11-21.md). Check every figure against the source before scripting.

## Data video ideas

1. **Is your pay rise beating prices? Pay vs prices, 2000–2026** (line race)
   - Hook: "Your pay rise this year was worth 0.4%."
   - Reveal: the years when prices beat pay.
   - Why: real pay is in the news (ONS, 17 Nov), and it's a "how do you compare" angle.
   - Source: ONS EARN01 average weekly earnings (2000–2026, XLS) plus ONS CPI annual rate series D7G7 (1989–2026).
2. **What a 55-litre tank of petrol cost, 2003–2026** (line race)
   - Hook: "Filling up used to cost £__."
   - Reveal: fuel is up 33% in a year (ONS CPI, Oct 2026).
   - Why: petrol is the top inflation story now.
   - Source: DESNZ weekly road fuel prices CSVs (2003–2017 and 2018–2026).
3. **Your energy bill 2019–2027: every price cap** (bar race)
   - Hook: "Your bill in 2019 vs January."
   - Reveal: the 2022 spike, then the new January jump.
   - Why: Ofgem announces the new cap on 25 Nov.
   - Source: Ofgem price cap levels, Q1 2019 to Q1 2027 (one PDF or XLSX per period; gather by hand).
4. **Top 10 best-paid jobs in the UK, 2026** (bar ranking)
   - Hook: "Where does your job rank?"
   - Reveal: the median full-time salary is just £40,911.
   - Why: "where do you rank" is the biggest UK money pattern (Damien 831K).
   - Source: ONS ASHE 2026, Table 14 by occupation (XLSX, published 22 Oct 2026).
5. **How much you need to earn to be in the UK's top 10%, 1%…** (bar ranking of pay by percentile)
   - Hook: "Top 10% starts lower than you think."
   - Reveal: the gap between the top 10% and the top 1%.
   - Why: British Finance with Jack's "Top 10% in the UK" got 56K views.
   - Source: ONS ASHE 2026 percentile tables (XLSX).
6. **Minimum wage: £3.60 to £13.21** USED (22 Nov 2026) (line race, 1999–2027)
   - Hook: "Your first job paid __ an hour."
   - Reveal: pay roughly 3.7x, compared with what prices did over the same years.
   - Why: the April 2027 rate was set at the Budget; nostalgia plus comparing yourself.
   - Source: Low Pay Commission reports (rates since 1999, PDF; take the tables by hand).
7. **Mortgage rates vs savings rates since 1995** (two-line race)
   - Hook: "The bank pays you __ and charges you __."
   - Reveal: the gap during the 2008–2021 low-rate years.
   - Why: rates rose in November, and Moneyfacts says 7 in 10 providers didn't pass it on.
   - Source: Bank of England Bankstats G1.3 quoted household rates (mostly 1995 onwards, Interactive Database).
8. **First-time buyer house prices by region** (bar race)
   - Hook: "Your first home cost __ in 2005."
   - Reveal: where first-time buyers got priced out the fastest.
   - Why: a different angle to D02, which covered all buyers. First Time Buyer ISA news.
   - Source: HM Land Registry UK HPI First-Time-Buyer CSV files (from 1995; Scotland from 2004, Northern Ireland from 2005).
9. **Where the taxman's money comes from: income tax vs VAT vs fuel duty** (bar race)
   - Hook: "Guess the UK's biggest tax."
   - Reveal: how far income tax pulls ahead of the rest.
   - Why: the tax burden is about to hit a record (OBR).
   - Source: HMRC tax and NICs receipts, NS_Table.ods (check how many years it covers).
10. **What £100 from 1989 buys today** USED (22 Nov 2026) (shrinking-banknote line race)
    - Hook: "Your £100 has been shrinking for 37 years."
    - Reveal: how much it's worth today.
    - Why: then-vs-now posts go viral (Full Fact, Jan 2026), and ours is sourced.
    - Source: ONS CPI annual rate D7G7 (1989–2026), compounded.

### Added 28 Nov 2026
11. **The price of a pint, 1987–2026** (line race) · Hook: "Your dad's pint cost __p." · Reveal: how far the pint outran pay. · Why: sourced then-vs-now (Full Fact shows the unsourced ones go viral and get things wrong). · Source: ONS RPI average price CZMT (pint of bitter, 1987–2022; superseded series, so use the corrected version it links to) plus the ONS Shopping Prices Comparison Tool (2020–now).
12. **Christmas dinner price race, 2020–2026** (bar race: turkey, sprouts, mince pies, pudding) · Hook: "Christmas dinner just got how much dearer?" · Reveal: the item that rose the most. · Why: seasonal, and everyone has a personal stake. · Source: ONS Shopping Prices Comparison Tool, monthly item prices 2020–now ("download all data"). Use by 24 Dec.
13. **Where rents rose most, by region, 2005–2025** (bar race) · Hook: "Renting in your area: up how much?" · Reveal: the region where rent outran house prices. · Why: our housing videos are the TikTok winners (G06 888 views; D02 "where do you live" was the best data video). · Source: ONS PIPR historical series (Jan 2005–Feb 2025) plus the current PIPR.
14. **Council tax since 1993: £__ to £__** (line race, England average Band D) · Hook: "Your council tax has tripled. Did your bins?" · Reveal: the multiple, compared with CPI. · Why: the £100 band A–D payment arrives in January. · Source: MHCLG Live Tables on Council Tax (1993-94 to 2026-27).
15. **Top 10 most expensive council tax areas, 2026-27** (bar ranking) · Hook: "Where does your council rank?" · Reveal: the cheapest area, probably a surprise. · Why: a local "where do you rank" angle. · Source: MHCLG Live Tables, Band D by local authority, 2026-27.
16. **What Brits spend money on: 2001 vs 2025** (bar ranking shift: housing, food, transport, recreation) · Hook: "Where your money goes now vs 2001." · Reveal: housing and energy jump up the list. · Why: "the average person" titles are the top finance outlier (OutlierKit: 120x, 1.4M). · Source: ONS Family Spending workbook 1 (FYE 2001 to FYE 2025).
17. **Median wealth by age: where do you rank?** (bar ranking, ages 16–24 to 75+) · Hook: "The average 30-something is worth __." · Reveal: the gap between median and mean, and how much of it is pensions and property. · Why: Damien's "by age" got 831K; "every level" titles 1.1M. · Source: ONS Wealth and Assets Survey ad-hoc 2813 (Apr 2020–Mar 2022).
18. **Student loans owed in England: the total, year by year** (line race) · Hook: "Graduates owe £__ billion." · Reveal: the share that will never be repaid. · Why: new student loan rules (Lifelong Learning Entitlement) start 1 Jan 2027. · Source: SLC "Student loans in England" annual editions (FY 2025-26 and earlier).
19. **330 years of interest rates: is 4% actually high?** (line race) · Hook: "Rates went UP. Is that bad?" · Reveal: 4% is roughly the long-run normal; 0.1% was the odd one out. · Why: Bank Rate is 4.00% and a 17 Dec rise is priced in. · Source: BoE Millennium of Macroeconomic Data v3.1 (to 2016) plus BoE Bank Rate database (1694–now).
20. **The price of a first-class stamp, 1971–2026** (line race) · Hook: "Posting a Christmas card cost __p in 1971." · Reveal: the multiple, compared with CPI. · Why: last posting dates are 18–23 Dec; nostalgia. · Source: ChannelX historic stamp prices 1971–2019 (unofficial; check against Royal Mail) plus today's £1.80 from press reports (check it). Use by 21 Dec.

## What If ideas

1. **What if you had to live on the state pension?** USED (22 Nov 2026)
   - Hook: "£250.70 a week. Go."
   - Reveal: rent plus energy plus food leaves £__.
   - Why: the April 2027 rate was just confirmed. Relatable for parents and grandparents.
2. **What if you kept £50,000 in savings outside an ISA after April?**
   - Hook: "The Budget just put a new tax on your savings."
   - Reveal: you'd pay 24% of the interest in tax, compared with £0 in an ISA.
   - Why: a real 28 Oct Budget change that few people have noticed.
3. **What if petrol hit £3 a litre?** USED (22 Nov 2026)
   - Hook: "Fuel is up a third in a year…"
   - Reveal: what that does to a commute, and to food prices.
   - Why: CPI motor fuel is +33.2%.
4. **What if you moved your exact UK job to the USA?**
   - Hook: "Is £30K a good salary? Americans can't believe it."
   - Reveal: what's left after healthcare and rent.
   - Why: UK vs USA is a repeat viral hook (LADbible; Money Stories' best format).
5. **What if prices were still 2000 prices, but you earned today's pay?**
   - Hook: "Freddo 10p, pint £1.90…"
   - Reveal: the fact-checked version: pay rose about 110% (Full Fact).
   - Why: then-vs-now goes viral, and correcting the wrong numbers is the twist.
6. **What if inflation went negative?**
   - Hook: "Prices fall every month. Sounds great?"
   - Reveal: spending stops, then jobs go.
   - Why: Explains101's version got 623K.
7. **What if the UK just printed £1 trillion?**
   - Hook: "Why not just print it?"
   - Reveal: inflation eats it (link to our £1M everyone video).
   - Why: Explains101's version got 1.0M.
8. **What if you overpaid your mortgage by £200 a month?** USED (22 Nov 2026)
   - Hook: "Mortgage-free 8 years early?"
   - Reveal: interest saved, compared with investing the same £200.
   - Why: the POV "pay off your house" video got 244K.
9. **What if you kept the same car for 10 years vs swapping every 3?**
   - Hook: "Two neighbours, two drives."
   - Reveal: the £ gap after 10 years.
   - Why: "POV: You Keep the Same Car for 10 Years" got 220K.

### Added 28 Nov 2026
11. **What if mortgage rates hit 7%?** · Hook: "Rates went up last month… and again in December?" · Reveal: the monthly payment on a £200k, 25-year mortgage at 4%, 5.5% and 7%. · Why: housing and debt shocks are our two best TikToks (888 and 485 views); a 17 Dec hike is priced in; 2-year fixes are at 5.5–6%.
12. **What if UK house prices fell 10% next year?** (distinct from "halve") · Hook: "Prices are already falling." · Reveal: a 2025 buyer with a 10% deposit has £0 equity. · Why: Lloyds −1.2% year on year, the biggest fall since 2023; Rightmove −1.8% in a month.
13. **What if your 1.5% fix ended this month?** · Hook: "Your 2021 mortgage deal just ran out." · Reveal: the payment jump at 5.5%, a year at a time. · Why: payment-shock stories about your own home are our best-performing theme.
14. **What if you paid for Christmas with Buy Now Pay Later?** · Hook: "14% of us will. 22% of Millennials." · Reveal: three "pay in 3"s stack into January, the 42-day month. · Why: IPA data; the debt-trap angle (G05 got 485).
15. **What if you took a 40-year mortgage instead of 25?** · Hook: "Lower payments. What's the catch?" · Reveal: the extra interest paid. · Why: affordability is squeezed by 5.5–6% rates; housing and debt combined.
16. **What if you rented forever instead of buying?** · Hook: "Two friends, same pay. One rents, one buys." · Reveal: the pot at 65 under realistic rent rises. · Why: ONS rents data; housing is our winner; it also pilots the two-character format.
17. **What if your UK salary came with US healthcare bills?** · Hook: "Americans can't believe our £30K." · Reveal: what's left after US insurance and deductibles. · Why: UK vs USA is Money Stories' best format, and comes back on LADbible regularly.
18. **What if you earned the UK minimum wage in the USA?** · Hook: "£13.21 an hour from April vs $__." · Reveal: the federal minimum (check the current figure) against the UK's. · Why: UK vs USA plus the Budget minimum wage rise.
19. **What if you'd saved for a deposit in the new First Time Buyer ISA?** · Hook: "The government adds 25%." · Reveal: £4K a year becomes £__ after 5 years (bonus on up to £4K; starts 2029; check details). · Why: Budget news; ties to G19 (deposit) from a new angle.
20. **Two flatmates, same salary — Part 1** (series pilot) · Hook: "Same job. Same pay. £100K apart at 50." · Reveal: Part 1 shows only the first fork (rent vs buy, or car vs ISA), with "Part 2 tomorrow". · Why: Stickify's Part 2 got 429K; YouTube Shorts Series plays episodes in order; Sketchinance's long version flopped (828 views), so the short, numbered form is the test.

## Money mindset ideas

1. **Average UK savings by age: where do you rank?**
   - Hook: "Most 30-year-olds have less than you think."
   - Reveal: the median is far below the mean.
   - Why: Damien's version got 831K.
   - Source to verify next run: ONS Wealth and Assets Survey.
2. **POV: You became the rich friend** (start of the POV series)
   - Hook: "Same school, same pay…"
   - Reveal: one habit, compounded.
   - Why: Money Life POV's version got 344K.
3. **Why everything changes after your first £20,000 saved**
   - Hook: "The first £20K is the hardest."
   - Reveal: compound growth starts to do the work, and it's a full ISA allowance.
   - Why: British Finance with Jack's version got 138K.
4. **Your pay rise is worth 0.4%** USED (22 Nov 2026)
   - Hook: "You got a raise. You're not richer."
   - Reveal: real wages explained in 60 seconds.
   - Why: ONS, 17 Nov.
5. **Christmas costs 54% of a month's pay** USED (22 Nov 2026)
   - Hook: "The average family spends £1,681 on Christmas."
   - Reveal: "the January you" after Christmas.
   - Why: MoneySuperMarket figure; very seasonal.
   - Use by: 24 Dec.
6. **The emergency fund number for UK life**
   - Hook: "How long could you last if your pay stopped tomorrow?"
   - Reveal: 3 months of average bills is £__.
   - Why: OutlierKit flags "emergency fund" as a rising topic (18x).
7. **Signs you're doing better financially than you think**
   - Hook: "If you do 3 of these, you're ahead of most Brits."
   - Reveal: the median salary is £40,911 (ONS ASHE).
   - Why: Damien's "Signs You're Doing Well Financially" got 1.2M.

### Added 28 Nov 2026
8. **Your Christmas at every salary level (£15K to £150K)** · Hook: "On £15K, Christmas looks like this…" · Reveal: £647 is a different share of pay at each level. · Why: Dark Ledger's "Your Life at Every Salary Level" got 300K and "Every Level of Wealth" 1.1M. Use by 24 Dec.
9. **10 shocking money stats about the average Brit (2026)** · Hook: "Number 1: 55% of us started this year in debt." · Reveal: rapid-fire, each stat sourced on screen. · Why: OutlierKit's top finance outlier type (120x; Humphrey Yang 1.4M).
10. **How the bank treats you at every savings level (£0 to £1M)** · Hook: "At £0 they charge you. At £1M they call you." · Reveal: overdraft fees, then the FSCS £85K limit (check the current limit), then private banking. · Why: Dark Ledger's version got 1.1M.
11. **POV: You're the only one in the family not in debt this January** · Hook: "55% of Brits started 2026 in debt." · Reveal: one habit, saving £12.44 a week from February. · Why: POV Finance 667K / 369K; Confused.com stat.
12. **POV: You chose being rich over looking rich** · Hook: "Same street. One has the new car." · Reveal: the PCP payments over 10 years vs an ISA. · Why: POV Finance's "Chose Wealth Over Looking Rich" got 369K.
13. **The gift budget by age: who's the most generous?** · Hook: "18–24s spend £87. Who spends most?" · Reveal: 45–54s at £119; 36% are cutting back. · Why: Nationwide's 9 Nov data; "by age" comparison hook. Use by 20 Dec.
14. **The January you: 29% take over a month to recover from Christmas** · Hook: "It's not the 25th that hurts. It's 31 Jan." · Reveal: £647 against the 42-day month. · Why: Confused.com data; post in the first week of January.

## Trending ideas

1. **Energy price cap: what January's bill means for you** (use by 5 Jan; updated 28 Nov)
   - Hook: "Your heating bill just jumped £443."
   - Reveal: £1,723 to £2,166 a year (+26%), about £37 a month more; electricity 26.32p to 32.69p/kWh, gas 7.97p to 10.96p. Then: "what if you'd fixed?"
   - Why: Ofgem announced on 25 Nov (per news reports; check Ofgem's page before scripting). It starts 1 Jan and is the third rise in a row.
2. **£235 every Black Friday since 2010, invested instead** USED (22 Nov 2026) (use by 30 Nov)
   - Hook: "The average shopper spends £235 this week."
   - Reveal: the pot today.
   - Why: PwC forecasts £6.6bn of spending, the highest since 2022.
4. **The long wait: November payday to January** USED (22 Nov 2026) (use by 30 Nov)
   - Hook: "Paid early in December? Your money has to last about 40 days."
   - Reveal: daily budget maths.
   - Why: most people are paid on the last working day (30 Nov), and December pay often comes early.
5. **Will the Bank of England raise rates again on 17 Dec?** (use by 18 Dec)
   - Hook: "Rates went UP last month…"
   - Reveal: what +0.25% costs on a £200k mortgage, and what it pays a saver.
   - Why: Bank Rate is 4% after the first rise in 3+ years.
6. **Petrol vs food: November inflation** (use by 20 Dec)
   - Hook: "Petrol is up a third, food is barely moving."
   - Reveal: the new CPI figure on 16 Dec.
   - Why: CPI is the monthly news peg.
7. **Your savings interest gets taxed more from April** (use by 31 Dec)
   - Hook: "The Budget change nobody noticed."
   - Reveal: 20% becomes 24%, so use your ISA before April.
   - Why: a Budget 28 Oct change.
8. **The £100 council tax payment: who gets it and what it buys** (use by 31 Jan)
   - Hook: "Free £100 from January?"
   - Reveal: bands A–D only, paid by councils from January, against a £443 cap rise (so £100 covers about 23% of it). Updated 28 Nov.
   - Why: Budget measure, paid from January 2027.

### Added 28 Nov 2026
9. **Black Friday: record £1.3bn online, high streets −14%** (use by 3 Dec) · Hook: "We spent a record… just not in the shops." · Reveal: phones made 62% of the spending; the average discount was only 18%. · Why: Adobe and MRI data published 28 Nov.
10. **House prices are falling: good news or bad?** (use by 10 Dec) · Hook: "The biggest fall since 2023." · Reveal: a buyer saves £__, but on a 5.5% fix the monthly cost is still up. · Why: Lloyds HPI −1.2% year on year; Nationwide Nov HPI due about 1 Dec (confirm).
11. **The £10 Christmas Bonus has been £10 since 1972** (use by 13 Dec) · Hook: "Pensioners get £10 for Christmas. Since 1972." · Reveal: worth about £__ today in 1972 money (CPI). · Why: the qualifying week is 7–13 Dec; check the details on gov.uk before scripting.
12. **"He wanna pay full price": stick figure pays for Christmas** (use by 15 Dec) · Hook: the trending SNL audio. · Reveal: the real price of a Christmas dinner, or a gift at full price vs on sale. · Why: 284 creators in 7 days, top example 1.4M (virlo.ai). TikTok only; check the sound is licensed for business use.
13. **What a 0.25% rate rise costs you on 17 Dec** (use by 19 Dec) · Hook: "4% to 4.25%. So what?" · Reveal: +£__ a month on a £200k tracker, +£__ a year on £10K saved. · Why: markets price a December hike; post the morning of the decision. Pairs with Trending 5.
14. **Missed the last posting date? What Christmas delivery really costs** (use by 21 Dec) · Hook: "2nd Class deadline: 18 Dec." · Reveal: the cost of a 2nd class stamp vs Special Delivery for the same card. · Why: Royal Mail dates; a practical search topic.
15. **Christmas dinner at January's energy prices** (use by 24 Dec) · Hook: "Your oven on Christmas Day, priced at 32.69p a unit." · Reveal: the cost of the full cook, now vs at the new cap. · Why: the £2,166 cap and seasonal timing.
16. **New student loans from 1 January: a 40-year debt** (use by 10 Jan) · Hook: "Starting a course in January? New loan rules." · Reveal: £25K repayment threshold, written off after 40 years; the total repaid on an average salary. · Why: the Lifelong Learning Entitlement starts 1 Jan 2027 (gov.uk).
