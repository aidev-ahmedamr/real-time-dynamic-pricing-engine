def explain_pricing_decision(
    current_price,
    recommended_price,
    competitor_price,
    inventory_level,
    predicted_demand
):

    reasons = []

    price_change = (
        recommended_price - current_price
    ) / current_price

    if predicted_demand > 20:
        reasons.append(
            "High predicted demand"
        )

    elif predicted_demand < 5:
        reasons.append(
            "Low predicted demand"
        )

    if inventory_level < 30:
        reasons.append(
            "Low inventory level"
        )

    elif inventory_level > 200:
        reasons.append(
            "High inventory level"
        )

    if competitor_price > current_price:
        reasons.append(
            "Competitor price is higher"
        )

    elif competitor_price < current_price:
        reasons.append(
            "Competitor price is lower"
        )

    if price_change > 0.01:
        action = "INCREASE_PRICE"

    elif price_change < -0.01:
        action = "DECREASE_PRICE"

    else:
        action = "KEEP_PRICE"

    return {
        "action": action,
        "price_change_percentage": round(
            price_change * 100,
            2
        ),
        "reasons": reasons
    }
