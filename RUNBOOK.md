# The Money What Ifs: weekly production run

This is the full procedure for the unattended weekly run. Follow it top to bottom. Archie is not watching: never stop to ask questions. Make sensible decisions, note them in the report, and keep going. Only stop early if something would publish wrong or harmful content.

Channel: YouTube @TheMoneyWhatIfs and TikTok @themoneywhatifs, both linked to **Metricool brand 8204403** (timezone Europe/London).
Output: **three videos per day for the next 7 days** (Mon to Sun after the run) for YouTube Shorts and TikTok, **posted by Archie himself** with the platforms' own schedulers (see step 8):
- one **"Money Data" video** (animated real UK data: bar race or line race; music only, no voice),
- one **"What If" video** (narrated glow-style scenario), and
- one **"Trending" video** (glow style, narrated): built on this week's UK money news or a money question/trend that is popular right now (from the trend scout and the research bot). It may be a topical What If, a "money truth" (relatable myth-flip, e.g. G02 "Same salary"), or a short news-driven explainer. It must still be fact-checked and original.
- **Posting times: 10:00, 16:00 and 19:00 (UK).** The format rotates daily so the analyst can separate format from time: on day-of-month d, with formats in the order [Data, What If, Trending] and slots [10:00, 16:00, 19:00], slot i gets format number (i + d) mod 3. Example: d = 26 → 10:00 What If, 16:00 Trending, 19:00 Data. Videos already in an earlier pack count towards that day's mix; fill only the missing formats in the free slots.
- **Every video must be at least 63 seconds long** (TikTok Creator Rewards only counts videos over 1 minute; 63 s gives a safety margin).
This is Archie's standing plan (confirmed 20 Nov 2026): **one Data, one What If and one Trending video every day**. Do not change the mix yourself; if the analytics strongly favour one format, recommend a change in the report and let Archie decide. If you cannot make a video that meets the quality bar for a slot, leave the slot empty and say so in the report; never publish a weak video to fill a slot.
- **Metricool is for analytics only** (free plan: only 20 published posts a month). Never create or update scheduled posts in Metricool.

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

Before planning new videos, read `~/media/packs/BACKLOG.md`: finished videos listed there are ready to use and should fill free slots first (TikTok-only ones go in a slot as TikTok-only, and the YouTube upload for that slot can be skipped). Remove used items from the backlog.

The schedule ledger is the posting packs in `~/media/packs/` (one file per week, named by the first date it covers). Read every pack that covers any of the 7 days after today: a slot (date + time) listed in a pack is taken. Each day has three slots, 10:00, 16:00 and 19:00, with formats set by the rotation rule above. Make one video of the right format per free slot (normally 7 + 7 + 7 = 21). Do not use Metricool for this.

## 2. Analyst: what is working

1. Metricool `getAnalyticsDataByMetrics` for the last 28 days, YouTube per-video: `YTVV17` title, `YTVV06` views, `YTVV08` average view duration, `YTVV09` likes, `YTVV11` comments, `YTVV12` shares. For TikTok, call `getAnalyticsAvailableMetrics` with network `tiktok` and connector `posts`, then pull views, likes, comments, shares, average watch time per post.
2. Rank videos by views and by average view duration as a share of length. Note which topic types (see topics.md) and which hook shapes did best and worst. If there is no data yet, say so and fall back to an even mix. (YouTube posts uploaded by Archie still appear in Metricool analytics because the channel is connected.) Also compare formats (Data / What If / Trending, splitting Trending into Money mindset vs other Trending) and times (10:00 / 16:00 / 19:00), using median views and average view percentage per group, and report which format and which time are ahead; after 3 weeks of rotation, recommend a fixed timetable if one is clearly better. Note: TikTok posts before 20 Nov 2026 were held back by API posting, so ignore their views.
3. Write the findings to `~/media/analytics/YYYY-MM-DD.md` (short: top 3, bottom 3, patterns, what to do more/less of).

## 3. Trend scout (separate agent)

First read `~/media/research/ideas.md` (the idea bank written by the weekly research bot) and the newest `~/media/research/YYYY-MM-DD.md` report. Prefer ideas from the bank; follow any style recommendations in the report **only if they are marked "APPROVED by Archie"**. Mark ideas you use as `USED (date)` in ideas.md when you commit at the end.

