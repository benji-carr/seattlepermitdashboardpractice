from typing import Any

import pandas as pd


PERMIT_COLUMNS = [
    "permitnum",
    "permitclassmapped",
    "permittypemapped",
    "statuscurrent",
    "estprojectcost",
    "applieddate",
    "issueddate",
    "latitude",
    "longitude",
]


def permits_to_dataframe(
    records: list[dict[str, Any]],
) -> pd.DataFrame:
    if not isinstance(records, list):
        raise ValueError("Top-level JSON is not a list")
    if not all(isinstance(item, dict) for item in records):
        raise ValueError("Not all items in JSON object are dictionaries")
    
    df = pd.DataFrame.from_records(records)

    for column in PERMIT_COLUMNS:
        if column not in df.columns:
            df[column] = pd.NA

    numeric_columns = [
        "estprojectcost",
        "latitude",
        "longitude",
    ]   

    date_columns = [
        "applieddate",
        "issueddate",
    ]

    text_columns = [
        "permitnum",
        "permitclassmapped",
        "permittypemapped",
        "statuscurrent",
    ]

    cat_columns = [
        "permitclassmapped",
        "permittypemapped",
        "statuscurrent",
    ]
    # Lesson learned: for batch application of operations use apply, occasionally with lambda
    cleaned_df = df.copy()
    cleaned_df[numeric_columns] = cleaned_df[numeric_columns].apply(pd.to_numeric, errors='coerce')
    cleaned_df[date_columns] = cleaned_df[date_columns].apply(pd.to_datetime, errors='coerce')

    cleaned_df[text_columns] = cleaned_df[text_columns].apply(
        lambda column: column.str.strip())
    cleaned_df[cat_columns] = cleaned_df[cat_columns].apply(
        lambda column: column.str.lower()
    )

    cleaned_df = cleaned_df.reset_index(drop=True)
    cleaned_df = cleaned_df.reindex(columns=PERMIT_COLUMNS)
    return cleaned_df