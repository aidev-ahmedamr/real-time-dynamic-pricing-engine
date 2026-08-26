import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Dynamic Pricing Engine",
    layout="wide"
)

st.title(
    "⚡ Real-Time Dynamic Pricing Engine"
)


uploaded_file = st.file_uploader(
    "Upload Pricing Decisions CSV",
    type=["csv"]
)


if uploaded_file:

    df = pd.read_csv(uploaded_file)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Decisions",
        len(df)
    )

    col2.metric(
        "Average Recommended Price",
        f"${df['recommended_price'].mean():.2f}"
    )

    col3.metric(
        "Average Predicted Demand",
        f"{df['predicted_demand'].mean():.2f}"
    )

    col4.metric(
        "Total Expected Profit",
        f"${df['expected_profit'].sum():,.2f}"
    )


    st.subheader("Price Decisions")

    st.dataframe(df)


    st.subheader(
        "Current vs Recommended Price"
    )

    chart_df = df[
        [
            "current_price",
            "recommended_price"
        ]
    ]

    st.line_chart(chart_df)
