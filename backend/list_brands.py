import json
from collections import Counter

with open("stores.json", encoding="utf-8") as f:
    places = json.load(f)

print(f"{len(places)} places in total\n")

for brand, count in Counter(
    p.get("brand") or "(no brand)" for p in places
).most_common():
    print(f"{count:5}  {brand}")

print("\nBy type:")
for t, count in Counter(p.get("type") for p in places).most_common():
    print(f"{count:5}  {t}")
