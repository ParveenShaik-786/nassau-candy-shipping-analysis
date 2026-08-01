import streamlit as st
from utils.preprocess import load_data
from utils.sidebar import render_filters
from utils.charts import order_timeline

st.set_page_config(page_title="Shipment Timeline Drilldown", page_icon="🕐", layout="wide")
st.title("🕐 Order-Level Shipment Timelines")

df = load_data()
filtered = render_filters(df, key_prefix="drilldown")

if len(filtered) == 0:
    st.warning("No shipments match the current filters.")
    st.stop()

n = st.slider("Number of recent orders to show", min_value=10, max_value=200, value=50, step=10)

st.plotly_chart(order_timeline(filtered, n=n), use_container_width=True)

st.divider()
st.subheader("Search by Order ID")
order_ids = sorted(filtered["Order ID"].unique())
selected_order = st.selectbox("Order ID", options=["All"] + list(order_ids))

if selected_order != "All":
    order_rows = filtered[filtered["Order ID"] == selected_order]
    st.dataframe(
        order_rows[[
            "Order ID", "Product Name", "Order Date", "Corrected Ship Date",
            "Ship Mode", "Lead Time (Days)", "Delayed", "Route State",
        ]],
        hide_index=True,
        use_container_width=True,
    )
else:
    st.dataframe(
        filtered[[
            "Order ID", "Order Date", "Corrected Ship Date", "Ship Mode",
            "Route State", "Lead Time (Days)", "Delayed",
        ]].sort_values("Order Date", ascending=False).head(200),
        hide_index=True,
        use_container_width=True,
    )
