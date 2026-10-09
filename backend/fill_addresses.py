import time
import requests
from sqlalchemy import or_
from app import app
from models import db, Store

LIMIT = None  # test with a few stores first; set to None to do everything

HEADERS = {
    "User-Agent": "karkille-fi candy price map (personal project, miljaemilia.harju@hotmail.fi)"
}


def reverse_geocode(lat, lon):
    resp = requests.get(
        "https://nominatim.openstreetmap.org/reverse",
        params={
            "lat": lat,
            "lon": lon,
            "format": "jsonv2",
            "addressdetails": 1,
            "zoom": 18,
            "accept-language": "fi",
        },
        headers=HEADERS,
        timeout=20,
    )
    resp.raise_for_status()
    a = resp.json().get("address", {})
    road = a.get("road")
    if not road:
        return None
    street = f"{road} {a['house_number']}" if a.get("house_number") else road
    place = a.get("city") or a.get("town") or a.get("village") or a.get("municipality")
    city_part = " ".join(x for x in [a.get("postcode"), place] if x)
    return ", ".join(x for x in [street, city_part] if x)


with app.app_context():
    query = Store.query.filter(or_(Store.address.is_(None), Store.address == ""))
    stores = query.limit(LIMIT).all() if LIMIT else query.all()
    print(f"{len(stores)} stores to fill in")

    try:
        for i, s in enumerate(stores, 1):
            try:
                addr = reverse_geocode(s.latitude, s.longitude)
            except requests.RequestException as e:
                print(f"{i}: error for {s.name}: {e}")
                time.sleep(5)
                continue
            if addr:
                s.address = addr
            print(f"{i}/{len(stores)}  {s.name}  ->  {addr}")
            if i % 25 == 0:
                db.session.commit()  # save progress as we go
            time.sleep(1.1)  # Nominatim allows 1 request per second
    finally:
        db.session.commit()  # also saves if you stop it with Ctrl+C
        print("Saved.")
