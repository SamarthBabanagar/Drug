import json
import qrcode
from pathlib import Path

# ---- SETTINGS ----
# Make sure this matches your GitHub Pages URL structure
BASE_URL = "https://SamarthBabanagar.github.io/Drug/drug.html?id="

# ---- LOAD JSON ----
with open("drugs.json", "r", encoding="utf-8") as f:
    drugs = json.load(f)

# ---- GENERATE CODES ----
out_dir = Path(".")  # save PNGs in repo root to match index.html
count = 0
for drug_id in drugs.keys():
    url = BASE_URL + drug_id
    img = qrcode.make(url)
    filename = out_dir / f"{drug_id}_qrcode.png"
    img.save(filename)
    count += 1
    print(f"QR generated: {filename.name} -> {url}")

print(f"\n✅ Done! Generated {count} QR code(s).")
