"""
Runs a live loop: generates a market event for a random product,
updates that product's state, and sends it to the running API for
pricing. This is what makes the project actually "real-time" instead
of just a one-off script.

Run this AFTER the API is running (docker-compose up, or
`uvicorn api.main:app --reload` from the project root):

    python -m src.streaming.run_simulation
"""

import time
import random
import requests

from src.data.generate_data import generate_products
from src.streaming.event_simulator import generate_event
from src.streaming.product_state import update_product_state

API_URL = "http://localhost:8000/optimize-price"
NUM_PRODUCTS = 10
SLEEP_SECONDS = 2


def build_initial_state(product):
    """Turn a generated product row into the full payload the API needs."""

    current_price = product["base_price"]
    competitor_price = product["base_price"] * random.uniform(0.9, 1.1)

    state = {
        "product_id": product["product_id"],
        "base_price": product["base_price"],
        "cost_price": product["cost_price"],
        "current_price": current_price,
        "competitor_price": competitor_price,
        "inventory_level": product["initial_inventory"],
        "views_last_hour": 20,
        "add_to_cart_count": 3,
        "hour": 12,
        "day_of_week": 0,
        "month": 1,
        "is_weekend": 0,
        "rating": product["rating"],
        "num_reviews": product["num_reviews"],
        "conversion_rate": 0.1,
        "_initial_inventory": product["initial_inventory"],
        "_demand_history": [],
    }

    return state


def compute_live_features(state):
    """Recompute the engineered features the model expects, for one product."""

    payload = {k: v for k, v in state.items() if not k.startswith("_")}

    payload["price_ratio_to_competitor"] = (
        payload["current_price"] / payload["competitor_price"]
    )
    payload["price_difference"] = (
        payload["current_price"] - payload["competitor_price"]
    )
    payload["profit_margin"] = (
        (payload["current_price"] - payload["cost_price"])
        / payload["current_price"]
    )
    payload["inventory_ratio"] = (
        payload["inventory_level"] / max(1, state["_initial_inventory"])
    )
    payload["cart_to_view_ratio"] = (
        payload["add_to_cart_count"] / max(1, payload["views_last_hour"])
    )

    history = state["_demand_history"]
    payload["avg_demand_3"] = (
        sum(history[-3:]) / len(history[-3:]) if history else 0
    )
    payload["avg_demand_7"] = (
        sum(history[-7:]) / len(history[-7:]) if history else 0
    )
    payload["demand_lag_1"] = history[-1] if history else 0

    return payload


def run():
    products = generate_products(n_per_category=2).to_dict("records")
    states = {p["product_id"]: build_initial_state(p) for p in products[:NUM_PRODUCTS]}

    print(f"Simulating {len(states)} products. Press Ctrl+C to stop.\n")

    while True:
        product_id = random.choice(list(states.keys()))
        state = states[product_id]

        event = generate_event(product_id)
        updated = update_product_state(state, event)
        updated["_initial_inventory"] = state["_initial_inventory"]
        updated["_demand_history"] = state["_demand_history"]
        states[product_id] = updated

        payload = compute_live_features(updated)

        try:
            response = requests.post(API_URL, json=payload, timeout=5)
            response.raise_for_status()
            decision = response.json()

            states[product_id]["_demand_history"].append(
                decision["predicted_demand"]
            )
            states[product_id]["current_price"] = decision["recommended_price"]

            print(
                f"[{event['event_type']}] {product_id}: "
                f"price {decision['current_price']} -> {decision['recommended_price']} "
                f"({decision['action']}) | {', '.join(decision['reasons'])}"
            )

        except requests.exceptions.RequestException as e:
            print(f"Could not reach API ({API_URL}): {e}")

        time.sleep(SLEEP_SECONDS)


if __name__ == "__main__":
    run()
