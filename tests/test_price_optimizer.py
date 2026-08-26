from src.optimization.price_optimizer import (
    apply_guardrails,
    calculate_profit
)


def test_price_above_minimum_margin():

    price = apply_guardrails(
        recommended_price=50,
        current_price=100,
        cost_price=90,
        competitor_price=100,
        min_margin=0.10
    )

    assert price >= 99


def test_max_price_increase():

    price = apply_guardrails(
        recommended_price=200,
        current_price=100,
        cost_price=50,
        competitor_price=200,
        max_price_change=0.20
    )

    assert price <= 120


def test_profit_calculation():

    profit = calculate_profit(
        price=100,
        cost_price=60,
        demand=50
    )

    assert profit == 2000
