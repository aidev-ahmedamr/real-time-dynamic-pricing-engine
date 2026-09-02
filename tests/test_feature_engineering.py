import pandas as pd

from src.features.feature_engineering import add_features


def test_add_features_columns_exist():
    df = pd.DataFrame({
        "timestamp": ["2025-01-01", "2025-01-02"],
        "product_id": ["P1", "P1"],
        "current_price": [100.0, 110.0],
        "competitor_price": [105.0, 105.0],
        "cost_price": [60.0, 60.0],
        "inventory_level": [50, 40],
        "views_last_hour": [20, 30],
        "add_to_cart_count": [4, 6],
        "demand": [10, 12],
    })

    result = add_features(df)

    expected_columns = [
        "price_ratio_to_competitor",
        "price_difference",
        "profit_margin",
        "inventory_ratio",
        "cart_to_view_ratio",
        "avg_demand_3",
        "avg_demand_7",
        "demand_lag_1",
    ]

    for col in expected_columns:
        assert col in result.columns

    assert result["price_difference"].iloc[0] == 100.0 - 105.0
