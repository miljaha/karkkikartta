import json
import re
from collections import Counter
from app import app
from models import db, Store


DRY_RUN = False  # first run just previews; set to False to actually save

CHAINS = [
    "K-Market",
    "S-market",
    "Sale",
    "K-Supermarket",
    "Lidl",
    "Alepa",
    "K-Citymarket",
    "Prisma",
]

# whole-word, case-insensitive, so "Sale" doesn't match inside other words
PATTERNS = {
    c: re.compile(rf"(?<!\w){re.escape(c)}(?!\w)", re.IGNORECASE) for c in CHAINS
}


def find_chain(place):
    brand = place.get("brand") or ""
    name = place.get("name") or ""
    for chain in CHAINS:  # 1) exact brand tag
        if brand.lower() == chain.lower():
            return chain, "brand"
    for chain in CHAINS:  # 2) chain name appears in brand/name text
        if PATTERNS[chain].search(f"{brand} {name}"):
            return chain, "name"
    return None, None


with open("stores.json", encoding="utf-8") as f:
    places = json.load(f)

selected = []
for p in places:
    chain, how = find_chain(p)
    if chain:
        selected.append((p, chain, how))

by_name = [(p, c) for p, c, how in selected if how == "name"]
print(
    f"{len(selected)} of {len(places)} places match ({len(by_name)} matched by name only)"
)

print("\nMatched by name (sample, check these look right):")
for p, c in by_name[:15]:
    print(f"  {p.get('brand') or '-':12} | {p.get('name')}  ->  {c}")

print("\nPer chain:")
for chain, n in Counter(c for _, c, _ in selected).most_common():
    print(f"{n:5}  {chain}")

if DRY_RUN:
    print("\nDry run, nothing saved. Set DRY_RUN = False to load.")
else:
    with app.app_context():
        existing = {
            (s.name, round(s.latitude, 5), round(s.longitude, 5))
            for s in Store.query.all()
        }
        added = 0
        for p, chain, _ in selected:
            name = p.get("name") or chain
            key = (name, round(p["lat"], 5), round(p["lon"], 5))
            if key in existing:
                continue
            db.session.add(
                Store(
                    name=name,
                    chain=chain,
                    latitude=p["lat"],
                    longitude=p["lon"],
                    base_price=None,
                )
            )
            existing.add(key)
            added += 1
        db.session.commit()
        print(f"\nAdded {added} new stores")
