import numpy as np
import pandas as pd


CATEGORIES = {
    "Electronics": {"base_price_range": (50, 1500), "elasticity": 1.3},
    "Fashion": {"base_price_range": (20, 250), "elasticity": 1.8},
    "Home & Kitchen": {"base_price_range": (30, 500), "elasticity": 1.4},
    "Sports": {"base_price_range": (15, 1000), "elasticity": 1.5},
    "Beauty": {"base_price_range": (10, 300), "elasticity": 1.6},
}


def generate_products(n_per_category=100, seed=42):
    rng = np.random.default_rng(seed)
    products = []
    product_id = 1

    for category, info in CATEGORIES.items():
        for i in range(n_per_category):
            base_price = round(rng.uniform(*info["base_price_range"]), 2)
            cost_price = round(base_price * rng.uniform(0.4, 0.75), 2)

            products.append({
                "product_id": f"P{product_id:05d}",
                "product_name": f"{category}_Product_{i + 1}",
                "category": category,
                "base_price": base_price,
                "cost_price": cost_price,
                "price_elasticity": info["elasticity"],
                "initial_inventory": int(rng.integers(50, 500)),
                "rating": round(rng.uniform(3.0, 5.0), 2),
                "num_reviews": int(rng.integers(10, 5000)),
            })
            product_id += 1

    return pd.DataFrame(products)


def generate_record(product, timestamp, rng):
    hour = timestamp.hour
    day_of_week = timestamp.dayofweek
    month = timestamp.month
    is_weekend = int(day_of_week >= 5)

    seasonal_factor = 1.0
    if month in (11, 12):
        seasonal_factor = 1.3
    elif month in (6, 7, 8):
        seasonal_factor = 1.1

    traffic_factor = 1.0
    if 18 <= hour <= 23:
        traffic_factor = 1.5
    elif 8 <= hour <= 10:
        traffic_factor = 1.2

    competitor_price = product["base_price"] * rng.uniform(0.85, 1.15)
    current_price = product["base_price"] * rng.uniform(0.75, 1.25)
    inventory_level = int(rng.integers(5, max(6, product["initial_inventory"])))

    views_last_hour = int(rng.poisson(50 * traffic_factor * seasonal_factor))
    add_to_cart_count = int(views_last_hour * rng.uniform(0.05, 0.25))

    price_ratio = current_price / product["base_price"]
    price_effect = price_ratio ** (-product["price_elasticity"])
    competitor_effect = (competitor_price / current_price) ** 0.8
    inventory_factor = min(1.2, max(0.3, inventory_level / 100))

    base_demand = 10
    demand = (
        base_demand * price_effect * competitor_effect * traffic_factor
        * seasonal_factor * inventory_factor * rng.uniform(0.7, 1.3)
    )
    demand = max(0, int(demand))
    conversion_rate = demand / max(views_last_hour, 1)

    return {
        "timestamp": timestamp,
        "product_id": product["product_id"],
        "category": product["category"],
        "base_price": product["base_price"],
        "cost_price": product["cost_price"],
        "current_price": round(current_price, 2),
        "competitor_price": round(competitor_price, 2),
        "inventory_level": inventory_level,
        "views_last_hour": views_last_hour,
        "add_to_cart_count": add_to_cart_count,
        "hour": hour,
        "day_of_week": day_of_week,
        "month": month,
        "is_weekend": is_weekend,
        "rating": product["rating"],
        "num_reviews": product["num_reviews"],
        "conversion_rate": round(conversion_rate, 4),
        "demand": demand,
    }


def generate_dataset(n_products=100, start_date="2025-01-01", end_date="2025-12-31",
                      freq="12h", seed=42):
    rng = np.random.default_rng(seed)
    products_df = generate_products(seed=seed)
    sample_products = products_df.sample(
        n=min(n_products, len(products_df)), random_state=seed
    ).to_dict("records")
    sample_dates = pd.date_range(start=start_date, end=end_date, freq=freq)

    records = [
        generate_record(product, timestamp, rng)
        for product in sample_products
        for timestamp in sample_dates
    ]
    return pd.DataFrame(records)


if __name__ == "__main__":
    data = generate_dataset()
    data.to_csv("data/raw/dynamic_pricing_raw.csv", index=False)
    print(f"Saved {len(data)} rows to data/raw/dynamic_pricing_raw.csv")
