import csv
import time
import requests

HEADERS = {"User-Agent": "candy-price-map (personal project, your-email@example.com)"}


def geocode(address):
    resp = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params={"q": f"{address}, Finland", "format": "json", "limit": 1},
        headers=HEADERS,
    )
    results = resp.json()
    if results:
        return float(results[0]["lat"]), float(results[0]["lon"])
    return None, None


with (
    open("all_stores.csv") as infile,
    open("geocoded_stores.csv", "w", newline="", encoding="utf-8") as outfile,
):
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(
        outfile, fieldnames=["name", "address", "chain", "latitude", "longitude"]
    )
    writer.writeheader()
    for row in reader:
        lat, lon = geocode(row["address"])
        row["latitude"] = lat
        row["longitude"] = lon
        writer.writerow(row)
        print(f"{row['name']}: {lat}, {lon}")
        time.sleep(1)  # Nominatim's rate limit
