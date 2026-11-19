# The Money What Ifs: weekly production run

This is the full procedure for the unattended weekly run. Follow it top to bottom. Archie is not watching: never stop to ask questions. Make sensible decisions, note them in the report, and keep going. Only stop early if something would publish wrong or harmful content.

Channel: YouTube @TheMoneyWhatIfs and TikTok @themoneywhatifs, both linked to **Metricool brand 8204403** (timezone Europe/London).
Output: **two videos per day for the next 7 days** (Mon to Sun after the run), posted to YouTube Shorts and TikTok:
- **10:00 = a "Money Data" video** (animated real UK data: map race, bar race or line race; music only, no voice).
- **16:00 = a "What If" video** (narrated stick-figure scenario).
This split is a two-week test that started 24 Nov 2026. From 8 Dec 2026, the analyst decides the mix: if one format clearly wins on views and watch time, give it more slots (but keep at least 2 of the other per week).

Hard rules:
- Never spend Higgsfield credits or any money.
- Every number is computed in Python or taken from a source found this run. Never from memory.
- Topics from other creators are fine as **inspiration only**. Never copy their scripts, wording, characters, visuals, music or titles. Every video must be an original script with our own UK angle and twist.
- No claims about real private individuals; no named companies portrayed negatively; no investment recommendations ("not financial advice" footnote on anything showing returns).
- YouTube: madeForKids false, isAiGeneratedContent false (cartoon). TikTok: isAigc true for What If videos (AI voice); false for data videos (no AI voice).
- Data videos use **real published figures only**. Only show years/points that exist in the source; never invent in-between data points or fill gaps; mark missing areas as "NO DATA".

## 0. Set up the workspace

1. `add_repo` owner `moneywhatifsvideos`, repo `moneywhatifs-media`, access `push`. Clone it: `git clone --depth 1 https://github.com/moneywhatifsvideos/moneywhatifs-media ~/media`. The engine is `~/media/engine/mwi.py`; past specs are in `~/media/engine/specs/`; `~/media/topics.md` lists topics already made.
2. Voice model and packages:
```bash
mkdir -p ~/kokoro && cd ~/kokoro
curl -sSL -o voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
curl -sSL -o kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
pip install --break-system-packages -q kokoro-onnx soundfile pillow numpy
export MWI_TTS_DIR=~/kokoro
```
3. Fonts: the engine needs Poppins Bold and Medium at `/usr/share/fonts/truetype/google-fonts/`. If missing, download `Poppins-Bold.ttf` and `Poppins-Medium.ttf` from `https://github.com/google/fonts/raw/main/ofl/poppins/` and fix the FB/FM paths at the top of mwi.py.
4. Check ffmpeg exists.

## 1. Find the free slots

Metricool `getScheduledPosts` (brandId 8204403, timezone Europe/London) for the 7 days after today. Each day has two slots: 10:00 (data) and 16:00 (What If). A slot is taken if any post is already there. Make one data video per free 10:00 slot and one What If per free 16:00 slot (normally 7 + 7).

## 2. Analyst: what is working

1. Metricool `getAnalyticsDataByMetrics` for the last 28 days, YouTube per-video: `YTVV17` title, `YTVV06` views, `YTVV08` average view duration, `YTVV09` likes, `YTVV11` comments, `YTVV12` shares. For TikTok, call `getAnalyticsAvailableMetrics` with network `tiktok` and connector `posts`, then pull views, likes, comments, shares, average watch time per post.
2. Rank videos by views and by average view duration as a share of length. Note which topic types (see topics.md) and which hook shapes did best and worst. If there is no data yet, say so and fall back to an even mix.
3. Write the findings to `~/media/analytics/YYYY-MM-DD.md` (short: top 3, bottom 3, patterns, what to do more/less of).

## 3. Trend scout (separate agent)

Spawn a separate agent (Agent tool) with this brief: find what money and personal-finance topics are popular **right now** with UK short-form audiences. Use WebSearch (standard first, extended if thin) for things like: viral money "what if" shorts and TikToks, popular personal finance shorts in the UK, trending questions on r/UKPersonalFinance, this week's UK money news (Budget, Bank of England, prices, wages, house prices, energy bills, student loans, tax changes). Return **25 candidate topics**, each with: the question in one line, why it is popular (with source URLs), and a suggested twist. Topics only, no scripts copied.

## 4. Choose the topics

Pick What If topics for the free 16:00 slots (data topics are chosen in step 5b):
- none already in topics.md (a clearly different angle on a theme is fine);
- weighted towards the analyst's winning types and hook shapes, but always a mix: savings/compounding, either/or choices, absurd-but-concrete numbers, debt traps, "what if the government/economy…", everyday prices;
- at least 3 tied to this week's UK news when the scout found good ones;
- each must have a real twist (something most viewers get wrong).

