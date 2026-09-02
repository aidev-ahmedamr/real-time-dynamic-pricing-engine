import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd

from database.db import get_recent_decisions


st.set_page_config(
    page_title="Dynamic Pricing Engine",
    layout="wide"
)

st.title("⚡ Real-Time Dynamic Pricing Engine")

if st.button("🔄 Refresh"):
    st.rerun()

try:
    rows = get_recent_decisions(limit=200)
except Exception as e:
    st.error(
        "Could not connect to the database. Make sure PostgreSQL is "
        "running (docker-compose up) and DATABASE_URL is set correctly."
    )
    st.stop()

if not rows:
    st.info("No pricing decisions yet. Call the /optimize-price API or run the simulation to generate some.")
    st.stop()

df = pd.DataFrame(rows)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Decisions", len(df))
col2.metric("Average Recommended Price", f"${df['recommended_price'].mean():.2f}")
col3.metric("Average Predicted Demand", f"{df['predicted_demand'].mean():.2f}")
col4.metric("Total Expected Profit", f"${df['expected_profit'].sum():,.2f}")

st.subheader("Recent Price Decisions")
st.dataframe(df, use_container_width=True)

st.subheader("Current vs Recommended Price")
chart_df = df[["current_price", "recommended_price"]]
st.line_chart(chart_df)

st.subheader("Actions Breakdown")
st.bar_chart(df["action"].value_counts())
