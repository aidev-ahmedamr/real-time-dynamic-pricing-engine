import numpy as np
import pandas as pd


def apply_guardrails(
    recommended_price,
    current_price,
    cost_price,
    competitor_price,
    min_margin=0.10,
    max_price_change=0.20,
    max_market_multiplier=1.25
):
    """
    Applies business constraints to the AI-recommended price.
    """

    min_price = cost_price * (1 + min_margin)

    min_allowed_price = current_price * (
        1 - max_price_change
    )

    max_allowed_price = current_price * (
        1 + max_price_change
    )

    max_market_price = (
        competitor_price * max_market_multiplier
    )

    final_price = max(
        recommended_price,
        min_price,
        min_allowed_price
    )

    final_price = min(
        final_price,
        max_allowed_price,
        max_market_price
    )

    return round(float(final_price), 2)


def calculate_profit(price, cost_price, demand):
    return round(
        (price - cost_price) * demand,
        2
    )


def optimize_price(
    product_data,
    model,
    features,
    min_margin=0.10,
    max_price_increase=0.20,
    max_price_decrease=0.20,
    num_candidates=21
):

    current_price = product_data["current_price"]
    cost_price = product_data["cost_price"]
    competitor_price = product_data["competitor_price"]

    min_price = max(
        cost_price * (1 + min_margin),
        current_price * (1 - max_price_decrease)
    )

    max_price = current_price * (
        1 + max_price_increase
    )

    candidate_prices = np.linspace(
        min_price,
        max_price,
        num_candidates
    )

    results = []

    for candidate_price in candidate_prices:

        temp = product_data.copy()

        temp["current_price"] = candidate_price

        temp["price_ratio_to_competitor"] = (
            candidate_price / temp["competitor_price"]
        )

        temp["price_difference"] = (
            candidate_price - temp["competitor_price"]
        )

        temp["profit_margin"] = (
            (candidate_price - temp["cost_price"])
            / candidate_price
        )

        input_df = pd.DataFrame([temp])

        input_df = input_df[features]

        predicted_demand = max(
            0,
            float(model.predict(input_df)[0])
        )

        expected_revenue = (
            candidate_price * predicted_demand
        )

        expected_profit = calculate_profit(
            candidate_price,
            cost_price,
            predicted_demand
        )

        results.append({
            "candidate_price": round(
                float(candidate_price), 2
            ),
            "predicted_demand": round(
                predicted_demand, 2
            ),
            "expected_revenue": round(
                expected_revenue, 2
            ),
            "expected_profit": round(
                expected_profit, 2
            )
        })

    results_df = pd.DataFrame(results)

    best_result = results_df.loc[
        results_df["expected_profit"].idxmax()
    ].to_dict()

    guarded_price = apply_guardrails(
        recommended_price=best_result["candidate_price"],
        current_price=current_price,
        cost_price=cost_price,
        competitor_price=competitor_price,
        min_margin=min_margin,
        max_price_change=max_price_increase
    )

    best_result["recommended_price"] = guarded_price

    return best_result, results_df
