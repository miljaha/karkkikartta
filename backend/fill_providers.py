from app import app
from models import db, Store
from providers import default_provider

with app.app_context():
    changed = 0
    for s in Store.query.all():
        provider = default_provider(s.chain) if s.has_loose_candy else None
        if s.candy_provider != provider:
            s.candy_provider = provider
            changed += 1
    db.session.commit()
    print(f"Updated {changed} stores")
