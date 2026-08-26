from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)


def calculate_model_metrics(
    actual,
    predicted
):

    mae = mean_absolute_error(
        actual,
        predicted
    )

    rmse = mean_squared_error(
        actual,
        predicted
    ) ** 0.5

    return {
        "mae": float(mae),
        "rmse": float(rmse)
    }
