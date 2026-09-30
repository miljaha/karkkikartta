from flask import Flask, jsonify, render_template, request
from datetime import datetime, date, timezone
from models import db, Campaign, Store, PriceUpdate
from prices import price_summary

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///candy.db"
db.init_app(app)


@app.route("/api/stores/<int:store_id>/update-price", methods=["POST"])
def update_price(store_id):
    store = Store.query.get_or_404(store_id)
    data = request.get_json()

    price_type = data.get("type")
    price = data.get("price")

    if price_type not in ("base", "campaign"):
        return jsonify({"error": "type must be 'base' or 'campaign'"}), 400
    if price is None or price <= 0 or price > 100:
        return jsonify({"error": "price must be a positive number below 100"}), 400
    if price_type == "base":
        store.base_price = price
        store.base_updated_at = datetime.now(timezone.utc)
        update = PriceUpdate(store_id=store.id, price_type="base", price=price)

    else:  # campaign price
        start_date_str = data.get("start_date")
        end_date_str = data.get("end_date")
        if not start_date_str or not end_date_str:
            return jsonify({"error": "campaign requires start_date and end_date"}), 400

        start_date = date.fromisoformat(start_date_str)
        end_date = date.fromisoformat(end_date_str)
        if end_date < start_date:
            return jsonify({"error": "end_date must be after start_date"}), 400

        is_chain_wide = bool(data.get("is_chain_wide", False))
        requires_membership = bool(data.get("requires_membership", False))

        campaign = Campaign(
            store_id=store.id,
            price=price,
            start_date=start_date,
            end_date=end_date,
            is_chain_wide=is_chain_wide,
            requires_membership=requires_membership,
        )
        db.session.add(campaign)

        update = PriceUpdate(
            store_id=store.id,
            price_type="campaign",
            price=price,
            start_date=start_date,
            end_date=end_date,
            is_chain_wide=is_chain_wide,
            requires_membership=requires_membership,
        )
    db.session.add(update)
    db.session.commit()
    return jsonify(price_summary(store))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/stores")
def api_stores():
    stores = Store.query.all()
    result = []
    for store in stores:
        summary = price_summary(store)
        result.append(
            {
                "id": store.id,
                "name": store.name,
                "address": store.address,
                "latitude": store.latitude,
                "longitude": store.longitude,
                "chain": store.chain,
                "candy_provider": store.candy_provider,
                "price": summary["price"],
                "is_campaign": summary["is_campaign"],
                "member_price": summary["member_price"],
            }
        )
    return jsonify(result)


if __name__ == "__main__":
    print("Starting server...")
    app.run(debug=True)
