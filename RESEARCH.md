# The Money What Ifs: weekly research run

Unattended weekly research for Archie's channel (YouTube @TheMoneyWhatIfs, TikTok @themoneywhatifs). Archie is not watching: don't ask questions; write findings down and report. You **do not** change the engine, the runbook or any scheduled posts. You only research, write the files below, push them, and report.

Goal: find what is getting traction in UK money / personal-finance / data short-form content right now, and turn it into (a) concrete ideas for our next videos and (b) a few ranked recommendations to improve our style.

## 0. Setup
`add_repo` owner `moneywhatifsvideos`, repo `moneywhatifs-media`, access `push`; `git clone --depth 1 https://github.com/moneywhatifsvideos/moneywhatifs-media ~/media`. Read `~/media/topics.md` (what we've made), `~/media/research/ideas.md` (the idea bank, if it exists) and the newest report in `~/media/research/`.

## 1. Our own numbers (baseline)
Metricool brand 8204403 (Europe/London). Pull the last 28 days per video: YouTube via `getAnalyticsDataByMetrics` (`YTVV17` title, `YTVV06` views, `YTVV08` average view duration, `YTVV09` likes, `YTVV11` comments, `YTVV12` shares); TikTok via `getAnalyticsAvailableMetrics` (network `tiktok`, connector `posts`) then the matching metrics. Note the top and bottom 3 videos and whether data videos or What If videos are doing better. If there is no data yet, say so.

## 2. Research (use separate agents in parallel if available, then combine)
Use WebSearch (standard, then extended where results are thin) and WebFetch on pages the searches return. You cannot watch videos; work from titles, descriptions, captions, view/like counts shown on pages, articles about trends, and creator-economy write-ups. Cover:
1. **Similar accounts and formats:** UK and global money/finance shorts that use animation, stick figures, "what if" scenarios, "UK vs USA" comparisons, data races (bar/line/map), rankings, "then vs now" prices. Starting points Archie likes: Money Stories (illustrated UK finance explainers, "UK vs USA" did best), DATA (UK data races: jobs pay, holiday destinations, Christmas costs by region), wrong.onpurpose, fammez_, Stick Motion and whatif-style channels. Find new ones too.
2. **What's working:** which topics, hook lines, title wordings, on-screen styles, lengths and series formats ("Part 1/2", recurring characters) are getting high views, saves and shares. Look for patterns, not one-offs.
3. **UK calendar for the next 3 weeks:** Budget and Spending Review dates, Bank of England decisions, ONS releases (inflation, wages, house prices), price cap changes (Ofgem), tax year deadlines, Black Friday, Christmas, January sales, Blue Monday, payday, student finance dates. These make timely data and What If topics.
4. **Data sources** for data videos: official, fetchable sources (ONS, HM Land Registry, Bank of England, gov.uk, Ofgem, HMRC, OBR, UK Finance) with long time series that would make good bar or line races.

## 3. Write the files
1. `~/media/research/YYYY-MM-DD.md` (today's date), short and scannable:
   - **Our numbers:** top/bottom 3, data vs What If.
   - **What's working out there:** 5–8 bullet findings, each with the example accounts or videos and links.
   - **Recommendations:** 3–5 ranked changes to our style or approach (hooks, titles, visuals, pacing, formats, series, posting), each with why (evidence), expected impact, and effort. Mark each "PROPOSED". Never mark anything approved yourself.
   - **Sources:** links.
2. `~/media/research/ideas.md`, the rolling idea bank (create if missing). Two sections, **Data video ideas** and **What If ideas**. Add 8–12 new ideas per section per week, each one line: the title/question, the hook, the twist or reveal, why it should work (trend/evidence), and for data ideas the exact official source and years available. Don't duplicate topics.md or existing ideas. Keep at most about 60 open ideas; delete the weakest ones beyond that. Leave ideas marked USED alone.
3. Commit with message "Weekly research YYYY-MM-DD" and `git -c push.negotiate=true push`.

## 4. Report to Archie
One short message (SendUserMessage; PushNotification too if available):
- our numbers in one line;
- the 3 best findings;
- the ranked recommendations, each one line, with: "Reply 'approve 1, 3' in the chat to adopt any of these."
- how many new ideas were added to the idea bank.

## 5. When Archie replies (same session, after the report)
If Archie replies approving recommendations (e.g. "approve 1, 3"):
1. Mark those items `APPROVED by Archie (date)` in the dated report; mark others `NOT APPROVED` only if he says so.
2. Changes to topics, titles, hooks, script structure or posting are applied by the next Sunday production run (it follows APPROVED items). Nothing else to do.
3. Changes that need the engine (visual style, new template, animation) : make them now in `~/media/engine/mwi.py`, keep old specs working, test by rendering one existing spec with `--stills` and one full render, look at the frames, then commit and push. Tell Archie what changed and send the test video.
4. Commit and push.

## Standing decisions (do not re-propose)
- Posting times: already being tested by alternating data/What If between 10:00 and 16:00 (approved 19 Nov 2026). Don't propose other time tests until the channel has about 1,000 followers.
- Minimum length: every video is at least 63 seconds (TikTok Creator Rewards needs over 1 minute).
