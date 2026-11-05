# GTA 6 channel

A YouTube channel that tests GTA 6 like a software engineer. Source plan: `../YouTube_Success_Roadmap.pdf`.

## Status
- Phase 1 (foundation): tooling and context files set up. The channel and brand are **not created yet** (Step 1). Channel name: TBD.
- Phase 2 (GTA 5 baseline tests) has **not started**. Do not design tests, write test scripts or plan videos around it unless I ask.
- GTA 6 launches 2026-11-19 (see `gta6-notes.md`). Phase 2 ends 2026-11-18.

## Strategy
Do not compete on speed or size. Be the channel that tests GTA 6 like a software engineer: a clear question, a fair test, a clear answer, with my own data.

## Identity
The masked developer with glowing `< >` eyes who runs experiments on GTA. Faceless: my voice is my face. I grew up without a PlayStation, earned one myself, and look at the game the way an engineer looks at a system: test it, measure it, explain it.

## Audience (draft - edit)
GTA fans who want measured results instead of first impressions or rumors.

## Content pillars
| Pillar | What it is | Example |
| --- | --- | --- |
| Experiments | A clear question, a fair test, a clear answer | "How smart are GTA 6's cops? I tested it." |
| Systems explained | How the game works, through an engineer's eyes | "How GTA 6's wanted system actually works." |
| Developer x AI | Stories only a developer can tell | "I built an AI to run my GTA channel." |
| Shorts | One surprising test result per Short | "GTA 6 cops arrive in 4 seconds?!" |

## What to avoid
- Chasing news and rumors. Big channels win those searches.
- Fake "secret" clickbait. It destroys trust fast.
- Story spoilers in titles or thumbnails during launch weeks.

## The rules (read before every video)
1. **Package first.** Write the title and sketch the thumbnail before recording. If it is not clickable, do not make the video.
2. **Win the first 30 seconds.** Show the stakes or the result immediately. No intro, no logo, no "hey guys".
3. **One clear idea per video.** A test with a clear question and a clear answer.
4. **Build a series, not just one-offs.** Recurring names bring viewers back.
5. **Shorts for discovery, long videos for depth.** Turn every long video into 2-3 Shorts.
6. **Your voice is your face.** On a faceless channel, energy and clarity on the mic carry everything.
7. **Comments are the idea database.** Every "can you test...?" is a free video idea.
8. **Consistency beats perfection.** A fixed schedule beats occasional masterpieces.

First 90 days: success means finishing videos and improving, not views. No quitting decisions before video 10. Compare only with my own previous videos.

## How Claude should work here
- Nothing publishes. Claude writes; I upload. End outputs with a block I can copy.
- Never invent a number, result or source. Test numbers come only from `test-results.csv`; GTA 6 facts only from `gta6-notes.md` (or search and cite, then update that file). Unknown GTA 6 features are asked as questions, never stated as claims.
- Read `~/.claude/youtube/voice.md` before writing anything in my voice. If its "How I actually talk" section is empty, say so and ask for samples. Do not guess a voice.
- Before using any new skill or tool, review its files for anything unsafe. Download tools only from their official site or GitHub page.
- Editing happens in **DaVinci Resolve** (not CapCut). Thumbnails are made by hand in Canva. Both are mine to operate; do not automate them.

## Files
| File | Purpose |
| --- | --- |
| `CLAUDE.md` | This file: identity, audience, rules |
| `gta6-notes.md` | GTA 6 facts with source + confidence. Ask Claude to search the web and update it |
| `test-results.csv` | One row per test run, every run I ever record (header only for now) |
| `PRE-VIDEO-GUIDE.md` | The research routine before every video (look at YouTube, idea, package, script, SEO, test plan). When I say "follow the pre-video guide", do it step by step and stop at each CHECKPOINT |
| `/pre-video <idea>` | One command: runs the whole guide unattended, writes the brief to `research/` and the PDF to `output/` (`.claude/commands/pre-video.md`) |
| `tools/collect.py` | Reads public YouTube data: search suggestions, niche outliers (feeds `/yt-viral`), comment requests |
| `tools/make_pdf.py` | Turns a brief `.md` into a PDF with Edge: `uv run tools/make_pdf.py research/<slug>.md` |
| `research/` | One brief (`.md`, the editable source) per video, plus the collected niche data |
| `output/` | The PDF of each brief, same file name |
| `schedule.md` | Weekly capacity + the ready-to-run `/yt-plan` prompt |
| `tools/transcribe.py` | faster-whisper transcription |
| `tools/bin/auto-editor.exe` | Silence removal / rough cut (v31.7.2, official GitHub release, SHA-256 verified) |
| `~/.claude/youtube/voice.md` | Voice profile every skill reads (draft) |

