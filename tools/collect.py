#!/usr/bin/env python3
"""collect.py - read public YouTube data for pre-video research. Never logs in, never posts.

    python tools/collect.py suggest "gta 5 police"
    python tools/collect.py niche "gta 5 police chase test" --channels 8 --videos 30 -o research/niche.json
    python tools/collect.py comments https://www.youtube.com/watch?v=VIDEO_ID --max 300

suggest   what people actually type into YouTube search (autocomplete). Standard library only.
niche     finds the channels that rank for a query, pulls each one's recent videos, and writes the file
          /yt-viral ranks: [{"channel","title","views","url","duration"}]. Needs yt-dlp.
comments  a video's top comments plus the ones that look like requests ("can you test...?"). Needs yt-dlp.

yt-dlp is looked for at tools/bin/yt-dlp.exe, then on PATH.
"""
import argparse, json, os, re, shutil, subprocess, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REQUEST = re.compile(r"\b(can|could|would|will) you\b|\bplease\b|\btest\b|\btry\b|\bwhat if\b|\bhow (does|would|do)\b", re.I)


def ytdlp(*args):
    exe = os.path.join(HERE, "bin", "yt-dlp.exe")
    exe = exe if os.path.exists(exe) else shutil.which("yt-dlp")
    if not exe:
        sys.exit("yt-dlp not found. Put yt-dlp.exe in tools/bin (official release: github.com/yt-dlp/yt-dlp/releases).")
    r = subprocess.run([exe, "--no-warnings", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        sys.exit("yt-dlp failed: " + (r.stderr.strip().splitlines() or ["no message"])[-1])
    return json.loads(r.stdout)


def suggest(seed, top, region):
    queries = [seed] + [f"{seed} {c}" for c in "abcdefghijklmnopqrstuvwxyz"] + \
              [f"{w} {seed}" for w in ("how", "why", "can", "does", "is", "what")]
    seen = []
    for q in queries:
        url = f"https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&hl=en&gl={region}&q=" + urllib.parse.quote(q)
        try:
            with urllib.request.urlopen(url, timeout=15) as f:
                for s in json.loads(f.read().decode("utf-8"))[1]:
                    if s not in seen:
                        seen.append(s)
        except Exception as e:
            print(f"[skipped '{q}': {e}]", file=sys.stderr)
        time.sleep(0.15)
    ranked = seen[:10]   # the first query is YouTube's own popularity order; the rest is letter-by-letter
    print(f"\nMOST TYPED after '{seed}' (YouTube's own order):")
    for s in ranked:
        print("  " + s)
    print(f"\nMORE ideas, grouped by next letter / question word ({len(seen) - len(ranked)} found, showing {top}):")
    for s in seen[len(ranked):len(ranked) + top]:
        print("  " + s)


def niche(query, n_channels, n_videos, out):
    found = ytdlp("--flat-playlist", "-J", f"ytsearch{n_channels * 6}:{query}")
    channels = {}
    for e in found.get("entries", []):
        url = e.get("channel_url") or e.get("uploader_url")
        if url and url not in channels:
            channels[url] = e.get("channel") or e.get("uploader") or url
        if len(channels) >= n_channels:
            break
    if not channels:
        sys.exit("no channels found for that query")
    rows = []
    for url, name in channels.items():
        print(f"  reading {name} ...", file=sys.stderr)
        data = ytdlp("--flat-playlist", "--playlist-end", str(n_videos), "-J", url.rstrip("/") + "/videos")
        for e in data.get("entries", []):
            if e.get("view_count") is None:
                continue
            rows.append({"channel": name, "title": e.get("title", ""), "views": e["view_count"],
                         "url": e.get("url") or "https://www.youtube.com/watch?v=" + e.get("id", ""),
                         "duration": e.get("duration")})
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)
    print(f"{len(rows)} videos from {len(channels)} channels -> {out}")
    print("next: /yt-viral " + out)


def comments(url, mx):
    data = ytdlp("--skip-download", "--write-comments", "--extractor-args", f"youtube:max_comments={mx}", "-J", url)
    top = [c for c in data.get("comments", []) if c.get("parent") == "root"]
    print(f"\n{data.get('title', url)}\n{len(top)} top-level comments read\n")
    print("MOST LIKED")
    for c in sorted(top, key=lambda c: -(c.get("like_count") or 0))[:10]:
        print(f"  {c.get('like_count') or 0:>6}  {c.get('text', '').strip()[:160]!r}")
    asks = [c for c in top if REQUEST.search(c.get("text", "")) and "?" in c.get("text", "")]
    print(f"\nLOOK LIKE REQUESTS ({len(asks)})  <- free video ideas")
    for c in sorted(asks, key=lambda c: -(c.get("like_count") or 0))[:20]:
        print(f"  {c.get('like_count') or 0:>6}  {c.get('text', '').strip()[:160]!r}")


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("suggest"); s.add_argument("seed"); s.add_argument("--top", type=int, default=40)
    s.add_argument("--region", default="us", help="country code, default us (English-speaking GTA audience); bd = Bangladesh")
    n = sub.add_parser("niche"); n.add_argument("query")
    n.add_argument("--channels", type=int, default=8); n.add_argument("--videos", type=int, default=30)
    n.add_argument("-o", "--out", default="research/niche.json")
    c = sub.add_parser("comments"); c.add_argument("url"); c.add_argument("--max", type=int, default=300)
    a = ap.parse_args()
    if a.cmd == "suggest":
        suggest(a.seed, a.top, a.region)
    elif a.cmd == "niche":
        niche(a.query, a.channels, a.videos, a.out)
    else:
        comments(a.url, a.max)


if __name__ == "__main__":
    main()
