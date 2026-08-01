import streamlit as st
from utils.preprocess import load_data
from utils.sidebar import render_filters
from utils.metrics import route_leaderboard
from utils.charts import route_leaderboard_bar

st.set_page_config(page_title="Route Efficiency Overview", page_icon="📊", layout="wide")
st.title("📊 Route Efficiency Overview")

df = load_data()
filtered = render_filters(df, key_prefix="dashboard")

MIN_SHIPMENTS = st.sidebar.number_input(
    "Minimum shipments per route", min_value=1, max_value=100, value=10,
    help="Routes with fewer shipments than this are excluded so single orders don't skew the ranking.",
)

leaderboard = route_leaderboard(filtered, min_shipments=MIN_SHIPMENTS)

if len(leaderboard) == 0:
    st.warning("No routes meet the minimum shipment threshold for the current filters. Try loosening the filters.")
else:
    st.subheader("Route Performance Leaderboard")
    st.plotly_chart(route_leaderboard_bar(leaderboard, top_n=min(15, len(leaderboard))), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Top 10 Most Efficient Routes")
        st.dataframe(
            leaderboard.head(10)[
                ["Route State", "Total_Shipments", "Avg_Lead_Time", "Delay_Frequency_Pct", "Route_Efficiency_Score"]
            ],
            hide_index=True,
            use_container_width=True,
        )
    with col2:
        st.markdown("#### Bottom 10 Least Efficient Routes")
        st.dataframe(
            leaderboard.tail(10)[
                ["Route State", "Total_Shipments", "Avg_Lead_Time", "Delay_Frequency_Pct", "Route_Efficiency_Score"]
            ].sort_values("Route_Efficiency_Score"),
            hide_index=True,
            use_container_width=True,
        )

    st.divider()
    st.markdown("#### Full Route Leaderboard")
    st.dataframe(leaderboard, hide_index=True, use_container_width=True)

st.info(
    "⚠️ **Interpretation note:** Lead Time (Days) is simulated from Ship Mode, "
    "so route rankings largely reflect which ship modes are used on each route "
    "rather than independently observed courier performance. See notebook 02 "
    "for the full methodology note."
)
