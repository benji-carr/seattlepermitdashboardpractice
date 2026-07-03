from typing import Any

import requests


def fetch_records(
    endpoint: str,
    limit: int = 100,
    offset: int = 0,
    timeout: float = 10.0,
) -> list[dict[str, Any]]:
    if not isinstance(endpoint, str) or not endpoint.strip():
        raise ValueError("endpoint must be a non-empty string")
    # Below please note that bools can sneak through as ints so we do a check for bools
    if isinstance(limit, bool) or not isinstance(limit, int):
        raise ValueError("limit must be an integer")
    if limit < 1:
        raise ValueError("Limit cannot be less than 1")

    if isinstance(offset, bool) or not isinstance(offset, int):
        raise ValueError("offset must be an integer")
    if offset < 0:
        raise ValueError("Offset cannot be negative")

    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)):
        raise ValueError("timout must be an integer or float")
    if timeout <= 0:
        raise ValueError("Timeout must be larger than zero")
    # End type and value checking

    params = {
        "$limit": limit,
        "$offset": offset,
    }

    response = requests.get(endpoint, params=params, timeout=timeout)
    response.raise_for_status()
    data = response.json()

    if not isinstance(data, list):
        raise ValueError("Top-level JSON is not a list")
    if not all(isinstance(item, dict) for item in data):
        raise ValueError("Not all items in JSON object are dictionaries")
    
    return data

# HI HI LOOK AT ME I'M A COMMENT INDICATING THAT THIS IS AN OLD TEST COMMENTED OUT
#if __name__ == "__main__":
#    endpoint = (
#        "https://data.seattle.gov/"
#        "resource/76t5-zqzr.json"
#    )
#
#    records = fetch_records(
#        endpoint,
#        limit=5,
#    )
#
#    print(f"Received {len(records)} records")
#    print(records[0])

def fetch_all_records(
    endpoint: str,
    page_size: int = 100,
    timeout: float = 10.0,
) -> list[dict[str, Any]]:
    
    if isinstance(page_size, bool) or not isinstance(page_size, int):
        raise ValueError("page_size must be an integer")
    if page_size < 1:
        raise ValueError("page_size cannot be less than one")

    all_records = []
    offset = 0 

    while True:
        page = fetch_records(
            endpoint, 
            limit=page_size, 
            offset=offset, 
            timeout=timeout
            )
        all_records.extend(page)

        if len(page) < page_size:
            break

        offset += page_size
        
    return all_records
    