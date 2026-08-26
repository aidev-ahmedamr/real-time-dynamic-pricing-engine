CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,
    category VARCHAR(100),
    base_price FLOAT,
    cost_price FLOAT
);


CREATE TABLE pricing_decisions (

    decision_id SERIAL PRIMARY KEY,

    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    product_id VARCHAR(50),

    current_price FLOAT,

    recommended_price FLOAT,

    predicted_demand FLOAT,

    expected_revenue FLOAT,

    expected_profit FLOAT,

    action VARCHAR(50),

    price_change_percentage FLOAT,

    reasons TEXT,

    model_version VARCHAR(50)
);


CREATE TABLE market_events (

    event_id VARCHAR(50) PRIMARY KEY,

    timestamp TIMESTAMP,

    product_id VARCHAR(50),

    event_type VARCHAR(100),

    event_data JSONB
);
