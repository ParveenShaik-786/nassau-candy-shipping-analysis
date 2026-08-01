import streamlit as st
from utils.preprocess import load_data
from utils.sidebar import render_filters
from utils.metrics import ship_mode_summary
from utils.charts import ship_mode_boxplot, ship_mode_bar

st.set_page_config(page_title="Ship Mode Comparison", page_icon="🚚", layout="wide")
st.title("🚚 Ship Mode Performance Comparison")

df = load_data()
filtered = render_filters(df, key_prefix="shipmode")

summary = ship_mode_summary(filtered)

if len(summary) == 0:
    st.warning("No shipments match the current filters.")
else:
    st.dataframe(summary, hide_index=True, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(ship_mode_boxplot(filtered), use_container_width=True)
    with col2:
        st.plotly_chart(
            ship_mode_bar(summary, "Delay_Frequency_Pct", "Delay Frequency by Ship Mode (%)"),
            use_container_width=True,
        )

    st.divider()
    st.markdown(
        "### Cost-time tradeoff\n"
        "Sales and cost in this dataset aren't tied to the shipping method chosen, "
        "so a direct cost-time tradeoff can't be derived from this data as-is. "
        "Descriptively: **Standard Class** carries both the longest lead times "
        "and is the only mode with meaningful delay risk, making it the primary "
        "target for operational improvement."
    )
