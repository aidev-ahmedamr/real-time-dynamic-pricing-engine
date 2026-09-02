import os
from sqlalchemy import create_engine, text


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/pricing_db"
)


engine = create_engine(DATABASE_URL)


SAVE_DECISION_SQL = text("""
    INSERT INTO pricing_decisions (
        product_id,
        current_price,
        recommended_price,
        predicted_demand,
        expected_revenue,
        expected_profit,
        action,
        price_change_percentage,
        reasons,
        model_version
    ) VALUES (
        :product_id,
        :current_price,
        :recommended_price,
        :predicted_demand,
        :expected_revenue,
        :expected_profit,
        :action,
        :price_change_percentage,
        :reasons,
        :model_version
    )
""")


def save_decision_to_db(decision, model_version="1.0.0"):
    """Persist one pricing decision to the pricing_decisions table."""

    with engine.begin() as conn:
        conn.execute(
            SAVE_DECISION_SQL,
            {
                "product_id": decision["product_id"],
                "current_price": decision["current_price"],
                "recommended_price": decision["recommended_price"],
                "predicted_demand": decision["predicted_demand"],
                "expected_revenue": decision["expected_revenue"],
                "expected_profit": decision["expected_profit"],
                "action": decision["action"],
                "price_change_percentage": decision["price_change_percentage"],
                "reasons": " | ".join(decision["reasons"]),
                "model_version": model_version,
            },
        )


def get_recent_decisions(limit=200):
    """Fetch the most recent pricing decisions (used by the dashboard)."""

    query = text("""
        SELECT *
        FROM pricing_decisions
        ORDER BY timestamp DESC
        LIMIT :limit
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {"limit": limit})
        rows = [dict(row._mapping) for row in result]

    return rows
