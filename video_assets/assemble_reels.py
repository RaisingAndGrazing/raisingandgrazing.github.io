"""Assemble five 15-second vertical product reels from the manifest."""
import json, pathlib, subprocess

HERE = pathlib.Path(__file__).resolve().parent
groups = json.loads((HERE / "reel_manifest.json").read_text(encoding="utf-8"))
for number, group in enumerate(groups, 1):
    concat = HERE / f"reel-{number}.txt"
    lines = []
    for item in group:
        path = pathlib.Path(item["path"])
        lines += [f"file '{path.as_posix()}'", "duration 3"]
    lines.append(f"file '{path.as_posix()}'")
    concat.write_text("\n".join(lines) + "\n", encoding="utf-8")
    output = HERE / f"raising-grazing-reel-{number}.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=#f5efe5,format=yuv420p",
        "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-movflags", "+faststart", str(output)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(output.name)
