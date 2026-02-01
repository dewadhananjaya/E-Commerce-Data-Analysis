import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set page title
st.set_page_config(page_title="E-Commerce Data Dashboard", layout="wide")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    return df

all_df = load_data()

# Sidebar for Date Filter
min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png") 
    start_date, end_date = st.date_input(
        label='Date Range',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                 (all_df["order_purchase_timestamp"] <= str(end_date))]

# Header
st.header('E-Commerce Performance Dashboard :sparkles:')

# --- Bagian 1: Revenue by Category ---
st.subheader("Top 10 Product Categories by Revenue")

col1, col2 = st.columns([2, 1])

with col1:
    category_revenue = main_df.groupby("product_category_name_english").price.sum().sort_values(ascending=False).reset_index().head(10)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(
        x="price", 
        y="product_category_name_english", 
        data=category_revenue, 
        palette="viridis",
        ax=ax
    )
    ax.set_title("Total Revenue per Category (BRL)", fontsize=15)
    ax.set_xlabel("Revenue")
    ax.set_ylabel("Category")
    st.pyplot(fig)

with col2:
    st.write("The category with the highest revenue indicates dominant market interest. Focusing stock on this category is highly recommended.")
    st.dataframe(category_revenue)

st.markdown("---")

# --- Bagian 2: Satisfaction & Delivery Duration ---
st.subheader("Customer Satisfaction vs Delivery Speed")

col3, col4 = st.columns([2, 1])

with col3:
    # Filter data with valid delivery duration
    delivery_analysis = main_df.dropna(subset=['delivery_duration', 'review_score'])
    review_stats = delivery_analysis.groupby("review_score").delivery_duration.mean().reset_index()

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.barplot(
        x="review_score", 
        y="delivery_duration", 
        data=review_stats, 
        palette="coolwarm",
        ax=ax2
    )
    ax2.set_title("Average Delivery Duration per Review Score", fontsize=15)
    ax2.set_xlabel("Review Score (1-5)")
    ax2.set_ylabel("Avg. Days to Deliver")
    st.pyplot(fig2)

with col4:
    st.markdown("""
    **Satisfaction Polarization Pattern:**
    - Score **1 (Disappointed)** is associated with significantly longer average delivery times.
    - Score **5 (Highly Satisfied)** features the shortest delivery durations.
    - This demonstrates that delivery speed is a critical factor in driving customer satisfaction.
    """)