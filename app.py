import streamlit as st
import pandas as pd
from reorder import load_sales_data, calculate_avg_daily_sales, calculate_reorder_points

st.set_page_config(page_title="Stock Reorder Assistant", layout="wide")

st.title("📦 Stock Reorder Assistant")
st.caption("Inventory reorder recommendations based on real retail transaction history.")


@st.cache_data
def get_results():
    sales = load_sales_data()
    products = pd.read_csv('products.csv')
    avg_daily_sales = calculate_avg_daily_sales(sales)
    return calculate_reorder_points(products, avg_daily_sales)


result = get_results()

reorder_count = result['needs_reorder'].sum()
st.metric("Products needing reorder", f"{reorder_count} / {len(result)}")

st.divider()

for _, row in result.iterrows():
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"{row['product_name']} ({row['product_id']})")
            st.write(f"Current stock: **{row['current_stock']}**")
            st.write(f"Reorder point: **{row['reorder_point']:.0f}**")
            st.write(f"Average daily sales: {row['avg_daily_sales']:.1f}")
        with col2:
            if row['needs_reorder']:
                st.error("⚠️ REORDER NEEDED")
            else:
                st.success("✅ OK")