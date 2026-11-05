---
description: Run the whole pre-video routine (research, idea, title, hook, script, SEO, test plan) and save it as a PDF in output/
argument-hint: '<one-sentence idea, or "no idea yet, game: GTA 5">'
allowed-tools:
  - PowerShell(python tools/collect.py *)
  - PowerShell(uv run tools/make_pdf.py *)
  - Bash(python tools/collect.py *)
  - Bash(uv run tools/make_pdf.py *)
  - Edit(research/**)
  - Edit(output/**)
  - Skill(yt-viral)
  - Skill(yt-package)
  - Skill(yt-script)
  - Skill(yt-seo)
  - Skill(youtube-agent:yt-viral)
  - Skill(youtube-agent:yt-package)
  - Skill(youtube-agent:yt-script)
  - Skill(youtube-agent:yt-seo)
---

Idea from me: $ARGUMENTS

Run `PRE-VIDEO-GUIDE.md` steps 0-6 for this idea, in order, **without stopping to ask me anything**. Read it first, then `CLAUDE.md` (the rules), `gta6-notes.md`, `test-results.csv` and `~/.claude/youtube/voice.md`. The guide is the source of truth for the steps; this file only says how to run it unattended. Game: GTA 5 unless I said otherwise. If I gave no idea, find one from the pillars in `CLAUDE.md`, the suggestions (1a) and the comments (1c).

Work in the project folder. Use `python` (not `python3`). **Run every command on its own, exactly as written in this file**: nothing before or after it. No `export`, `cd`, `$env:...`, `&&`, `;`, pipes or `2>&1`. The environment (UTF-8, caches) is already set in `.claude/settings.json`, and a command with extra parts in front is refused by the permission system. Call the `/yt-*` skills through the Skill tool; if a bare name is not found use the namespaced form, e.g. `youtube-agent:yt-package`.

## Name the files first
`<slug>` = today's date `yyyy-mm-dd` (run `Get-Date -Format yyyy-MM-dd` if unsure) + `-` + 2-4 lowercase words for the idea. Everything for this video uses it: `research/<slug>.md` (the brief), `research/<slug>-niche.json`, `output/<slug>.pdf`.

## Step 1: look at YouTube
- 1a: `python tools/collect.py suggest "<2-3 word seed>"` (a second seed if the first is thin).
- 1b + 1c in ONE command: `python tools/collect.py niche "<query>" --keep gta --comments 2 -o research/<slug>-niche.json`. It searches YouTube, keeps only videos with "gta" in the title (change the `--keep` word if the game is not GTA), prints the **outlier table itself** (views divided by that channel's own median, with links) and reads the comments of the two most-viewed outliers, flagging the ones that look like requests. Take the multiples and the requests from its output. Use a short, plain query such as "gta 5 police chase".
- If it prints "none: no channel had 4+ videos left", try one broader query. `/yt-viral research/<slug>-niche.json` is **optional** (it only adds a title-formula classification): if it needs a permission prompt or cannot run, skip it. That is not a failure and the table already exists.
- **If `collect.py` says yt-dlp is missing or failed, or a command is blocked by a permission prompt: do not work around it** (no other downloader, no running yt-dlp by hand, no scraping). Keep 1a only, and write in the brief which parts were skipped and the exact reason. Still finish.
- Use only numbers the tools printed. Quote multiples exactly. If a channel has fewer than 4 videos it was skipped by design; say so.

## What the CHECKPOINTS become when I am not there
- CHECKPOINT 1: rank the **top 3 ideas** with the evidence for each (the suggestion, the outlier and its multiple, the comment). Fully develop #1 only; give #2 and #3 one line each. Run the Step 2 fit checklist on #1 and show every answer with its evidence. Every item must be a clean yes: "partly" or "unchecked" counts as a fail, not a GO with a condition. If #1 fails, move to #2; if all three fail, the result is NO-GO and the brief says why. (A limit you can state on screen, such as "different maps, so road type matched", is fine only if the test is still fair; if you are not sure it is, put that question in the "You decide" box and recommend NO-GO.)
- CHECKPOINT 2 ("would YOU click this at small size?") is mine and cannot be done by you. Put it in the "You decide before recording" box.
- GO / NO-GO: write it as **Claude's recommendation**, never as a decision. It judges the **plan** (clickable title and thumbnail, a hook that promises the result in 30 seconds, a fair repeatable test, sourced facts). It is never NO-GO because nothing is measured yet, `test-results.csv` is empty, there is no GTA 5 baseline, or GTA 6 is not out yet: this brief is a plan, the script uses `[RESULT: ...]` placeholders for exactly that reason, and Phase 2 baselines are not your job. If the idea is vague (for example "smarter"), do not reject it: reframe it into the nearest ONE measurable question, say that you did, and continue.

## Scores come from the plugin scripts, not from you
Write the candidate titles to `research/<slug>-titles.txt` and the hooks to `research/<slug>-hooks.txt` (one per line), then run the plugin's scripts by full path, e.g. `python "<full path>\title.py" research/<slug>-titles.txt` and `python "<full path>\hookscore.py" research/<slug>-hooks.txt`. They live in `~/.claude/plugins/cache/youtube-agent-skill/youtube-agent/<version>/skills/yt-package/` and `.../yt-script/`. Quote the scores they print. If one cannot run, label every score from it **"manual estimate, tool not run"** in the brief and say why in the last section.

## Guardrails (nobody is watching this run)
- Never invent a number, result, view count or source. The script uses placeholders such as `[RESULT: average of 10 runs, seconds]`. `test-results.csv` is empty: there are no real results yet.
- GTA 6 facts only from `gta6-notes.md`, with their [read]/[via-search]/[outlet] tag. Unknown GTA 6 features are questions, not claims, and that includes titles, thumbnails, hooks and tags: a title may not name or imply a feature that `gta6-notes.md` lists as "not stated" (for example "wanted stars" or "wanted level" for GTA 6 while those are unknown). Word it so it still makes sense if GTA 6 has no such feature (e.g. "police", "cops", "chase").
- If the "How I actually talk" part of `voice.md` is empty, write the script in a plain neutral style and say at the top of the script section: "Neutral draft, not my voice. Rewrite it."
- Test rules cover **this one video** only. No Phase 2 planning, no series plan, no list of future tests.
- Nothing is posted anywhere. Do not touch Canva, the channel or the brand.

## Write the brief, then the PDF
1. Write `research/<slug>.md` as one self-contained document, with these headings in this order:
   1. `# <chosen title>` and a line `Date / Game / Pillar`
   2. A `>` quote: **Claude's recommendation: GO or NO-GO** + one sentence of reason, "a recommendation, not a decision".
   3. `## You decide before recording`: a `- [ ]` checklist: would I click this title and thumbnail at small size; rewrite the script in my own words and read it aloud; make the thumbnail in Canva; check that the test rules are fair; confirm the facts used.
   4. `## What YouTube showed`: 1a suggestions (table), 1b outliers (table: channel, video, views, multiple) + what the top ones share + the gap, 1c requests (list). Say plainly what was skipped.
   5. `## Idea` (the question, how it is answered, why this one) and `## Other ideas considered` (#2, #3).
   6. `## Fit check` (the Step 2 checklist with evidence).
   7. `## Title and thumbnail`: top 3 titles with their scores, the thumbnail brief (max 3 words, not the title).
   8. `## Hook and script`: the hooks with scores, the chosen one, the script draft with `[ON SCREEN: ...]` beats.
   9. `## Search text`: first 2 description lines, 3 target searches, tags.
   10. `## Test plan`: exact rules identical every run, runs planned, the `test-results.csv` columns to fill, the OBS check.
   11. `## Facts and sources`: each fact used with its `gta6-notes.md` line or tool output.
   12. `## What this run could not do`: every skipped step or tool and the exact reason, and whether `voice.md` was usable. Write "nothing skipped" if so.
2. Make the PDF: `uv run tools/make_pdf.py research/<slug>.md`. It prints the path of `output/<slug>.pdf`. If it prints an error, show it; the `.md` is still the result.
3. Reply to me with at most 8 lines: the PDF path, the chosen idea and title, your GO/NO-GO recommendation, what I must decide, and anything skipped. Do not paste the whole brief. End with the PDF path. Do not ask a question at the end.