## Skills
YouTube Agent Skill pack (`youtube-agent`, project scope, reviewed at commit a2feb21): `/yt-viral`, `/yt-package`, `/yt-script`, `/yt-edit`, `/yt-shorts`, `/yt-seo`, `/yt-chapters`, `/yt-comment`, `/yt-plan`, `/yt-retention`, `/yt-audit`. If a bare name is not recognised use the namespaced form, e.g. `/youtube-agent:yt-plan`.

## Windows notes (this machine)
- **Use `python`, not `python3`.** `python3` here is the Microsoft Store stub and fails. The skill docs say `python3`; substitute `python` (3.12).
- `PYTHONUTF8=1` is set for this project in `.claude/settings.json`. Without it the plugin scripts read text files as cp1252 and silently corrupt emoji and arrows in titles (wrong character counts). If you run them by hand in a terminal outside Claude Code: `$env:PYTHONUTF8=1`.
- **Keep big files off C: (low space).** `UV_CACHE_DIR=D:\cache\uv` and `HF_HOME=D:\cache\huggingface` are set at user level and in `.claude/settings.json`, so uv environments and Whisper models download to D. Do not install heavy tools or models to C. (Only Claude Code's own ~20 MB `~/.claude` config stays on C.)
- Plugin scripts live under `~/.claude/plugins/cache/youtube-agent-skill/youtube-agent/<version>/skills/`.
- Create JSON inputs (e.g. for `/yt-viral`) as plain UTF-8 without BOM. Windows PowerShell 5.1 `>` and `Set-Content -Encoding utf8` write UTF-16 or a BOM, which `swipe.py` rejects.

## Production pipeline (Phase 4 loop)
1. **Record**: OBS Studio. Simple output, Hybrid MP4, 1080p60, saved to `D:\obsVideo`. Capture card (CM700) for PS5; direct capture for PC.
2. **Transcribe**: `uv run tools/transcribe.py "D:\obsVideo\<clip>.mp4"` writes `<clip>.srt` and `<clip>.json` next to it. First run downloads the model (about 1.6 GB). GPU if it works, CPU otherwise. `--translate` outputs English text from other languages.
3. **Rough cut**: `/yt-edit` on the transcript to see the cuts, then `tools\bin\auto-editor.exe "D:\obsVideo\<clip>.mp4" --edit audio:0.04 --margin 0.2sec --export resolve -o "D:\obsVideo\<clip>_rough"` writes `<clip>_rough.fcpxml` (it links the original file; nothing is re-encoded). Import it in DaVinci Resolve (File > Import > Timeline). **Always review the cuts before trusting them.**
   - OBS currently records one mixed audio track (mic + game). Game audio is rarely silent, so on gameplay the threshold cuts little; on a quiet clip it can cut most of it (a real 4:39 test clip came out 92% removed). Two fixes, neither applied yet: (a) run auto-editor on the separate voiceover recording (the Saturday voiceover block in `schedule.md`), or (b) switch OBS to Advanced output with the mic on its own track, then use `--edit audio:stream=<mic track index from "auto-editor info">`.
4. **Final edit**: DaVinci Resolve (pacing, zooms, captions, sound). Shorts: crop to vertical in Resolve.
5. Upload (`/yt-seo`, `/yt-chapters`; A/B test up to 3 titles or thumbnails in YouTube Studio desktop), engage (`/yt-comment`), review after a week (`/yt-retention`) and write one lesson.
