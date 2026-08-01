"""
Shared sidebar filters used on every page: date range, region/state,
ship mode, and lead-time threshold slider (per project requirements).
"""

import streamlit as st
from utils.preprocess import apply_filters


def render_filters(df, key_prefix: str):
    """Render the standard filter sidebar and return the filtered dataframe.

    key_prefix must be unique per page so Streamlit widget keys don't collide
    across pages.
    """
    st.sidebar.header("Filters")

    min_date = df["Order Date"].min().date()
    max_date = df["Order Date"].max().date()
    date_range = st.sidebar.date_input(
        "Order Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key=f"{key_prefix}_date",
    )

    regions = st.sidebar.multiselect(
        "Region",
        options=sorted(df["Region"].unique()),
        default=[],
        key=f"{key_prefix}_region",
    )

    states = st.sidebar.multiselect(
        "State / Province",
        options=sorted(df["State/Province"].unique()),
        default=[],
        key=f"{key_prefix}_state",
    )

    ship_modes = st.sidebar.multiselect(
        "Ship Mode",
        options=sorted(df["Ship Mode"].unique()),
        default=[],
        key=f"{key_prefix}_shipmode",
    )

    max_lead = int(df["Lead Time (Days)"].max())
    lead_time_threshold = st.sidebar.slider(
        "Max Lead Time (Days)",
        min_value=0,
        max_value=max_lead,
        value=max_lead,
        key=f"{key_prefix}_leadtime",
    )

    filtered = apply_filters(
        df,
        date_range=date_range if len(date_range) == 2 else None,
        regions=regions if regions else None,
        states=states if states else None,
        ship_modes=ship_modes if ship_modes else None,
        max_lead_time=lead_time_threshold,
    )

    st.sidebar.caption(f"{len(filtered):,} of {len(df):,} shipments match current filters")

    return filtered
