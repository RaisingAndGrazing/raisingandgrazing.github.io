"""Download current Etsy feed images and assemble five five-item vertical reels."""
import json, pathlib, urllib.request, xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "marketing_site" / "video_assets"
IMG = OUT / "product_images"
IMG.mkdir(parents=True, exist_ok=True)
feed = ET.parse(ROOT / "marketing_site" / "feed.xml").getroot()
ns = {"g": "http://base.google.com/ns/1.0"}
bad = {"4548091644", "4548077175"}
items = []
for item in feed.findall(".//item"):
    lid = item.findtext("g:id", namespaces=ns)
    if lid in bad:
        continue
    title = item.findtext("title") or ""
    image = item.findtext("g:image_link", namespaces=ns)
    if lid and image:
        items.append({"id": lid, "title": title, "image": image})
items = items[:25]
for i, entry in enumerate(items, 1):
    path = IMG / f"{i:02d}-{entry['id']}.jpg"
    if not path.exists():
        urllib.request.urlretrieve(entry["image"], path)
    entry["path"] = str(path)
groups = [items[i:i + 5] for i in range(0, 25, 5)]
(OUT / "reel_manifest.json").write_text(json.dumps(groups, indent=2), encoding="utf-8")
print(json.dumps([[x["id"] for x in group] for group in groups]))
