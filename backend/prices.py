from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy import or_, and_
from models import Store, Campaign

HELSINKI = ZoneInfo("Europe/Helsinki")

def active_campaigns(store, today):
    # campaigns reported for this store
    conditions = [Campaign.store_id == store.id]
    # ...or chain-wide ones
    if store.chain:
        conditions.append(and_(Campaign.is_chain_wide == True,
                               Store.chain == store.chain))
    return (Campaign.query
            .join(Store, Campaign.store_id == Store.id)
            .filter(Campaign.start_date <= today, Campaign.end_date >= today)
            .filter(or_(*conditions))
            .all())

def price_summary(store):
    today = datetime.now(HELSINKI).date()
    campaigns = active_campaigns(store, today)

    # if several overlap: store-specific beats chain-wide, then newest wins
    def pick(cs):
        return max(cs, key=lambda c: (c.store_id == store.id, c.created_at)) if cs else None

    public = pick([c for c in campaigns if not c.requires_membership])
    member = pick([c for c in campaigns if c.requires_membership])

    return {
        "price": public.price if public else store.base_price,
        "is_campaign": public is not None,
        "member_price": member.price if member else None,
    }
