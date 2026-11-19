# The Money What Ifs: weekly production run

This is the full procedure for the unattended weekly run. Follow it top to bottom. Archie is not watching: never stop to ask questions. Make sensible decisions, note them in the report, and keep going. Only stop early if something would publish wrong or harmful content.

Channel: YouTube @TheMoneyWhatIfs and TikTok @themoneywhatifs, both linked to **Metricool brand 8204403** (timezone Europe/London).
Output: **two videos per day for the next 7 days** (Mon to Sun after the run), at **10:00 and 16:00 UK time**, posted to YouTube Shorts and TikTok.

Hard rules:
- Never spend Higgsfield credits or any money.
- Every number is computed in Python or taken from a source found this run. Never from memory.
- Topics from other creators are fine as **inspiration only**. Never copy their scripts, wording, characters, visuals, music or titles. Every video must be an original script with our own UK angle and twist.
- No claims about real private individuals; no named companies portrayed negatively; no investment recommendations ("not financial advice" footnote on anything showing returns).
- YouTube: madeForKids false, isAiGeneratedContent false (cartoon). TikTok: isAigc true (AI voice).

## 0. Set up the workspace

1. `add_repo` owner `moneywhatifsvideos`, repo `moneywhatifs-media`, access `push`. Clone it: `git clone --depth 1 https://github.com/moneywhatifsvideos/moneywhatifs-media ~/media`. The engine is `~/media/engine/mwi.py`; past specs are in `~/media/engine/specs/`; `~/media/topics.md` lists topics already made.
2. Voice model and packages:
```bash
mkdir -p ~/kokoro && cd ~/kokoro
curl -sSL -o voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
curl -sSL -o kokoro-v1.0.int8.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.int8.onnx
pip install --break-system-packages -q kokoro-onnx soundfile pillow numpy
export MWI_TTS_DIR=~/kokoro
```
3. Fonts: the engine needs Poppins Bold and Medium at `/usr/share/fonts/truetype/google-fonts/`. If missing, download `Poppins-Bold.ttf` and `Poppins-Medium.ttf` from `https://github.com/google/fonts/raw/main/ofl/poppins/` and fix the FB/FM paths at the top of mwi.py.
4. Check ffmpeg exists.

## 1. Find the free slots

Metricool `getScheduledPosts` (brandId 8204403, timezone Europe/London) for the 7 days after today. Each day has two slots: 10:00 and 16:00. A slot is taken if any post is already there. The number of videos to make = number of free slots (normally 14).

## 2. Analyst: what is working

1. Metricool `getAnalyticsDataByMetrics` for the last 28 days, YouTube per-video: `YTVV17` title, `YTVV06` views, `YTVV08` average view duration, `YTVV09` likes, `YTVV11` comments, `YTVV12` shares. For TikTok, call `getAnalyticsAvailableMetrics` with network `tiktok` and connector `posts`, then pull views, likes, comments, shares, average watch time per post.
2. Rank videos by views and by average view duration as a share of length. Note which topic types (see topics.md) and which hook shapes did best and worst. If there is no data yet, say so and fall back to an even mix.
3. Write the findings to `~/media/analytics/YYYY-MM-DD.md` (short: top 3, bottom 3, patterns, what to do more/less of).

## 3. Trend scout (separate agent)

Spawn a separate agent (Agent tool) with this brief: find what money and personal-finance topics are popular **right now** with UK short-form audiences. Use WebSearch (standard first, extended if thin) for things like: viral money "what if" shorts and TikToks, popular personal finance shorts in the UK, trending questions on r/UKPersonalFinance, this week's UK money news (Budget, Bank of England, prices, wages, house prices, energy bills, student loans, tax changes). Return **25 candidate topics**, each with: the question in one line, why it is popular (with source URLs), and a suggested twist. Topics only, no scripts copied.

## 4. Choose the topics

Pick exactly as many topics as there are free slots:
- none already in topics.md (a clearly different angle on a theme is fine);
- weighted towards the analyst's winning types and hook shapes, but always a mix: savings/compounding, either/or choices, absurd-but-concrete numbers, debt traps, "what if the government/economy…", everyday prices;
- at least 3 tied to this week's UK news when the scout found good ones;
- each must have a real twist (something most viewers get wrong).

## 5. Writer: scripts as spec files

Write one spec per video into `~/media/engine/specs/NN_short_name.json`, numbering on from the highest existing number. Follow the format of the existing specs exactly (read two of them first). Rules:
- **Hook (most important, from analytics):** scene 0 states the full claim on screen in the first frame: key items `"at": 0`, static text (never a counter counting up from £0 in the hook). First voice line is one sentence of at most about 15 words that says the claim itself. Best hook shapes so far: clear either/or, absurd-but-concrete number, relatable trap.
- 8–9 scenes: hook, relatable setup, first result, mechanism, escalating numbers (DAY/AGE HUD, counters, chart), payoff number, twist, lesson, A/B question.
- 165–185 spoken words so the video is **61–70 seconds**. Numbers as words in voice lines, digits on screen.
- Compute every number in Python first; take current facts (prices, rates, tax bands) from sources found this run and name the source in the spec's `footnote`. Footnote "Not financial advice." on anything showing returns or debt.
- On-screen text: no →, ✈ or emoji (Poppins lacks them). £ × % ≠ = are fine.
- Templates, fields, moods, icons and chart kinds: see the docstring and TEMPLATES in mwi.py and the existing specs. `chart` series kinds: annuity, linear, decay (negative r = lump-sum growth), points.
- Also write, per video: YouTube/TikTok **title** (question + one emoji), **description** (hook line, "Comment A or B 👇", footnote, 4–5 hashtags, no #shorts), and 6 tags. Keep these in a `posts.json` in the run folder.

## 6. Fact-checker (separate agent, independent)

Spawn a **fresh** agent that has not seen your reasoning. Give it only the spec files and posts.json. Its brief: independently verify every number and factual claim (recompute all maths in Python; check every current fact with WebSearch against an official or reputable source; check spoken numbers match on-screen numbers; flag anything misleading, any copied wording, any claim about a real person or company). It returns PASS or a list of problems per video.
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
