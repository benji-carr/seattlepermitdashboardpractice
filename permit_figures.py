import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure


def make_status_bar_chart(
    df: pd.DataFrame,
    top_n: int = 10,
) -> Figure:
    if "statuscurrent" not in df.columns:
        raise ValueError("statuscurrent column is missing from the DataFrame")
    
    if isinstance(top_n, bool) or not isinstance(top_n, int) or top_n <= 0:
        raise ValueError("top_n must be a positive integer")
    
    plot_df = df.copy()
    counts = (
        plot_df["statuscurrent"]
        .value_counts()
        .head(top_n)
        .rename_axis("status")
        .reset_index(name="count")
        )
    fig = px.bar(
        counts,
        x="status",
        y="count",
        title=f"Top Permit Statuses",
        labels={"status": "Permit Status", "count": "Number of Permits"},
    )
    return fig

def make_monthly_application_chart(
    df: pd.DataFrame,
) -> Figure:
    if "applieddate" not in df.columns:
        raise ValueError("applieddate column is missing from the DataFrame")
    plot_df = df.copy()
    plot_df["applieddate"] = pd.to_datetime(plot_df["applieddate"], errors="coerce")
    plot_df = plot_df.dropna(subset=["applieddate"])
    
    plot_df["month"] = (
        plot_df["applieddate"]
        .dt.to_period("M")
        .dt.to_timestamp()
        )
    monthly_counts = (
        plot_df
        .groupby("month")
        .size()
        .reset_index(name="count")
        .sort_values("month")
        )

    fig = px.line(
        monthly_counts,
        x="month",
        y="count",
        title="Permit Applications by Month",
        labels={"month": "Application Month", "count": "Number of Applications"},
    )
    return fig

