from pydantic import BaseModel
from typing import List


class ProductPricingRequest(BaseModel):

    product_id: str

    base_price: float
    cost_price: float
    current_price: float
    competitor_price: float

    inventory_level: int

    views_last_hour: int
    add_to_cart_count: int

    hour: int
    day_of_week: int
    month: int
    is_weekend: int

    rating: float
    num_reviews: int

    conversion_rate: float

    price_ratio_to_competitor: float
    price_difference: float
    profit_margin: float
    inventory_ratio: float
    cart_to_view_ratio: float
    avg_demand_3: float
    avg_demand_7: float
    demand_lag_1: float


class PricingResponse(BaseModel):

    product_id: str

    current_price: float
    recommended_price: float

    predicted_demand: float
    expected_revenue: float
    expected_profit: float

    action: str

    price_change_percentage: float

    reasons: List[str]
