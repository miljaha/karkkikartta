import csv
from app import app
from models import db, Store

with app.app_context():
    with open("geocoded_stores.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["latitude"] and row["longitude"]:
                store = Store(
                    name=row["name"],
                    address=row["address"],
                    chain=row["chain"],
                    latitude=float(row["latitude"]),
                    longitude=float(row["longitude"]),
                    base_price=None,
                )
                db.session.add(store)
        db.session.commit()
    print("Done!")