## 5. Writer: scripts as spec files

Write one spec per video into `~/media/engine/specs/NN_short_name.json`, numbering on from the highest existing number. Follow the format of the existing specs exactly (read two recent ones first, e.g. 09 and 10). Rules:
- **Voice:** `"voice": "af_heart"` and `"speed": 0.92` (Archie's chosen voice, Nov 2026). The engine polishes the audio automatically.
- **Title banner:** `"banner": {"text": "<the title without emoji>"}`. The engine keeps it on screen above every scene after the hook (the scene is shrunk to fit under it).
- **Hook (most important, from analytics):** scene 0 states the full claim on screen in the first frame: key items `"at": 0`, static text (never a counter counting up from £0 in the hook). First voice line is one sentence of at most about 15 words that says the claim itself. Best hook shapes so far: clear either/or, absurd-but-concrete number, relatable trap.
- 8–9 scenes: hook, relatable setup, first result, mechanism, escalating numbers (DAY/AGE HUD, counters, chart), payoff number, twist, lesson, A/B question.
- 165–185 spoken words so the video is **61–70 seconds**. Numbers as words in voice lines, digits on screen.
- Compute every number in Python first; take current facts (prices, rates, tax bands) from sources found this run and name the source in the spec's `footnote`. Footnote "Not financial advice." on anything showing returns or debt.
- On-screen text: no →, ✈ or emoji (Poppins lacks them). £ × % ≠ = are fine.
- Templates, fields, moods, icons and chart kinds: see the docstring and TEMPLATES in mwi.py and the existing specs. `chart` series kinds: annuity, linear, decay (negative r = lump-sum growth), points.
- Also write, per video: YouTube/TikTok **title** (question + one emoji), **description** (hook line, "Comment A or B 👇", footnote, 4–5 hashtags, no #shorts), and 6 tags. Keep these in a `posts.json` in the run folder.

## 5b. Data videos (10:00 slots)

For each free 10:00 slot, make one data video spec in `~/media/engine/specs/DNN_short_name.json` (numbering on from the highest D-number). Read `engine/specs/D01_house_prices_by_region.json` first: it is the reference example.

1. **Pick a data topic** people in the UK care about and will want to compare or argue about in the comments: house prices or rents by region, wages by job or region, what things cost then vs now (bread, pint, petrol, energy bills, train fares, tuition), inflation, interest rates, savings rates, council tax by region, Christmas spending by region, UK vs USA comparisons, wealth or pay gaps by age. Use the trend scout's ideas and this week's news. Not already in topics.md.
2. **Get the real numbers.** Use WebSearch to find an official source (ONS, HM Land Registry, Bank of England, gov.uk, OBR, HMRC, Ofgem, UK Finance) and read the values with WebFetch (it can read CSV files and tables from URLs found by WebSearch; use its `offset` to page through long files). The shell cannot download from most of these sites. GitHub-hosted datasets are fine. Record every value with its source URL in `~/media/data/DNN_short_name.md`. If you cannot get a complete, sourced dataset, pick another topic.
3. **Choose a template. Use the fast, light "DATA-style" templates** (Archie found the slow map style too slow, 19 Nov 2026): constant motion, about 1.2–1.6 seconds per year, big year counter, light chart background. Reference examples: `D02_most_expensive_regions.json` (bar race) and `D03_rates_vs_inflation.json` (line race). Add `"light": true` and `"footnote_y": 1640` at the top level.
   - `bar_race2` (like "Which job pays the most in the UK?"): up to 11 items re-ranking every year. Fields: `years`, `items_data` [{name, label, values (one per year, null if missing), color [r,g,b]}], `prefix`/`suffix`/`decimals`, `spy` (seconds per year, 1.2–1.6), `lead`, `tail`, `top` 410, `row` 98, `year_y` 1530, `subtitle`. Best with 20–40 years of annual data where the order changes.
   - `line_race2` (like "Where do people in the UK go on holiday?"): 2–6 lines drawn across a timeline. Fields: `x0`, `x1` (years), `spy` (seconds per year, 1.0–1.5), `series` [{name, xs (fractional years), ys, color, decimals}], `ymin`, `ymax`, `yticks`, `suffix`, `xstep`, optional `shade` {above, below, color, label} to shade where one line beats another, and `events` [{x, y, text, sub, dur}] short pop-up callouts at key moments (peaks, crashes, records). Monthly or quarterly data looks best.
   Older templates (only if a topic really needs a map; keep it fast with `hold` 2 or less):
   - `map_race`: UK regions coloured by value, stepping through years (12 region names exactly as in `engine/assets/uk_regions.json`; use `null` for missing, which shows NO DATA). Copy the `labels` block from D01 (in-map labels + callout boxes).
   - `bar_race`: up to 12 bars that re-rank each year: `items_data` [{name, values:[one per year], color}], `show`, `top`, `row`.
   - `line_race`: several lines drawn across years: `series` [{name, values, color}], `ymax`, `ymin`, `yticks`, `xstep`.
   Common fields: `years` (real data years only), `prefix`/`suffix`/`decimals`/`short`, `lead` 0.5, `tail` (seconds after the race for the `after` overlay pages, about 13), and `after` pages: biggest change, a surprise, then a call to action ("WHAT'S IT LIKE WHERE YOU LIVE?" / "COMMENT YOUR AREA" or a question). Total length 61–70 s: for bar_race2, lead + (years−1)×spy + tail; for line_race2, lead + (x1−x0)×spy + tail. Set `after` page times (`at`) relative to the end of the race.
4. Top level: `"kind": "data"`, `slug` `TheMoneyWhatIfs_DNN_name`, `title`, `banner` {text, highlight}, a short `footnote` naming the source (keep it under about 90 characters), `thumbnail`.
5. Compute the headline facts for the `after` pages in Python from the same numbers (e.g. % change).
6. Render the same way as What If videos (step 7). The fast templates render in about 2 minutes each. Check a frame mid-race and the final frame: no label overlaps, nothing cut off.
7. Post text: hook line, "Comment your area 👇" (or the question), source, 4–5 hashtags (#data #uk ...). TikTok `isAigc` false.

## 6. Fact-checker (separate agent, independent)

Spawn a **fresh** agent that has not seen your reasoning. Give it only the spec files, posts.json and the `data/DNN_*.md` source notes. Its brief: independently verify every number and factual claim (for data videos, re-fetch the source and spot-check at least 10 values per video plus every number on the `after` pages) (recompute all maths in Python; check every current fact with WebSearch against an official or reputable source; check spoken numbers match on-screen numbers; flag anything misleading, any copied wording, any claim about a real person or company). It returns PASS or a list of problems per video.
Fix every problem and re-run the checker on the fixed videos. If a video still cannot be verified after one fix round, drop it and make a replacement from the next-best topic (which also goes through the checker).

## 7. Render and inspect

For each spec:
```bash
cd ~/media/engine && python3 mwi.py specs/NN_name.json ~/out/NN_name --stills
```
Look at `stills.png` and the thumbnail with Read: fix text overlaps, empty-looking scenes, text running off screen. Confirm the printed duration is 61 s or more (add a line if not). Then:
```bash
python3 mwi.py specs/NN_name.json ~/out/NN_name --reuse-voice
ffmpeg -v error -y -i ~/out/NN_name/<slug>.mp4 -frames:v 1 -vf scale=270:-1 ~/out/NN_name/first.png
```
Check `first.png` shows the hook claim and `check.png` looks right. Re-render anything broken.

## 8. Publish

1. Copy each `<slug>.mp4` and `<slug>_thumbnail.png` to the root of `~/media`, `git add`, commit (message "Add videos NN-MM"), and `git -c push.negotiate=true push`. Check each link returns 200: `curl -sS -o /dev/null -w "%{http_code}" https://raw.githubusercontent.com/moneywhatifsvideos/moneywhatifs-media/main/<file>`.
2. Metricool `createScheduledPost` per video into its slot (blogId 8204403). `info` JSON:
   - `autoPublish` true, `draft` false, `descendants` [], `firstCommentText` "", `hasNotReadNotes` false, `mediaAltText` [], `shortener` false, `smartLinkData` {"ids": []}
   - `media`: [raw GitHub MP4 link]; `videoThumbnailUrl`: raw GitHub PNG link
   - `providers`: [{"network":"youtube"},{"network":"tiktok"}]
   - `publicationDate`: {"dateTime":"YYYY-MM-DDTHH:MM:00","timezone":"Europe/London"}
   - `text`: the description
   - `youtubeData`: {title, type "short", privacy "public", tags, category "EDUCATION", madeForKids false, isAiGeneratedContent false}
   - `tiktokData`: {disableComment false, disableDuet false, disableStitch false, privacyOption "PUBLIC_TO_EVERYONE", commercialContentThirdParty false, commercialContentOwnBrand false, **title** (required, same as YouTube title), autoAddMusic false, isAigc true}
   Schedule the first one alone; if it succeeds, do the rest. Keep each `plannerUrl`.
3. Append the new topics to `topics.md` (with type and date), commit the specs, analytics note and topics.md, push.

## 9. Report to Archie

Send one message (SendUserMessage; also PushNotification if available) with:
- the week's schedule: day, time, title, Metricool planner link;
- analytics highlights: best and worst videos last week and what changed in this batch because of it;
- trending topics used and the twist added;
- anything dropped or that went wrong, and anything he needs to do.
Keep it short and scannable. Remind him he can delete any post in the Metricool planner before it goes out.
