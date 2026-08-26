from src.optimization.price_optimizer import optimize_price
from src.optimization.explainability import explain_pricing_decision


def generate_pricing_decision(
    product_data,
    model,
    features
):

    best_result, results_df = optimize_price(
        product_data=product_data,
        model=model,
        features=features
    )

    explanation = explain_pricing_decision(
        current_price=product_data["current_price"],
        recommended_price=best_result[
            "recommended_price"
        ],
        competitor_price=product_data[
            "competitor_price"
        ],
        inventory_level=product_data[
            "inventory_level"
        ],
        predicted_demand=best_result[
            "predicted_demand"
        ]
    )

    decision = {
        "product_id": product_data["product_id"],
        "current_price": product_data[
            "current_price"
        ],
        "recommended_price": best_result[
            "recommended_price"
        ],
        "predicted_demand": best_result[
            "predicted_demand"
        ],
        "expected_revenue": best_result[
            "expected_revenue"
        ],
        "expected_profit": best_result[
            "expected_profit"
        ],
        "action": explanation["action"],
        "price_change_percentage": explanation[
            "price_change_percentage"
        ],
        "reasons": explanation["reasons"]
    }

    return decision, results_df
