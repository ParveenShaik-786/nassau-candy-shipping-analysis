import streamlit as st
from utils.preprocess import load_data
from utils.sidebar import render_filters
from utils.metrics import geographic_summary
from utils.charts import us_choropleth

st.set_page_config(page_title="Geographic Shipping Map", page_icon="🗺️", layout="wide")
st.title("🗺️ Geographic Shipping Map")
st.caption("US state-level shipping performance. Canadian provinces are excluded from the map (shown in the table below).")

df = load_data()
filtered = render_filters(df, key_prefix="geo")

geo = geographic_summary(filtered)

if len(geo) == 0:
    st.warning("No US shipments match the current filters.")
else:
    metric_choice = st.radio(
        "Map metric",
        options=["Avg_Lead_Time", "Delay_Frequency_Pct", "Total_Shipments"],
        format_func=lambda x: {
            "Avg_Lead_Time": "Average Lead Time (days)",
            "Delay_Frequency_Pct": "Delay Frequency (%)",
            "Total_Shipments": "Shipment Volume",
        }[x],
        horizontal=True,
    )

    color_scale = "Blues" if metric_choice == "Total_Shipments" else "RdYlGn_r"
    fig = us_choropleth(
        geo,
        value_col=metric_choice,
        title=f"US Shipping Performance — {metric_choice.replace('_', ' ')}",
        color_scale=color_scale,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("Geographic Bottlenecks")
    st.caption("States with above-median shipment volume AND above-median lead time — these affect the most customers.")

    median_vol = geo["Total_Shipments"].median()
    median_lead = geo["Avg_Lead_Time"].median()
    bottlenecks = geo[
        (geo["Total_Shipments"] >= median_vol) & (geo["Avg_Lead_Time"] >= median_lead)
    ].sort_values("Total_Shipments", ascending=False)

    st.dataframe(bottlenecks, hide_index=True, use_container_width=True)

    st.divider()
    st.subheader("All States (Table View)")
    st.dataframe(geo.sort_values("Avg_Lead_Time", ascending=False), hide_index=True, use_container_width=True)

# Canada, shown separately since it can't go on a US choropleth
canada = filtered[filtered["Country/Region"] == "Canada"]
if len(canada) > 0:
    st.divider()
    st.subheader("Canada Shipments (not shown on map)")
    canada_summary = (
        canada.groupby("State/Province")
        .agg(
            Total_Shipments=("Order ID", "count"),
            Avg_Lead_Time=("Lead Time (Days)", "mean"),
            Delay_Frequency_Pct=("Delayed", lambda x: round(x.mean() * 100, 2)),
        )
        .reset_index()
    )
    st.dataframe(canada_summary, hide_index=True, use_container_width=True)
