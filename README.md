# ⚡ Real-Time Dynamic Pricing Engine

An end-to-end AI-powered dynamic pricing engine that predicts product demand,
optimizes prices for maximum profit, simulates live market events, and
explains every pricing decision in plain language.

![Demo Run](docs/images/demo-run.png)

## Overview

The project simulates an e-commerce catalog, trains a demand-prediction
model on price, competitor, and behavioral signals, then searches for the
price that maximizes expected profit for each product while staying inside
business guardrails (minimum margin, maximum price swing, competitor
positioning). Every decision comes with a plain-language explanation of
why that price was recommended.

## Business Problem

Manually-set prices can't react to changing demand, inventory, or
competitor pricing in real time, which leaves margin and revenue on the
table. This project shows how a demand model plus a constrained
optimization step can recommend a better price automatically, with an
explanation attached, and persist that decision history for analysis.

## Solution / Pipeline

1. **Generate synthetic market data** — `src/data/generate_data.py`
2. **Engineer features** from raw events — `src/features/feature_engineering.py`
3. **Train an XGBoost demand model**, tracked with MLflow — `src/models/train.py`
4. **Search candidate prices** and pick the profit-maximizing one, subject
   to guardrails — `src/optimization/price_optimizer.py`
5. **Explain the recommendation** in plain language —
   `src/optimization/explainability.py`
6. **Serve recommendations** through a FastAPI endpoint — `api/main.py`
7. **Cache live product state** in Redis and **persist every decision**
   to PostgreSQL — `src/cache/redis_client.py`, `database/db.py`
8. **Simulate a real-time stream** of market events hitting the API —
   `src/streaming/run_simulation.py`
9. **Visualize decisions** on a live dashboard reading from PostgreSQL —
   `dashboard/app.py`

## Key Features

- Demand prediction (XGBoost)
- Dynamic price optimization with business guardrails (min margin, max
  price swing, competitor positioning)
- Revenue and profit optimization (not just revenue maximization)
- Explainable AI — plain-language reasons behind every decision
- Real-time market event simulation (views, add-to-cart, purchases,
  competitor price moves) streamed against a live API
- REST API (FastAPI)
- Redis caching of live product state
- PostgreSQL persistence of full decision history
- Streamlit dashboard reading live from the database
- MLflow experiment tracking (params, metrics, model artifact)
- Data drift detection (`src/monitoring/drift_detection.py`)
- Model quality monitoring — MAE/RMSE (`src/monitoring/model_monitoring.py`)
- Automated tests (pytest) + GitHub Actions CI
- Docker / docker-compose setup

## Results

Trained on 72,900 synthetic hourly product-market snapshots:

| Metric | Value |
|---|---|
| MAE | 0.24 |
| RMSE | 0.59 |
| R² | 0.993 |

## Project Structure


## Dataset

Synthetic hourly e-commerce data across 5 categories (Electronics, Fashion,
Home & Kitchen, Sports, Beauty), generated with configurable seasonality,
time-of-day traffic patterns, and price elasticity per category.

## Machine Learning

An `XGBRegressor` is trained to predict demand from price, competitor
price, inventory, traffic, and rolling demand-history features, using a
time-ordered 80/20 train/test split (no shuffling, to avoid leaking future
demand into training). Every training run is logged to MLflow (params,
metrics, and the model artifact).

## Pricing Algorithm

For each product, 21 candidate prices are evaluated between the guardrail
floor and ceiling. The candidate with the highest **predicted profit**
(not just revenue) is selected, then clipped again by `apply_guardrails()`
for margin, maximum price change, and competitor positioning before being
returned.

## API

`POST /optimize-price` — takes a product's current state (price, cost,
competitor price, inventory, traffic signals, engineered features) and
returns the recommended price, predicted demand, expected profit, and the
reasons behind the recommendation. The decision is automatically cached in
Redis and persisted to PostgreSQL. See `api/schemas.py` for the full
request/response shape.

`GET /product-state/{product_id}` — returns the last cached state for a
product from Redis.

`GET /health` — health check.

## Real-Time Simulation

`src/streaming/run_simulation.py` runs a live loop: it generates a market
event for a random product (view, add-to-cart, purchase, or a competitor
price change), updates that product's state, and sends it to the running
API, which prices it and stores the decision. This is what makes the
system genuinely "real-time" rather than a one-off batch script.

## Dashboard

A Streamlit app that reads pricing decisions live from PostgreSQL —
showing total decisions, average recommended price, average predicted
demand, total expected profit, a current-vs-recommended price chart, and
a breakdown of actions taken (increase / decrease / keep price).

## Testing

`pytest` covers the guardrail and profit-calculation logic
(`src/optimization/price_optimizer.py`), the explainability rules
(`src/optimization/explainability.py`), and the feature engineering
pipeline (`src/features/feature_engineering.py`). Run with:

```bash
pytest
```

## Monitoring

- `src/monitoring/drift_detection.py` — Kolmogorov-Smirnov test comparing
  reference vs. current feature distributions
- `src/monitoring/model_monitoring.py` — MAE / RMSE tracking over time

## How to Run (Google Colab)

This project was built and tested end-to-end in Google Colab. To
reproduce the full pipeline — data generation, feature engineering, model
training, the API, the real-time simulation, and the database — in a
single Colab notebook:

```python
!git clone https://github.com/aidev-ahmedamr/real-time-dynamic-pricing-engine.git
%cd real-time-dynamic-pricing-engine
!pip install -q -r requirements.txt

!apt-get -qq install postgresql redis-server > /dev/null
!service postgresql start
!service redis-server start
!sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
!sudo -u postgres psql -c "CREATE DATABASE pricing_db;"
!sudo -u postgres psql -d pricing_db -f database/init.sql

import os
os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/pricing_db"

!mkdir -p data/raw data/processed models
!python -m src.data.generate_data
!python -m src.features.feature_engineering
!python -m src.models.train

get_ipython().system_raw("uvicorn api.main:app --host 0.0.0.0 --port 8000 &")
import time; time.sleep(5)

import requests
print("Health check:", requests.get("http://localhost:8000/health").json())

get_ipython().system_raw("timeout 20 python -m src.streaming.run_simulation > sim_output.txt 2>&1 &")
time.sleep(25)

from database.db import get_recent_decisions
for d in get_recent_decisions(limit=5):
    print(d)

!python -m pytest -q
```

## How to Run (Docker)

```bash
docker-compose up --build
```

This starts the FastAPI service, PostgreSQL (schema in
`database/init.sql`), and Redis.

## Future Improvements

- Replace synthetic data with a real e-commerce dataset
- Add authentication to the API
- Add a proper CI step that trains and validates the model on every PR
- Add alerting on top of the drift detection module
