import json
import qrcode

# GitHub Pages base URL
BASE_URL = "https://SamarthBabanagar.github.io/Drug/drug.html?id="

# Load your drugs.json file
with open("drugs.json", "r") as f:
    drugs = json.load(f)

# Generate QR code for each drug
for drug_id in drugs:
    url = BASE_URL + drug_id
    qr = qrcode.make(url)
    filename = f"{drug_id}_qrcode.png"
    qr.save(filename)
    print(f"Generated {filename} → {url}")