Spawn a separate agent (Agent tool) with this brief: find what money and personal-finance topics are popular **right now** with UK short-form audiences. Use WebSearch (standard first, extended if thin) for things like: viral money "what if" shorts and TikToks, popular personal finance shorts in the UK, trending questions on r/UKPersonalFinance, this week's UK money news (Budget, Bank of England, prices, wages, house prices, energy bills, student loans, tax changes). Return **25 candidate topics**, each with: the question in one line, why it is popular (with source URLs), and a suggested twist. Topics only, no scripts copied.

## 4. Choose the topics

Pick What If topics for the free What If slots and Trending topics for the free Trending slots (Trending = the scout's freshest items and this week's UK money news; what is being talked about now, not evergreen) (data topics are chosen in step 5b):
- none already in topics.md (a clearly different angle on a theme is fine);
- weighted towards the analyst's winning types and hook shapes, but always a mix: savings/compounding, either/or choices, absurd-but-concrete numbers, debt traps, "what if the government/economy…", everyday prices;
- at least 3 tied to this week's UK news when the scout found good ones;
- each must have a real twist (something most viewers get wrong).

## 5. Writer: scripts as spec files (GLOW STYLE)

**All What If videos use the glow style** (Archie's decision, 19 Nov 2026): dark stage, spotlights, glowing faceless figures, gold £ counters, thin outline icons, small pill labels, 1–2 word captions, slow camera push. Never use the old cartoon templates (stack, figures, phone, bars, tags, chart, twist, choice) for new What Ifs.

Write one spec per video into `~/media/engine/specs/GNN_short_name.json`, numbering on from the highest G-number, slug `TheMoneyWhatIfs_GNN_short_name`. **Read two of `engine/specs/G01.json` … `G09.json` first and copy their structure exactly**, and read the docstring and `DRAW` table at the top of `engine/glow.py`.

Spec format:
- Top level: `"style": "glow"`, `"voice": "af_heart"`, `"speed": 0.92`, `slug`, `title`, `footnote`, `thumbnail` {`scene` (index of a visually strong scene), `lines` [{text, c, size}] — 2–3 short lines; the scene's top-area text is hidden automatically on the thumbnail}.
- Each scene: `"type": "glow"`, `lines` (voice lines), `els` (elements), optional `spots` [[x, power]] (spotlight cones, power 40–90), `focus` [x, y] (camera push target), `twist` true (ducks music), `footnote` true (shows the footnote on that scene), `dings` [[line, offset]].
- Elements (`"k"`): `counter` (big £ number; `from`/`to`/`dur` or `keys` [[at, value, dur]], `prefix`, `suffix`, `dec`, `c`, `label`), `caps` (small spaced label), `text` (big bold line), `pill` (white rounded label; `inv` for outline), `fig` (glowing figure; `s`, `c` white/dim/mid/gold, `pose` stand/up/point/shrug, `hat` grad/crown, `ring`, `tag`, `move`), `crowd` (row of figures, `hero` index), `stairs` (figure climbing, `climb` {at, dur}), `cards` (row of outline cards with icons, labels and optional cross/check `mark`), `grid` (boxes that fill with marks over time), `curve` (glowing line chart, `ys` real values, `xlabels`, `fill`, `head`), `bars` (2–3 glowing bars with value labels, `sub`), `icon` (coin, cup, house, card, phone, bag, car, chart, clock, cross, check, question, pound, mattress, pint, bank, arrow_up), `box` (glass panel with 1–2 lines), `coins` (coin rain), `divider`, `line` (dashed floor).
- Every element takes `at` (and optional `until`): line index, [line, offset] or seconds from scene start. Keep content between x 80–1000 and y 250–1320 (captions sit at y 1420; TikTok covers the bottom and right edge).
- **Variety:** use at least 7 different element kinds per video and never the same layout twice in a row. Something new should appear every 1–2 seconds.

Script rules:
- **Hook (most important):** scene 0 shows the claim or the payoff number on the first frame (elements `"at": 0`, counters with `dur` 0). First voice line is one sentence of at most about 15 words.
- 8–10 scenes: hook, relatable setup, mechanism, escalating numbers, payoff, twist, lesson, closing question.
- **Closing question, not "Comment A or B":** end with a natural, slightly personal question people want to answer ("How old were you when you started saving?", "Where did your last pay rise go?", "Ever only paid the minimum? No judgement."). Put the same question in the description.
- **Money mindset (Archie, 21 Nov 2026): 3–4 of the 7 Trending slots each week.** The emotional, identity-driven energy of motivational shorts, but always grounded in a real UK money number or worked example, never generic hustle motivation. Shape: a relatable belief or habit as the hook ("You're not bad with money. You're paid monthly and spend daily."), a worked example with real numbers computed in Python, then a quotable closing line people want to share. Examples: "The 1% rule: why rich people never buy cars with cash", "Why your 20s matter more than your 40s, in one graph", "What £10 a week says about you in 30 years". Rules: no promises of wealth, no "quit your job" advice, no named real people, no investment recommendations; "Not financial advice." footnote on anything about returns. Glow style, slow and atmospheric music bed is fine, still at least 7 element kinds and 63+ seconds. Mark these as type "Money mindset" in the pack and topics.md so the analyst can compare them.
- **Money truths:** usually go in Trending slots; up to 2 of the 7 What If slots per week may also be "money truth" scripts: a relatable myth-flip with an identity angle (e.g. "Same salary. One retires rich." G02). Same glow format, one strong statement, illustrative numbers computed in Python with the assumptions in the footnote.
- 175–195 spoken words so the video is **63–72 seconds**. Numbers as words in voice lines, digits on screen; every on-screen number must match the spoken one.
- Compute every number in Python first; take current facts from sources found this run and name the source in `footnote`. "Not financial advice." on anything showing returns or debt.
- On-screen text: no →, ✈ or emoji (Poppins lacks them). £ × % · = are fine.
- Also write, per video: YouTube/TikTok **title** (question or statement + one emoji), **description** (hook line, the closing question + 👇, footnote, 4–5 hashtags, no #shorts), and 6 tags. Keep these in a `posts.json` in the run folder.

## 5b. Data videos

For each free data slot, make one data video spec in `~/media/engine/specs/DNN_short_name.json` (numbering on from the highest D-number). Read `engine/specs/D01_house_prices_by_region.json` first: it is the reference example.

1. **Pick a data topic** people in the UK care about and will want to compare or argue about in the comments: house prices or rents by region, wages by job or region, what things cost then vs now (bread, pint, petrol, energy bills, train fares, tuition), inflation, interest rates, savings rates, council tax by region, Christmas spending by region, UK vs USA comparisons, wealth or pay gaps by age. Use the trend scout's ideas and this week's news. Not already in topics.md.
2. **Get the real numbers.** Use WebSearch to find an official source (ONS, HM Land Registry, Bank of England, gov.uk, OBR, HMRC, Ofgem, UK Finance) and read the values with WebFetch (it can read CSV files and tables from URLs found by WebSearch; use its `offset` to page through long files). The shell cannot download from most of these sites. GitHub-hosted datasets are fine. Record every value with its source URL in `~/media/data/DNN_short_name.md`. If you cannot get a complete, sourced dataset, pick another topic.
3. **Choose a template. Use the fast, light "DATA-style" templates** (Archie found the slow map style too slow, 19 Nov 2026): constant motion, about 1.2–1.6 seconds per year, big year counter, light chart background. Reference examples: `D02_most_expensive_regions.json` (bar race) and `D03_rates_vs_inflation.json` (line race). Add `"light": true` and `"footnote_y": 1640` at the top level.
   - `bar_race2` (like "Which job pays the most in the UK?"): up to 11 items re-ranking every year. Fields: `years`, `items_data` [{name, label, values (one per year, null if missing), color [r,g,b]}], `prefix`/`suffix`/`decimals`, `spy` (seconds per year, 1.2–1.6), `lead`, `tail`, `top` 410, `row` 98, `year_y` 1530, `subtitle`. Best with 20–40 years of annual data where the order changes.
   - `line_race2` (like "Where do people in the UK go on holiday?"): 2–6 lines drawn across a timeline. Fields: `x0`, `x1` (years), `spy` (seconds per year, 1.0–1.5), `series` [{name, xs (fractional years), ys, color, decimals}], `ymin`, `ymax`, `yticks`, `suffix`, `xstep`, optional `shade` {above, below, color, label} to shade where one line beats another, and `events` [{x, y, text, sub, dur}] short pop-up callouts at key moments (peaks, crashes, records). Monthly or quarterly data looks best.
   Older templates (only if a topic really needs a map; keep it fast with `hold` 2 or less):
   - `map_race`: UK regions coloured by value, stepping through years (12 region names exactly as in `engine/assets/uk_regions.json`; use `null` for missing, which shows NO DATA). Copy the `labels` block from D01 (in-map labels + callout boxes).
   - `bar_race`: up to 12 bars that re-rank each year: `items_data` [{name, values:[one per year], color}], `show`, `top`, `row`.
   - `line_race`: several lines drawn across years: `series` [{name, values, color}], `ymax`, `ymin`, `yticks`, `xstep`.
   Common fields: `years` (real data years only), `prefix`/`suffix`/`decimals`/`short`, `lead` 0.5, `tail` (seconds after the race for the `after` overlay pages, about 13), and `after` pages: biggest change, a surprise, then a call to action ("WHAT'S IT LIKE WHERE YOU LIVE?" / "COMMENT YOUR AREA" or a question). Total length 63–72 s: for bar_race2, lead + (years−1)×spy + tail; for line_race2, lead + (x1−x0)×spy + tail. Set `after` page times (`at`) relative to the end of the race.
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
Look at `stills.png` and the thumbnail with Read: fix text overlaps, empty-looking scenes, text running off screen, captions hidden behind elements, and any scene that looks like the one before it. Glow videos render in about 2 minutes each. Confirm the printed duration is **63 s or more**. If it is short, add a line (What If) or increase `tail` (data), and re-render. As a last resort, pad the finished file with an end hold: `ffmpeg -i in.mp4 -vf tpad=stop_mode=clone:stop_duration=PAD -af apad=pad_dur=PAD -c:v libx264 -crf 18 -preset veryfast -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k out.mp4`. Check every final MP4 with ffprobe before publishing; never publish anything under 63 s. Then:
```bash
python3 mwi.py specs/NN_name.json ~/out/NN_name --reuse-voice
ffmpeg -v error -y -i ~/out/NN_name/<slug>.mp4 -frames:v 1 -vf scale=270:-1 ~/out/NN_name/first.png
```
Check `first.png` shows the hook claim and `check.png` looks right. Re-render anything broken.

## 8. Publish: the posting pack (Archie uploads)

Archie posts everything himself with the native schedulers (YouTube Studio, and TikTok Studio on desktop, which schedules up to 10 days ahead). TikTok gave API-scheduled posts 0 views, and Metricool's free plan only allows 20 published posts a month, so **do not schedule anything in Metricool.**

1. Copy each `<slug>.mp4` and `<slug>_thumbnail.png` to the root of `~/media`, `git add`, commit (message "Add videos for week of YYYY-MM-DD"), and `git -c push.negotiate=true push`. Check each link returns 200: `curl -sS -o /dev/null -w "%{http_code}" https://raw.githubusercontent.com/moneywhatifsvideos/moneywhatifs-media/main/<file>`.
(Exception for the week of 23 Nov 2026 only: YouTube for Mon 23 16:00, Tue 24 10:00 and Wed 25 10:00 is already scheduled in Metricool, and the pack `packs/2026-11-21.md` covers TikTok for 21–25 Nov. Treat all those slots as taken.)
2. Write the posting pack `~/media/packs/YYYY-MM-DD.md` (date = first day it covers). Copy the layout of the newest existing pack exactly: the upload instructions at the top, a summary table (When, Type, Video link, Platforms, TikTok AI label), then one section per video in time order with: download link (`https://github.com/moneywhatifsvideos/moneywhatifs-media/raw/main/<file>`), thumbnail link, platforms, TikTok AI label (ON for narrated videos, off for data videos), the **Title** in its own code block and the **Caption** (description) in its own code block, so Archie can copy each with one tap.
3. Append the new topics to `topics.md` (with type and date), commit the pack, specs, analytics note and topics.md, push.

## 9. Report to Archie

Send one message (SendUserMessage; also PushNotification if available) with:
- the link to the posting pack (`https://github.com/moneywhatifsvideos/moneywhatifs-media/blob/main/packs/YYYY-MM-DD.md`) and a reminder to upload and schedule the week's videos on YouTube Studio and TikTok Studio (about 40 minutes);
- the week's schedule: day, time, type, title;
- analytics highlights: best and worst videos last week and what changed in this batch because of it;
- trending topics used and the twist added;
- anything dropped or that went wrong, and anything he needs to do.
Keep it short and scannable. He can skip any video he doesn't like by simply not uploading it.
