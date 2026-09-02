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
