# System Architecture

```text
                    MARKET EVENTS
                         │
                         ▼
                  EVENT SIMULATOR
                         │
                         ▼
                 PRODUCT STATE UPDATE
                         │
                         ▼
                     REDIS CACHE
                         │
                         ▼
                 FEATURE ENGINEERING
                         │
                         ▼
                  DEMAND ML MODEL
                         │
                         ▼
               PRICE OPTIMIZATION ENGINE
                         │
                         ▼
                 BUSINESS GUARDRAILS
                         │
                         ▼
                EXPLAINABLE AI DECISION
                         │
                         ▼
                    FASTAPI API
                         │
                ┌────────┴────────┐
                ▼                 ▼
           POSTGRESQL         STREAMLIT
          DECISION HISTORY    DASHBOARD

