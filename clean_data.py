import pandas as pd


def clean_rent_data(df: pd.DataFrame) -> pd.DataFrame:
    # Verify that all columns are present 
    required_columns = ['rent', 'sqfeet', 'beds', 'type']
    numeric_columns = ['rent', 'sqfeet', 'beds']

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    cleaned_df = df.copy()
    cleaned_df[numeric_columns] = cleaned_df[numeric_columns].apply(pd.to_numeric, errors='coerce')
    cleaned_df = cleaned_df.dropna(subset=['rent', 'sqfeet'], how='any')
    cleaned_df = cleaned_df[(cleaned_df['rent'] > 0) & (cleaned_df['sqfeet'] > 0) & (cleaned_df['beds'] >= 0)]
    cleaned_df['type'] = cleaned_df['type'].str.strip().str.lower()
    cleaned_df = cleaned_df.reset_index(drop=True)
    cleaned_df = cleaned_df.reindex(columns=['rent', 'sqfeet', 'beds', 'type'])
    return cleaned_df

df = pd.DataFrame(
    {
        "rent": ["1800", "bad", "2200", "-100"],
        "sqfeet": ["750", "900", None, "600"],
        "beds": ["1", "2", "3", "0"],
        "type": [" Apartment ", "HOUSE", "Townhouse", " Studio "],
        "irrelevant_column": [10, 20, 30, 40],
    }
)

print(clean_rent_data(df))