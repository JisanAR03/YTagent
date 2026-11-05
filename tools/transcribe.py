# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "faster-whisper",
#   "av<17",  # faster-whisper 1.2.1 passes av.open(metadata_errors=...), which PyAV 19 rejects
#   "nvidia-cublas-cu12; sys_platform == 'win32'",
#   "nvidia-cudnn-cu12==9.*; sys_platform == 'win32'",
# ]
# ///
"""transcribe.py - local transcription with faster-whisper (free, runs on this laptop).

    uv run tools/transcribe.py recording.mp4
    uv run tools/transcribe.py recording.mp4 --translate     # speech in any language -> English text
    uv run tools/transcribe.py recording.mp4 --device cpu    # force CPU

Writes <name>.srt and <name>.json next to the recording (or into --out). The .json is
{"language": ..., "segments": [{"start", "end", "text"}]}, the shape /yt-edit and /yt-chapters read.
Uses the GPU when it works and falls back to CPU (int8) on its own.
"""
import argparse, json, os, sys, time

os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")


def add_cuda_dlls():
    # pip's nvidia-* wheels put cuBLAS/cuDNN under site-packages/nvidia/<lib>/bin, which Windows does not search.
    if sys.platform != "win32":
        return
    for base in sys.path:
        nv = os.path.join(base, "nvidia")
        if os.path.isdir(nv):
            for lib in os.listdir(nv):
                d = os.path.join(nv, lib, "bin")
                if os.path.isdir(d):
                    os.add_dll_directory(d)
                    os.environ["PATH"] = d + os.pathsep + os.environ["PATH"]


def stamp(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def transcribe(path, model_name, device, compute, task, language):
    from faster_whisper import WhisperModel
    model = WhisperModel(model_name, device=device, compute_type=compute)
    segs, info = model.transcribe(path, task=task, language=language, vad_filter=True,
                                  vad_parameters={"min_silence_duration_ms": 500})
    # transcribe() is lazy: GPU/DLL problems only surface while this list is built, inside the caller's try.
    rows = [{"start": round(s.start, 3), "end": round(s.end, 3), "text": s.text.strip()} for s in segs]
    return info.language, rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("media")
    ap.add_argument("--model", help="default: large-v3-turbo (large-v3 with --translate; turbo cannot translate)")
    ap.add_argument("--device", choices=["auto", "cuda", "cpu"], default="auto")
    ap.add_argument("--translate", action="store_true", help="output English text whatever language is spoken")
    ap.add_argument("--language", help="e.g. en. Default: auto-detect")
    ap.add_argument("--out", help="output folder (default: next to the media file)")
    a = ap.parse_args()
    if not os.path.exists(a.media):
        sys.exit(f"not found: {a.media}")
    model = a.model or ("large-v3" if a.translate else "large-v3-turbo")
    task = "translate" if a.translate else "transcribe"
    add_cuda_dlls()
    plans = [("cuda", "float16"), ("cpu", "int8")] if a.device == "auto" else \
            [("cuda", "float16")] if a.device == "cuda" else [("cpu", "int8")]
    t0 = time.time()
    for i, (device, compute) in enumerate(plans):
        try:
            lang, rows = transcribe(a.media, model, device, compute, task, a.language)
            break
        except Exception as e:
            if i == len(plans) - 1:
                raise
            print(f"[{device} failed: {e}] falling back to cpu", file=sys.stderr)
    out = a.out or os.path.dirname(os.path.abspath(a.media))
    os.makedirs(out, exist_ok=True)
    stem = os.path.join(out, os.path.splitext(os.path.basename(a.media))[0])
    with open(stem + ".json", "w", encoding="utf-8") as f:
        json.dump({"language": lang, "segments": rows}, f, ensure_ascii=False, indent=1)
    with open(stem + ".srt", "w", encoding="utf-8") as f:
        for n, r in enumerate(rows, 1):
            f.write(f"{n}\n{stamp(r['start'])} --> {stamp(r['end'])}\n{r['text']}\n\n")
    print(f"{model} on {device}/{compute}, {task}, language={lang}, {len(rows)} segments, {time.time() - t0:.1f}s")
    print(stem + ".srt")
    print(stem + ".json")


if __name__ == "__main__":
    main()
