import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# Fix path — works from any directory
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database", "retail.db")

st.set_page_config(
    page_title="Retail Price Intelligence",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Real-Time Retail Price Intelligence Engine")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

@st.cache_data(ttl=300)
def load_data():
    conn = duckdb.connect(DB_PATH, read_only=True)
    prices = conn.execute("SELECT * FROM raw_prices ORDER BY price_gbp DESC").fetchdf()
    by_rating = conn.execute("""
        SELECT
            rating,
            ROUND(AVG(price_gbp), 2) as avg_price,
            COUNT(*)                  as book_count,
            ROUND(MIN(price_gbp), 2) as min_price,
            ROUND(MAX(price_gbp), 2) as max_price
        FROM raw_prices
        GROUP BY rating
        ORDER BY avg_price DESC
    """).fetchdf()
    conn.close()
    return prices, by_rating

try:
    prices, by_rating = load_data()

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Books Tracked", len(prices))
    col2.metric("Avg Price", f"£{prices['price_gbp'].mean():.2f}")
    col3.metric("Cheapest", f"£{prices['price_gbp'].min():.2f}")
    col4.metric("Most Expensive", f"£{prices['price_gbp'].max():.2f}")

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Price Distribution")
        fig = px.histogram(
            prices, x="price_gbp", nbins=20,
            color_discrete_sequence=["#0C447C"],
            labels={"price_gbp": "Price (£)", "count": "Books"}
        )
        fig.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Average Price by Rating")
        fig2 = px.bar(
            by_rating, x="rating", y="avg_price",
            color="avg_price",
            color_continuous_scale="Blues",
            labels={"rating": "Rating", "avg_price": "Avg Price (£)"}
        )
        fig2.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    st.subheader("🚨 Price Alert Feed")
    st.info("Alerts appear here when prices change more than 5% between daily scrape runs.")

    st.divider()

    st.subheader("📋 Full Price Table")
    col_f1, col_f2 = st.columns(2)

    with col_f1:
        rating_filter = st.multiselect(
            "Filter by rating",
            options=sorted(prices["rating"].unique()),
            default=sorted(prices["rating"].unique())
        )
    with col_f2:
        max_price = st.slider(
            "Max price (£)",
            min_value=float(prices["price_gbp"].min()),
            max_value=float(prices["price_gbp"].max()),
            value=float(prices["price_gbp"].max())
        )

    filtered = prices[
        (prices["rating"].isin(rating_filter)) &
        (prices["price_gbp"] <= max_price)
    ]

    st.dataframe(
        filtered[["title", "price_gbp", "rating", "availability", "scraped_at"]],
        use_container_width=True,
        height=400
    )
    st.caption(f"Showing {len(filtered)} of {len(prices)} books")

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.write(f"Looking for database at: {DB_PATH}")
    st.write(f"File exists: {os.path.exists(DB_PATH)}")