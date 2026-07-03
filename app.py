import pandas as pd
from dash import Dash, dcc, html

from permit_eda import summarize_permits
from permit_figures import (
    make_monthly_application_chart,
    make_status_bar_chart,
)

import pandas as pd
from dash import Dash, Input, Output, dcc, html

from permit_eda import summarize_permits
from permit_figures import (
    make_monthly_application_chart,
    make_status_bar_chart,
)

from pathlib import Path
from permit_snapshot import load_permit_snapshot

DEFAULT_SNAPSHOT_DIRECTORY = Path("data/processed")

def create_app(df: pd.DataFrame) -> Dash:
    """Create a Dash application from a prepared permit DataFrame."""

    if not isinstance(df, pd.DataFrame):
        raise ValueError("df must be a pandas DataFrame")

    if "permittypemapped" not in df.columns:
        raise ValueError(
            "permittypemapped column is missing from the DataFrame"
        )

    # Calculate the initial dashboard values using all records.
    summary = summarize_permits(df)

    initial_status_figure = make_status_bar_chart(
        df,
        top_n=8,
    )

    initial_monthly_figure = make_monthly_application_chart(df)

    # Format the summary-card values.
    total_records_text = f"{summary['total_records']:,}"
    unique_permits_text = f"{summary['unique_permits']:,}"

    total_cost = summary["total_estimated_cost"]

    if total_cost is None:
        total_cost_text = "N/A"
    else:
        total_cost_text = f"${total_cost:,.0f}"

    minimum_date = summary["application_date_min"]
    maximum_date = summary["application_date_max"]

    if minimum_date is None or maximum_date is None:
        date_range_text = "No application dates available"
    else:
        date_range_text = (
            f"{minimum_date:%Y-%m-%d} "
            f"to {maximum_date:%Y-%m-%d}"
        )

    # Find the permit types that will appear in the dropdown.
    permit_types = sorted(
        df["permittypemapped"]
        .dropna()
        .unique()
        .tolist()
    )

    # Start with a special option representing the entire DataFrame.
    permit_type_options = [
        {
            "label": "All Permit Types",
            "value": "__all__",
        }
    ]

    # Add one dropdown option for each permit type.
    for permit_type in permit_types:
        permit_type_options.append(
            {
                "label": permit_type.title(),
                "value": permit_type,
            }
        )

    app = Dash(__name__)

    app.layout = html.Div(
        [
            html.H1("Seattle Building Permit Dashboard"),

            html.Div(
                [
                    html.H3("Filter by Permit Type"),

                    dcc.Dropdown(
                        id="permit-type-filter",
                        options=permit_type_options,
                        value="__all__",
                        clearable=False,
                    ),
                ]
            ),

            html.Div(
                [
                    html.Div(
                        [
                            html.H3("Total Records"),
                            html.P(
                                total_records_text,
                                id="total-records-card",
                            ),
                        ]
                    ),

                    html.Div(
                        [
                            html.H3("Unique Permits"),
                            html.P(
                                unique_permits_text,
                                id="unique-permits-card",
                            ),
                        ]
                    ),

                    html.Div(
                        [
                            html.H3("Total Estimated Cost"),
                            html.P(
                                total_cost_text,
                                id="total-cost-card",
                            ),
                        ]
                    ),

                    html.Div(
                        [
                            html.H3("Application Date Range"),
                            html.P(
                                date_range_text,
                                id="date-range-card",
                            ),
                        ]
                    ),
                ]
            ),

            dcc.Graph(
                id="status-chart",
                figure=initial_status_figure,
            ),

            dcc.Graph(
                id="monthly-chart",
                figure=initial_monthly_figure,
            ),
        ]
    )

    @app.callback(
        Output("status-chart", "figure"),
        Output("monthly-chart", "figure"),
        Input("permit-type-filter", "value"),
    )
    def update_charts(
        selected_permit_type: str,
    ):
        """Update both charts when the permit-type dropdown changes."""

        if selected_permit_type == "__all__":
            filtered_df = df.copy()
        else:
            filtered_df = df[
                df["permittypemapped"] == selected_permit_type
            ].copy()

        updated_status_figure = make_status_bar_chart(
            filtered_df,
            top_n=8,
        )

        updated_monthly_figure = (
            make_monthly_application_chart(filtered_df)
        )

        return (
            updated_status_figure,
            updated_monthly_figure,
        )

    return app

def create_app_from_snapshot(
    snapshot_directory: str | Path = DEFAULT_SNAPSHOT_DIRECTORY,
) -> Dash:
    df, metadata = load_permit_snapshot(snapshot_directory)
    app = create_app(df)
    return app

dashboard = create_app_from_snapshot()
server = dashboard.server

if __name__ == "__main__":
    dashboard.run(debug=True)
