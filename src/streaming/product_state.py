def update_product_state(
    product_state,
    event
):

    state = product_state.copy()

    event_type = event["event_type"]

    if event_type == "PRODUCT_VIEW":

        state["views_last_hour"] += 1

    elif event_type == "ADD_TO_CART":

        state["add_to_cart_count"] += 1

    elif event_type == "PURCHASE":

        state["inventory_level"] = max(
            0,
            state["inventory_level"] - 1
        )

    elif event_type == "COMPETITOR_PRICE_CHANGE":

        change = event[
            "price_change_percentage"
        ]

        state["competitor_price"] *= (
            1 + change
        )

    elif event_type == "INVENTORY_UPDATE":

        state["inventory_level"] = max(
            0,
            state["inventory_level"]
            + event["inventory_change"]
        )

    return state
