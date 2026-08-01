"""
Shared KPI calculation utilities for the Nassau Candy Shipping Analysis dashboard.
"""

import pandas as pd


def compute_summary_kpis(df: pd.DataFrame) -> dict:
    """Top-line KPIs shown at the top of every page."""
    if len(df) == 0:
        return {
            "total_shipments": 0,
            "avg_lead_time": 0,
            "delay_frequency_pct": 0,
            "total_sales": 0,
            "total_profit": 0,
        }

    return {
        "total_shipments": len(df),
        "avg_lead_time": round(df["Lead Time (Days)"].mean(), 2),
        "delay_frequency_pct": round(df["Delayed"].mean() * 100, 2),
        "total_sales": df["Sales"].sum(),
        "total_profit": df["Gross Profit"].sum(),
    }


def route_leaderboard(df: pd.DataFrame, min_shipments: int = 10) -> pd.DataFrame:
    """
    Recompute the Route Efficiency Score from a (possibly filtered) dataframe.
    Mirrors the logic in notebook 04_Route_Efficiency_Analysis.ipynb so the
    dashboard stays consistent with the notebooks even after filters are applied.
    """
    agg = df.groupby("Route State").agg(
        Total_Shipments=("Order ID", "count"),
        Avg_Lead_Time=("Lead Time (Days)", "mean"),
        Delay_Frequency_Pct=("Delayed", lambda x: round(x.mean() * 100, 2)),
        Total_Sales=("Sales", "sum"),
        Total_Gross_Profit=("Gross Profit", "sum"),
    ).reset_index()

    agg = agg[agg["Total_Shipments"] >= min_shipments].copy()

    if len(agg) == 0:
        return agg

    def normalize_inverse(series):
        rng = series.max() - series.min()
        if rng == 0:
            return pd.Series(100, index=series.index)
        return 100 * (series.max() - series) / rng

    agg["Lead_Time_Score"] = normalize_inverse(agg["Avg_Lead_Time"])
    agg["Delay_Score"] = normalize_inverse(agg["Delay_Frequency_Pct"])
    agg["Route_Efficiency_Score"] = (
        0.6 * agg["Lead_Time_Score"] + 0.4 * agg["Delay_Score"]
    ).round(1)

    return agg.sort_values("Route_Efficiency_Score", ascending=False)


def ship_mode_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Ship Mode")
        .agg(
            Total_Shipments=("Order ID", "count"),
            Avg_Lead_Time=("Lead Time (Days)", "mean"),
            Delay_Frequency_Pct=("Delayed", lambda x: round(x.mean() * 100, 2)),
            Avg_Sales=("Sales", "mean"),
            Avg_Gross_Profit=("Gross Profit", "mean"),
        )
        .reset_index()
        .sort_values("Avg_Lead_Time")
    )


def geographic_summary(df: pd.DataFrame) -> pd.DataFrame:
    """State-level aggregation for the geographic map, US only."""
    us = df[df["Country/Region"] == "United States"]
    return (
        us.groupby("State/Province")
        .agg(
            Total_Shipments=("Order ID", "count"),
            Avg_Lead_Time=("Lead Time (Days)", "mean"),
            Delay_Frequency_Pct=("Delayed", lambda x: round(x.mean() * 100, 2)),
        )
        .reset_index()
    )
