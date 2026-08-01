"""
Data loading utilities for the Nassau Candy Shipping Analysis dashboard.

IMPORTANT: This loads the CLEANED dataset (data/processed/Nassau_Candy_Cleaned.csv),
not the raw source file. The raw file's Ship Date column is corrupted (see
notebook 02_Data_Cleaning_Feature_Engineering.ipynb for the full diagnosis) --
"Lead Time (Days)" here is a corrected/simulated field derived from Ship Mode,
not the raw date difference. Do not point this at the raw CSV.
"""

import pandas as pd
import streamlit as st


@st.cache_data
def load_data(path: str = "data/processed/Nassau_Candy_Cleaned.csv") -> pd.DataFrame:
    """Load the cleaned Nassau Candy dataset with proper dtypes."""
    df = pd.read_csv(path)

    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])
    df["Corrected Ship Date"] = pd.to_datetime(df["Corrected Ship Date"])

    return df


@st.cache_data
def load_route_state_aggregates(path: str = "data/processed/route_state_aggregates.csv") -> pd.DataFrame:
    return pd.read_csv(path)


@st.cache_data
def load_route_region_aggregates(path: str = "data/processed/route_region_aggregates.csv") -> pd.DataFrame:
    return pd.read_csv(path)


@st.cache_data
def load_efficiency_leaderboard(path: str = "data/processed/route_efficiency_leaderboard.csv") -> pd.DataFrame:
    return pd.read_csv(path)


def apply_filters(
    df: pd.DataFrame,
    date_range=None,
    regions=None,
    states=None,
    ship_modes=None,
    max_lead_time=None,
) -> pd.DataFrame:
    """Apply the shared sidebar filters used across every dashboard page."""
    filtered = df.copy()

    if date_range and len(date_range) == 2:
        start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        filtered = filtered[(filtered["Order Date"] >= start) & (filtered["Order Date"] <= end)]

    if regions:
        filtered = filtered[filtered["Region"].isin(regions)]

    if states:
        filtered = filtered[filtered["State/Province"].isin(states)]

    if ship_modes:
        filtered = filtered[filtered["Ship Mode"].isin(ship_modes)]

    if max_lead_time is not None:
        filtered = filtered[filtered["Lead Time (Days)"] <= max_lead_time]

    return filtered
