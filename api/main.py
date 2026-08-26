from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd

from api.schemas import (
    ProductPricingRequest,
    PricingResponse
)

from src.optimization.pricing_pipeline import (
    generate_pricing_decision
)


app = FastAPI(
    title="Real-Time Dynamic Pricing Engine",
    version="1.0.0"
)


model = joblib.load(
    "models/demand_model.pkl"
)

features = joblib.load(
    "models/model_features.pkl"
)


@app.get("/")
def root():
    return {
        "message": "Dynamic Pricing Engine is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post(
    "/optimize-price",
    response_model=PricingResponse
)
def optimize_price_endpoint(
    product_data: ProductPricingRequest
):

    try:
        decision, _ = generate_pricing_decision(
            product_data.model_dump(),
            model,
            features
        )

        return decision

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
