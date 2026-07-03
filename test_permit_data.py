from permit_client import fetch_permit_page
from permit_data import permits_to_dataframe


records = fetch_permit_page(
    start_date="2026-01-01",
    limit=25,
)

df = permits_to_dataframe(records)

print(df.head())
print(df.dtypes)
print(df.isna().sum())