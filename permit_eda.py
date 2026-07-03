from typing import Any

import pandas as pd
import numpy as np


def summarize_permits(df: pd.DataFrame) -> dict[str, Any]:
    required_columns = [
        "permitnum",
        "permittypemapped",
        "statuscurrent",
        "estprojectcost",
        "applieddate",
    ]
    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"DataFrame is missing required columns: {missing_columns}"
        )
    
    result = {}
    result['total_records'] = len(df)
    result['unique_permits'] = df['permitnum'].nunique()
    if df['applieddate'].isnull().all():
        result['application_date_min'] = None
        result['application_date_max'] = None
    else:
        result['application_date_min'] = df['applieddate'].min()
        result['application_date_max'] = df['applieddate'].max()
    if df['estprojectcost'].isnull().all():
        result['total_estimated_cost'] = 0.0
        result['median_estimated_cost'] = None
    else:
        result['total_estimated_cost'] = float(df['estprojectcost'].sum())
        result['median_estimated_cost'] = df['estprojectcost'].median()

    result['status_counts'] = df['statuscurrent'].value_counts().to_dict()
    result['permit_type_counts'] = df['permittypemapped'].value_counts().to_dict()
    result['missing_values'] = df.isnull().sum().to_dict()

    return result
