from fastapi import FastAPI, HTTPException
import joblib

from api.schemas import (
    ProductPricingRequest,
    PricingResponse
)

from src.optimization.pricing_pipeline import (
    generate_pricing_decision
)

from src.cache.redis_client import (
    save_product_state,
    get_product_state
)

from database.db import save_decision_to_db


app = FastAPI(
    title="Real-Time Dynamic Pricing Engine",
    version="1.0.0"
)


model = joblib.load("models/demand_model.pkl")
features = joblib.load("models/model_features.pkl")


@app.get("/")
def root():
    return {"message": "Dynamic Pricing Engine is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/product-state/{product_id}")
def product_state(product_id: str):
    """Return the last cached state we have for this product, if any."""

    state = get_product_state(product_id)

    if state is None:
        raise HTTPException(
            status_code=404,
            detail=f"No cached state for product {product_id}"
        )

    return state


@app.post("/optimize-price", response_model=PricingResponse)
def optimize_price_endpoint(product_data: ProductPricingRequest):

    try:
        payload = product_data.model_dump()

        decision, _ = generate_pricing_decision(payload, model, features)

        try:
            save_product_state(payload["product_id"], payload)
        except Exception:
            pass  # Redis being down shouldn't break pricing

        try:
            save_decision_to_db(decision)
        except Exception:
            pass  # DB being down shouldn't break pricing

        return decision

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
