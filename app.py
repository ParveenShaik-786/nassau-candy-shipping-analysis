import streamlit as st
from utils.preprocess import load_data
from utils.sidebar import render_filters
from utils.metrics import compute_summary_kpis
from utils.charts import lead_time_histogram

st.set_page_config(
    page_title="Nassau Candy | Shipping Route Efficiency",
    page_icon="🍬",
    layout="wide",
)

st.title("🍬 Factory-to-Customer Shipping Route Efficiency")
st.caption("Nassau Candy Distributor — Unified Mentor Capstone")

df = load_data()
filtered = render_filters(df, key_prefix="home")

kpis = compute_summary_kpis(filtered)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Shipments", f"{kpis['total_shipments']:,}")
col2.metric("Avg Lead Time", f"{kpis['avg_lead_time']} days")
col3.metric("Delay Frequency", f"{kpis['delay_frequency_pct']}%")
col4.metric("Total Sales", f"${kpis['total_sales']:,.0f}")
col5.metric("Total Gross Profit", f"${kpis['total_profit']:,.0f}")

st.divider()

st.subheader("Lead Time Distribution")
st.plotly_chart(lead_time_histogram(filtered), use_container_width=True)

st.divider()
st.markdown(
    "### About this dashboard\n"
    "Use the pages in the sidebar to explore:\n"
    "- **Dashboard** — Route Efficiency Overview and leaderboard\n"
    "- **Geographic** — US shipping performance heatmap\n"
    "- **Ship Mode** — Lead time and delay comparison by shipping method\n"
    "- **Route Analysis** — State-level route performance drill-down\n"
    "- **Drilldown** — Order-level shipment timelines\n\n"
    "**Data note:** the raw `Ship Date` field in the source data was found to be "
    "corrupted during cleaning. `Lead Time (Days)` here is a corrected value "
    "simulated from `Ship Mode` — see the project notebooks for the full "
    "methodology and limitations."
)
