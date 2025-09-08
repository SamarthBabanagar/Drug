import json
import qrcode
from pathlib import Path

# Update this if your Pages URL ever changes
BASE_URL = "https://SamarthBabanagar.github.io/Drug/drug.html?id="

with open("drugs.json", "r", encoding="utf-8") as f:
    drugs = json.load(f)

out_dir = Path(".")
count = 0
for drug_id in drugs.keys():
    url = BASE_URL + drug_id
    img = qrcode.make(url)
    filename = out_dir / f"{drug_id}_qrcode.png"
    img.save(filename)
    count += 1
    print(f"QR generated: {filename.name} -> {url}")

print(f"\nDone. Generated {count} QR code(s).")
