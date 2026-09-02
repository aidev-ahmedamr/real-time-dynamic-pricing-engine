from src.optimization.explainability import explain_pricing_decision


def test_increase_price_action():
    result = explain_pricing_decision(
        current_price=100,
        recommended_price=110,
        competitor_price=120,
        inventory_level=15,
        predicted_demand=25,
    )
    assert result["action"] == "INCREASE_PRICE"
    assert "High predicted demand" in result["reasons"]
    assert "Low inventory level" in result["reasons"]


def test_decrease_price_action():
    result = explain_pricing_decision(
        current_price=100,
        recommended_price=90,
        competitor_price=80,
        inventory_level=250,
        predicted_demand=2,
    )
    assert result["action"] == "DECREASE_PRICE"
    assert "Low predicted demand" in result["reasons"]
    assert "High inventory level" in result["reasons"]


def test_keep_price_action():
    result = explain_pricing_decision(
        current_price=100,
        recommended_price=100.05,
        competitor_price=100,
        inventory_level=100,
        predicted_demand=10,
    )
    assert result["action"] == "KEEP_PRICE"
