import random
from datetime import datetime


EVENT_TYPES = [
    "PRODUCT_VIEW",
    "ADD_TO_CART",
    "PURCHASE",
    "COMPETITOR_PRICE_CHANGE",
    "INVENTORY_UPDATE"
]


def generate_event(product_id):

    event_type = random.choice(EVENT_TYPES)

    event = {
        "event_id": f"EVT-{random.randint(100000, 999999)}",
        "event_type": event_type,
        "product_id": product_id,
        "timestamp": datetime.utcnow().isoformat()
    }

    if event_type == "COMPETITOR_PRICE_CHANGE":

        event["price_change_percentage"] = round(
            random.uniform(-0.10, 0.10),
            3
        )

    if event_type == "INVENTORY_UPDATE":

        event["inventory_change"] = random.randint(
            -20,
            20
        )

    return event
