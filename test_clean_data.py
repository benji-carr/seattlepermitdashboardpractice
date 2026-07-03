import pandas as pd
import pytest

from clean_data import clean_rent_data

def test_clean_rent_data_returns_expected_rows():
    raw_df = pd.DataFrame(
    {
        "rent": ["1800", "bad", "2200", "-100", "1500"],
        "sqfeet": ["750", "900", None, "600", "500"],
        "beds": ["1", "2", "3", "0", "-1"],
        "type": [
            " Apartment ",
            "HOUSE",
            "Townhouse",
            " Studio ",
            "Condo",
        ],
        "irrelevant_column": [10, 20, 30, 40, 50],
        }
    )

    expected_df = pd.DataFrame({"rent": [1800.0],
                                "sqfeet": [750.0],
                                "beds":[1],
                                "type":["apartment"]
                                })
    
    actual_df = clean_rent_data(raw_df)
    pd.testing.assert_frame_equal(actual_df, expected_df)

    
def test_clean_rent_data_rejects_missing_columns():
    df = pd.DataFrame(
    {
        "rent": ["1800", "bad", "2200", "-100", "1500"],
        "sqfeet": ["750", "900", None, "600", "500"],
        "irrelevant_column": [10, 20, 30, 40, 50],
        }
    )
    with pytest.raises(ValueError) as exception_info:
        clean_rent_data(df)

    message = str(exception_info.value)

    assert "beds" in message
    assert "type" in message

def test_clean_rent_data_does_not_modify_input():
    raw_df = pd.DataFrame(
    {
        "rent": ["1800", "bad", "2200", "-100", "1500"],
        "sqfeet": ["750", "900", None, "600", "500"],
        "beds": ["1", "2", "3", "0", "-1"],
        "type": [
            " Apartment ",
            "HOUSE",
            "Townhouse",
            " Studio ",
            "Condo",
        ],
        "irrelevant_column": [10, 20, 30, 40, 50],
        }
    )
    original_df = raw_df.copy(deep=True)

    clean_rent_data(raw_df)
    
    pd.testing.assert_frame_equal(raw_df, original_df)


def test_clean_rent_data_resets_index():
    raw_df = pd.DataFrame(
    {
        "rent": ["1800", "bad", "2200"],
        "sqfeet": ["750", "900", "200"],
        "beds": ["1", "2", "3"],
        "type": [
            " Apartment ",
            "HOUSE",
            "Townhouse"
        ]
        }
    )
    result = clean_rent_data(raw_df)
    assert list(result.index) == [0, 1]

def test_clean_rent_data_can_return_empty_dataframe():
    raw_df = pd.DataFrame(
    {
        "rent": ["-1800", "bad", "2200"],
        "sqfeet": ["750", "900", "-200"],
        "beds": ["1", "2", "3"],
        "type": [
            " Apartment ",
            "HOUSE",
            "Townhouse"
        ]
        }
    )
    result = clean_rent_data(raw_df)
    assert result.empty
    assert list(result.columns) == ["rent", "sqfeet", "beds", "type"]