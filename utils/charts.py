"""
Chart-building utilities for the Nassau Candy Shipping Analysis dashboard.
"""

import plotly.express as px
import pandas as pd

US_STATE_ABBREV = {
    "Alabama": "AL", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA",
    "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME",
    "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI",
    "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
    "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
    "New York": "NY", "North Carolina": "NC", "North Dakota": "ND",
    "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA",
    "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD",
    "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY",
}

SHIP_MODE_ORDER = ["Same Day", "First Class", "Second Class", "Standard Class"]


def route_leaderboard_bar(df: pd.DataFrame, top_n: int = 15):
    """Bar chart of top N routes by Route Efficiency Score."""
    top = df.head(top_n).sort_values("Route_Efficiency_Score")
    fig = px.bar(
        top,
        x="Route_Efficiency_Score",
        y="Route State",
        orientation="h",
        color="Route_Efficiency_Score",
        color_continuous_scale="Blues",
        title=f"Top {top_n} Routes by Efficiency Score",
        labels={"Route_Efficiency_Score": "Efficiency Score (0-100)"},
    )
    fig.update_layout(height=max(400, top_n * 30))
    return fig


def us_choropleth(df: pd.DataFrame, value_col: str, title: str, color_scale="RdYlGn_r"):
    """US state-level choropleth. value_col should already be state-aggregated."""
    plot_df = df.copy()
    plot_df["state_code"] = plot_df["State/Province"].map(US_STATE_ABBREV)
    plot_df = plot_df.dropna(subset=["state_code"])

    fig = px.choropleth(
        plot_df,
        locations="state_code",
        locationmode="USA-states",
        color=value_col,
        scope="usa",
        color_continuous_scale=color_scale,
        title=title,
        hover_data={"State/Province": True, "state_code": False},
    )
    return fig


def ship_mode_boxplot(df: pd.DataFrame):
    fig = px.box(
        df,
        x="Ship Mode",
        y="Lead Time (Days)",
        color="Ship Mode",
        title="Lead Time Distribution by Ship Mode",
        category_orders={"Ship Mode": SHIP_MODE_ORDER},
    )
    fig.update_layout(showlegend=False)
    return fig


def ship_mode_bar(summary_df: pd.DataFrame, y_col: str, title: str):
    fig = px.bar(
        summary_df,
        x="Ship Mode",
        y=y_col,
        color="Ship Mode",
        title=title,
        category_orders={"Ship Mode": SHIP_MODE_ORDER},
    )
    fig.update_layout(showlegend=False)
    return fig


def lead_time_histogram(df: pd.DataFrame):
    fig = px.histogram(
        df,
        x="Lead Time (Days)",
        nbins=8,
        title="Lead Time Distribution",
    )
    return fig


def order_timeline(df: pd.DataFrame, n: int = 50):
    """Order-level shipment timeline (Order Date -> Corrected Ship Date) for drill-down."""
    plot_df = df.sort_values("Order Date").tail(n).copy()
    fig = px.timeline(
        plot_df,
        x_start="Order Date",
        x_end="Corrected Ship Date",
        y="Order ID",
        color="Ship Mode",
        title=f"Shipment Timeline (most recent {n} orders in current filter)",
    )
    fig.update_yaxes(autorange="reversed", showticklabels=False)
    return fig
