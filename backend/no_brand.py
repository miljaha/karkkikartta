import csv
import json
from collections import Counter

with open("stores.json", encoding="utf-8") as f:
    places = json.load(f)

nobrand = [p for p in places if not p.get("brand")]
print(f"{len(nobrand)} places without a brand\n")

print("Most common names:")
for name, count in Counter(p.get("name") or "(no name)" for p in nobrand).most_common(
    40
):
    print(f"{count:4}  {name}")

print("\nBy type:")
for t, count in Counter(p.get("type") for p in nobrand).most_common():
    print(f"{count:4}  {t}")

# names that start with a chain you might want to keep
keywords = [
    "prisma",
    "s-market",
    "k-citymarket",
    "k-supermarket",
    "k-market",
    "lidl",
    "tokmanni",
    "sale",
    "alepa",
]
print("\nNo-brand places whose name starts with a known chain:")
for kw in keywords:
    hits = [p for p in nobrand if (p.get("name") or "").lower().startswith(kw)]
    if hits:
        print(f"{len(hits):4}  {kw}")

# full list to browse
with open("no_brand.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "type", "lat", "lon"])
    for p in nobrand:
        writer.writerow([p.get("name"), p.get("type"), p["lat"], p["lon"]])
print("\nFull list saved to no_brand.csv")
