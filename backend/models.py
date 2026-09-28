from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime, timezone

db = SQLAlchemy()

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    chain = db.Column(db.String(100))  # e.g. "Prisma", "K-Citymarket"
    address = db.Column(db.String(200))
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    candy_provider = db.Column(db.String(100))
    base_price = db.Column(db.Float, nullable=False)
    base_updated_at = db.Column(db.DateTime,default=lambda: datetime.now(timezone.utc))

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    is_chain_wide = db.Column(db.Boolean, nullable=False, default=False)
    requires_membership = db.Column(db.Boolean, nullable=False, default=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class PriceUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    price_type = db.Column(db.String(10), nullable=False)  # "base" or "campaign"
    price = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.Date)   # only used for campaign updates
    end_date = db.Column(db.Date)     # only used for campaign updates
    submitted_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_chain_wide = db.Column(db.Boolean, default=False)
    requires_membership = db.Column(db.Boolean, default=False)
