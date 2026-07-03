from typing import Any

import requests

from permit_query import build_permit_query_params


PERMIT_ENDPOINT = (
    "https://data.seattle.gov/"
    "resource/76t5-zqzr.json"
)


def fetch_permit_page(
    start_date: str,
    limit: int = 1000,
    offset: int = 0,
    timeout: float = 10.0,
) -> list[dict[str, Any]]:
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)):
        raise ValueError("timeout must be an integer or float")
    if timeout <= 0:
        raise ValueError("timeout must be larger than zero")
    
    params = build_permit_query_params(
        start_date=start_date,
        limit=limit,
        offset=offset,
    )

    response = requests.get(
        PERMIT_ENDPOINT,
        params=params,
        timeout=timeout,
    )

    response.raise_for_status()
    data = response.json()

    if not isinstance(data, list):
        raise ValueError("Top-level JSON is not a list")
    if not all(isinstance(item, dict) for item in data):
        raise ValueError("Not all items in JSON object are dictionaries")
    
    return data

if __name__ == "__main__":
    records = fetch_permit_page(
        start_date="2026-01-01",
        limit=5,
    )

    print(f"Number of records: {len(records)}")

    if records:
        print(records[0])