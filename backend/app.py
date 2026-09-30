from flask import Flask, jsonify, render_template
from models import Store, db
from prices import price_summary

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///candy.db"
db.init_app(app)


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
