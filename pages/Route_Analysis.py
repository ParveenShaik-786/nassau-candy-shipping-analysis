import streamlit as st
from utils.preprocess import load_data
from utils.sidebar import render_filters

st.set_page_config(page_title="Route Analysis", page_icon="🔍", layout="wide")
st.title("🔍 Route Drill-Down")

df = load_data()
filtered = render_filters(df, key_prefix="routeanalysis")

if len(filtered) == 0:
    st.warning("No shipments match the current filters.")
    st.stop()

routes = sorted(filtered["Route State"].unique())
selected_route = st.selectbox("Select a Route (Factory → State)", options=routes)

route_df = filtered[filtered["Route State"] == selected_route]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Shipments", f"{len(route_df):,}")
col2.metric("Avg Lead Time", f"{route_df['Lead Time (Days)'].mean():.2f} days")
col3.metric("Delay Frequency", f"{route_df['Delayed'].mean() * 100:.1f}%")
col4.metric("Total Sales", f"${route_df['Sales'].sum():,.0f}")

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Lead Time by Ship Mode on this Route")
    st.dataframe(
        route_df.groupby("Ship Mode")["Lead Time (Days)"].agg(["count", "mean"]).rename(
            columns={"count": "Shipments", "mean": "Avg Lead Time"}
        ),
        use_container_width=True,
    )
with col2:
    st.subheader("Top Products Shipped on this Route")
    st.dataframe(
        route_df.groupby("Product Name")["Order ID"].count()
        .sort_values(ascending=False)
        .head(10)
        .rename("Shipments"),
        use_container_width=True,
    )

st.divider()
st.subheader("Order-Level Detail")
st.dataframe(
    route_df[[
        "Order ID", "Order Date", "Corrected Ship Date", "Ship Mode",
        "City", "State/Province", "Sales", "Gross Profit", "Lead Time (Days)", "Delayed",
    ]].sort_values("Order Date", ascending=False),
    hide_index=True,
    use_container_width=True,
)
