import pandas as pd
import pytest
from plotly.graph_objects import Figure

from permit_figures import (
    make_monthly_application_chart,
    make_status_bar_chart,
)

def test_status_chart_uses_top_n_counts():
    df = pd.DataFrame(
        {
            "statuscurrent": [
            "issued",
            "issued",
            "issued",
            "closed",
            "closed",
            "pending",
            "cancelled",
            None,
        ]
        }
        )
    fig = make_status_bar_chart(df, top_n=2)
    assert isinstance(fig, Figure)
    assert fig.data[0].type == "bar"
    assert list(fig.data[0].x) == ["issued", "closed"]
    assert list(fig.data[0].y) == [3, 2]
    assert fig.layout.title.text == "Top Permit Statuses"

@pytest.mark.parametrize(
    "top_n",
    [
        0,
        -1,
        True,
        1.5,
        "3",
    ],
)
def test_status_chart_rejects_invalid_top_n(top_n):
    df = pd.DataFrame(
        {
            "statuscurrent": [
            "issued",
            "issued",
            "issued",
            "closed",
            "closed",
            "pending",
            "cancelled",
            None,
        ]
        }
        )
    with pytest.raises(ValueError, match="top_n must be a positive integer"):
        make_status_bar_chart(df, top_n=top_n)
    

def test_status_chart_rejects_missing_column():
    df = pd.DataFrame()
    with pytest.raises(ValueError, match ="statuscurrent column is missing from the DataFrame"):
        make_status_bar_chart(df, top_n=2)

def test_monthly_chart_counts_and_sorts_months():
    df = pd.DataFrame(
        {
            "applieddate": [
            "2026-03-15",
            "2026-01-10",
            "2026-02-05",
            "2026-01-20",
            "bad date",
            None,
            "2026-03-01",
            ]
            }
            )
    fig = make_monthly_application_chart(df)
    actual_months = pd.to_datetime(
        list(fig.data[0].x)
        ).tolist()
    expected_months = pd.to_datetime(
        [
            "2026-01-01",
            "2026-02-01",
            "2026-03-01",
            ]
            ).tolist()
    assert actual_months == expected_months

def test_status_chart_handles_empty_data():
    df = pd.DataFrame(
        {
            "statuscurrent": [None, None]
            }
            )
    fig = make_status_bar_chart(df, top_n=2)
    assert isinstance(fig, Figure)

def test_monthly_chart_handles_empty_data():
    df = pd.DataFrame(
        {
            "applieddate": [None, None]
            }
            )
    fig = make_monthly_application_chart(df)
    assert isinstance(fig, Figure)

def test_monthly_chart_does_not_modify_input():
    df = pd.DataFrame(
        {
            "applieddate": [
                "2026-03-15",
                "2026-01-10",
                "2026-02-05",
                "2026-01-20",
                "bad date",
                None,
                "2026-03-01",
            ]
        }
    )

    original_df = df.copy(deep=True)

    make_monthly_application_chart(df)

    pd.testing.assert_frame_equal(df, original_df)