# Pre-video guide: from "no idea" to "ready to record"

Do this for **every** video, before you record. It takes about 2 hours (your Sunday block).
It follows the roadmap: Phase 4 steps 1-3 (find the idea, package first, script) and the rules.
The result is ONE brief file per video: `research/<yyyy-mm-dd>-<short-name>.md` (template at the bottom).

This guide does not choose your tests or your first videos. That is Phase 2. This is the repeatable routine for any video.

## Before the first run (once, about 5 minutes)

1. **Open a new Claude Code session** in `D:\YTHELPER\gta-channel`. Commands are loaded when a session starts.
2. **Install the plugin (new machine or fresh clone only).** The skills `/yt-package`, `/yt-script`, `/yt-seo` and `/yt-viral` come from the `youtube-agent` plugin. This repo declares it in `.claude/settings.json`, but it is installed per machine. Claude Code should offer to install it when you open the folder. If it does not, run `/plugin marketplace add Jakeschincariol/youtube-agent-skill` and then `/plugin install youtube-agent@youtube-agent-skill`. Without it `/pre-video` still finishes, but titles, hooks and search text are written by hand and labelled "manual estimate".
3. **yt-dlp** (`tools\bin\yt-dlp.exe`) reads public YouTube pages for steps 1b and 1c (search, outlier ranking, comments). It was tested on live YouTube. The `.exe` is not stored in this repo (it is git-ignored): on a new machine download `yt-dlp.exe` from github.com/yt-dlp/yt-dlp/releases into `tools\bin\`. `/pre-video` starts it by itself through `collect.py`, which the command pre-approves, so you may **not** be asked. If you do not want it used, delete the file: the routine then does step 1a only.
4. **Fewer prompts (optional).** Paste the lines shown below this list under `allowed-tools:` in `.claude\commands\pre-video.md`. They let the command read your `voice.md` and run the plugin's scoring scripts without asking. Without them you approve 2-3 prompts per run, or the script is a neutral draft and the scores are labelled "manual estimate, tool not run".
5. **Give Claude your real voice.** Put a few paragraphs of how you actually talk into `~/.claude/youtube/voice.md` ("How I actually talk"). Until then every script is a neutral draft.

The lines for item 4 (copy them exactly, the stars are part of the rule):

```
  - Read(~/.claude/youtube/**)
  - Read(~/.claude/plugins/cache/youtube-agent-skill/**)
  - PowerShell(python *title.py*)
  - PowerShell(python *hookscore.py*)
  - PowerShell(python *swipe.py*)
  - Bash(python *title.py*)
  - Bash(python *hookscore.py*)
  - Bash(python *swipe.py*)
```

## Two ways to use it

**A. One command (easiest).** Open Claude Code in this folder and type:

```
/pre-video <one sentence idea, or: no idea yet, game: GTA 5>
```

Claude does steps 0-6 alone and saves the brief in `research/` and a **PDF in `output/`** (same name). It does not stop at the checkpoints. It picks the top 3 ideas, develops the best, and gives a GO/NO-GO as a *recommendation*. The two human calls (would I click it? my own words?) are in a "You decide before recording" box at the top of the PDF.

**A2. Step by step with Claude.** If you want to decide at each checkpoint yourself, paste:

```
Follow PRE-VIDEO-GUIDE.md for this idea: <one sentence, or "I have no idea yet, game: GTA 5">.
Do steps 1-6 in order. Stop at every CHECKPOINT and wait for me. Save the brief in research/.
```

**B. Do it yourself,** step by step, using the commands below.

---

## Step 0: What is the idea? (2 min)

Write it as **a question + how you will answer it**:

> "How fast do the cops arrive after a minor crime?" + "I measure it 10 times in the same place and take the average."

No idea? Use these sources: your content pillars in `CLAUDE.md`, the comments in step 1c, and the search suggestions in step 1a.

## Step 1: Look at YouTube first (20 min)

Always look before you decide. You are looking for three things.

**1a. What people type into YouTube search**
```
python tools/collect.py suggest "gta 6 cops"
```
Use a short seed (2-3 words). Long phrases return nothing. Top block = most typed. Every line is a possible title or idea.
It shows US-English results (your target audience). To see another country add `--region bd` (or `gb`, `in`...).

**1b. What already works** (needs yt-dlp in `tools/bin`)
```
python tools/collect.py niche "gta 5 police chase" --keep gta --comments 2 -o research/<name>-niche.json
```
It searches YouTube, keeps only videos with "gta" in the title, prints the outlier table itself, and also reads the comments of the two most-viewed outliers (that covers step 1c too). Optional: `/yt-viral research/<name>-niche.json` adds a title-formula classification.

It ranks every video by **how far it beat its own channel's usual views** (not by channel size). Read:
- the top 5 and their multiple (2x or more is a signal)
- the one thing they share (format? question? number in the title?)
- the gap: what does nobody show **with real data**? That gap is your idea.

**1c. What viewers ask for** (needs yt-dlp)
```
python tools/collect.py comments <url of one of the top videos>
```
The "look like requests" list = free video ideas ("can you test...?"). Roadmap rule 7: comments are your idea database.

**What this cannot tell you:** other people's click rate or retention. You only see public views. Views are a signal, not proof. Do not copy a video: take the structure and add your own test data. That data is what nobody can copy.
If a channel has fewer than 4 videos collected, `/yt-viral` skips it (a median needs 4+).

> **CHECKPOINT 1.** Pick ONE idea. If two are tied, pick the one you can test fairly.

## Step 2: Does it fit? (5 min)

All answers must be yes. If one is no, go back to step 1.

- [ ] Fits a pillar: Experiment, Systems explained, Developer x AI, or a Short?
- [ ] ONE clear question and ONE clear answer? (rule 3)
- [ ] Is the test a **written procedure** (same steps, same metric) that you can re-run in GTA 6 after launch? Whether GTA 6 even has the feature is unknown until launch. That is not a fail: it becomes the question you ask then.
- [ ] Fair test: same time of day, weather, place and vehicle class; repeat 5-10 times and use the average
- [ ] Not news, a rumor, a leak, or a fake "secret"? No story spoilers in title/thumbnail?
- [ ] Every GTA 6 fact you need is in `gta6-notes.md` (official source)? Unknown features phrased as a **question**, not a claim?

## Step 3: Package first (30 min): title + thumbnail, before recording

Rule 1: if you cannot make it clickable, **do not make the video.**

In Claude Code: `/yt-package` with your idea and the best lines from step 1.
- It writes 10 titles and keeps the top 3 with scores. Check: under 60 characters (40 for mobile), has a number or name, no vague words.
- It writes a thumbnail brief: **max 3 words**, and the words must **not repeat the title**.
- Make the thumbnail in Canva yourself. Your masked `< >` character goes in a corner.

> **CHECKPOINT 2.** Look at the title + thumbnail at small size. Would YOU click? No? Pick another idea.

## Step 4: Hook and script (45 min)

In Claude Code: `/yt-script`. It writes 5 hooks, scores them, shows the best 2.
- Hook score under 55 (WEAK): rewrite. A high score is not a promise, a low score means look again.
- Rule 2: the **first 30 seconds show the stakes or the result.** No intro, no logo, no "hey guys".
- Every beat has `[ON SCREEN: ...]`, so you are never just a talking head.
- Then **rewrite it in your own words and read it aloud.** The script is a draft. Your voice is your face (rule 6).
- Every number in the script must come from `test-results.csv` or a source. Claude must never invent one.

## Step 5: Search text (15 min)

In Claude Code: `/yt-seo`.
- The first **two lines** of the description are what people see. Say what the video gives them, in the words they type (from step 1a).
- Write the 3 searches this video should win. Check the title contains those words.
- Tags: 15 at most. They matter little. Chapters come after editing (`/yt-chapters`).

## Step 6: Test plan + recording check (10 min)

- [ ] Write the exact test rules in the brief (conditions from step 2). They must be identical every run.
- [ ] You know which `test-results.csv` columns you will fill after each run (date, game, patch, test_id, run, metric, value, unit, time_of_day, weather, location, vehicle, footage_file, notes).
- [ ] OBS: mic level OK, scene OK, saves to `D:\obsVideo`. Record a 10-second test and play it back.
- [ ] A clear file name per run, and the same name goes in the `footage_file` column.

## GO / NO-GO

GO only if **all** are true: you have a clickable title + thumbnail, a hook that shows the result in 30 seconds, a fair repeatable test, and facts that come from a source or your own data.
Otherwise: NO-GO. Go back to step 1 with a new idea. Finishing videos beats perfect videos (rule 8), but a video nobody clicks teaches you nothing.

Next: record, then follow "Production pipeline" in `CLAUDE.md` (transcribe, rough cut, Resolve, Shorts). After a week: `/yt-retention`, and write ONE lesson.

---

## Notes

- **Before GTA 6 launches (2026-11-19)** there is almost no GTA 6 test content, so research the GTA 5 / "experiments" niche. After launch, run step 1 again with GTA 6 queries to see what early winners look like.
- Do not run `niche` too often or with huge numbers. Defaults (8 channels, 30 videos each) are enough. It only reads public pages and never logs in.
- No yt-dlp? Do step 1a only. For 1b, paste 4+ recent videos (title + views) per channel into the chat and `/yt-viral` can work from that list.

## If something goes wrong

| What you see | What it means | What to do |
| --- | --- | --- |
| No PDF in `output\` | The brief was written but the PDF step failed | The brief is in `research\`. Run `uv run tools/make_pdf.py research/<name>.md`. If it still fails, close all Edge windows and retry |
| "yt-dlp not found" / "yt-dlp failed" | Steps 1b/1c could not run | The PDF says what was skipped. Step 1a still works. "Sign in to confirm you're not a bot" means YouTube is slowing you down: wait a few minutes and retry with `--channels 3`. Anything else: send Claude the error line |
| Scores say "manual estimate, tool not run" | The plugin scripts were not allowed to run, or the plugin is not installed | Add the permission lines in "Before the first run", or approve the prompts. On a fresh clone, install the plugin first (item 2) |
| Script says "neutral draft, not my voice" | `voice.md` was empty or unreadable | Add your speech samples to `~/.claude/youtube/voice.md` |
| Claude says NO-GO | Its recommendation on the plan, not a rule | Read the reason in the PDF. You decide |

## Brief template (copy to `research/<yyyy-mm-dd>-<short-name>.md`)

```
# <working title>
Date:            Game: GTA 5 / GTA 6      Pillar:
Idea (question + how answered):
Why now / what the research showed (3 lines, with the multiples you saw):
Search phrases people use (from 1a):
Requests from comments (from 1c):

Title (chosen):                 Alternatives:
Thumbnail (max 3 words, not the title):
Hook (chosen) + score:
Script: link or paste
Description first 2 lines:      3 target searches:

Test rules (identical every run):
  time of day / weather / location / vehicle:   runs planned (5-10):
Facts used + their source (gta6-notes.md line or test-results.csv rows):

GO / NO-GO:   Reason:
After a week (fill later): CTR / first-30s retention / returning viewers / ONE lesson:
```
