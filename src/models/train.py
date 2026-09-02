
"""
Train the demand-prediction model, with MLflow experiment tracking.

Usage:
    python -m src.models.train
"""

import joblib
import mlflow
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor


FEATURES = [
    "base_price",
    "cost_price",
    "current_price",
    "competitor_price",
    "inventory_level",
    "views_last_hour",
    "add_to_cart_count",
    "hour",
    "day_of_week",
    "month",
    "is_weekend",
    "rating",
    "num_reviews",
    "conversion_rate",
    "price_ratio_to_competitor",
    "price_difference",
    "profit_margin",
    "inventory_ratio",
    "cart_to_view_ratio",
    "avg_demand_3",
    "avg_demand_7",
    "demand_lag_1",
]

TARGET = "demand"

MODEL_PARAMS = {
    "n_estimators": 300,
    "learning_rate": 0.05,
    "max_depth": 8,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "random_state": 42,
}


def train_model(df, features=FEATURES, target=TARGET, params=MODEL_PARAMS):
    """Time-ordered 80/20 split + XGBoost regressor."""

    df = df.sort_values("timestamp")

    split_index = int(len(df) * 0.8)
    train_df = df.iloc[:split_index]
    test_df = df.iloc[split_index:]

    X_train, y_train = train_df[features], train_df[target]
    X_test, y_test = test_df[features], test_df[target]

    model = XGBRegressor(**params)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    metrics = {
        "mae": mean_absolute_error(y_test, predictions),
        "rmse": mean_squared_error(y_test, predictions) ** 0.5,
        "r2": r2_score(y_test, predictions),
    }

    return model, metrics


def save_model(model, features, model_path="models/demand_model.pkl",
                features_path="models/model_features.pkl"):
    joblib.dump(model, model_path)
    joblib.dump(features, features_path)


if __name__ == "__main__":
    data = pd.read_csv("data/processed/dynamic_pricing_processed.csv")

    mlflow.set_experiment("dynamic-pricing-demand-model")

    with mlflow.start_run():
        trained_model, metrics = train_model(data)

        mlflow.log_params(MODEL_PARAMS)
        mlflow.log_metrics(metrics)
        mlflow.xgboost.log_model(trained_model, "model")

        print("MAE:", metrics["mae"])
        print("RMSE:", metrics["rmse"])
        print("R2:", metrics["r2"])

    save_model(trained_model, FEATURES)
    print("Saved model to models/demand_model.pkl")
    print("Saved feature list to models/model_features.pkl")
