"""Fetch Finnish grocery stores from OpenStreetMap and save them to stores.json.

Run this once, then again whenever you want fresh data (e.g. weekly):
    python fetch_stores.py
"""

import json
import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

QUERY = """
[out:json][timeout:180];
area["ISO3166-1"="FI"][admin_level=2]->.fi;
nwr["shop"~"^(supermarket|convenience)$"](area.fi);
out center tags;
"""


def main():
    response = requests.post(
        OVERPASS_URL,
        data={"data": QUERY},
        headers={"User-Agent": "finland-grocery-map/0.1 (hobby project)"},
        timeout=200,
    )
    response.raise_for_status()

    stores = []
    for element in response.json()["elements"]:
        # Nodes have lat/lon directly; ways and relations have a "center".
        point = element if element["type"] == "node" else element.get("center")
        if not point:
            continue
        tags = element.get("tags", {})
        stores.append(
            {
                "id": f"{element['type']}/{element['id']}",
                "lat": point["lat"],
                "lon": point["lon"],
                "name": tags.get("name") or tags.get("brand") or "Grocery store",
                "brand": tags.get("brand"),
                "type": tags.get("shop"),
                "opening_hours": tags.get("opening_hours"),
            }
        )

    with open("stores.json", "w", encoding="utf-8") as f:
        json.dump(stores, f, ensure_ascii=False)

    print(f"Saved {len(stores)} stores to stores.json")


if __name__ == "__main__":
    main()
