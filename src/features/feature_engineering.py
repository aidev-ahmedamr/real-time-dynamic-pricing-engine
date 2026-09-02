import pandas as pd


def add_features(df):
    df = df.copy()

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values(["product_id", "timestamp"])

    df["price_ratio_to_competitor"] = df["current_price"] / df["competitor_price"]
    df["price_difference"] = df["current_price"] - df["competitor_price"]
    df["profit_margin"] = (df["current_price"] - df["cost_price"]) / df["current_price"]
    df["inventory_ratio"] = (
        df["inventory_level"] / df.groupby("product_id")["inventory_level"].transform("max")
    )
    df["cart_to_view_ratio"] = df["add_to_cart_count"] / df["views_last_hour"].clip(lower=1)

    if "demand" in df.columns:
        df["avg_demand_3"] = (
            df.groupby("product_id")["demand"]
            .transform(lambda x: x.rolling(window=3, min_periods=1).mean())
        )
        df["avg_demand_7"] = (
            df.groupby("product_id")["demand"]
            .transform(lambda x: x.rolling(window=7, min_periods=1).mean())
        )
        df["demand_lag_1"] = df.groupby("product_id")["demand"].shift(1)
        df["demand_lag_1"] = df["demand_lag_1"].fillna(df["demand"].median())
    else:
        df["avg_demand_3"] = df.get("avg_demand_3", 0)
        df["avg_demand_7"] = df.get("avg_demand_7", 0)
        df["demand_lag_1"] = df.get("demand_lag_1", 0)

    return df


if __name__ == "__main__":
    raw = pd.read_csv("data/raw/dynamic_pricing_raw.csv")
    processed = add_features(raw)
    processed.to_csv("data/processed/dynamic_pricing_processed.csv", index=False)
    print(f"Saved {len(processed)} rows to data/processed/dynamic_pricing_processed.csv")
