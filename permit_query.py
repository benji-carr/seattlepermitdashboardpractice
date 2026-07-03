from datetime import date


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


def build_permit_query_params(
    start_date: str,
    limit: int = 1000,
    offset: int = 0,
) -> dict[str, str | int]:
    if not isinstance(start_date, str):
        raise ValueError("date must be a string")
    
    try:
        parsed_date = date.fromisoformat(start_date)
    except ValueError as error:
        raise ValueError("start_date must be a valid date in YYYY-MM-DD format") from error
    
    if parsed_date.isoformat() != start_date:
        raise ValueError("start_date must be in YYYY-MM-DD format")

    if isinstance(limit, bool) or not isinstance(limit, int):
        raise ValueError("limit must be an integer")
    if limit < 1:
        raise ValueError("limit cannot be less than 1")
    
    if isinstance(offset, bool) or not isinstance(offset, int):
        raise ValueError("offset must be an integer")
    if offset < 0:
        raise ValueError("offset cannot be negative")
    
    params = {
        "$select": ",".join(PERMIT_COLUMNS),
        "$where": (f"applieddate >= '{start_date}T00:00:00.000'"),
        "$order": "applieddate DESC",
        "$limit": limit, 
        "$offset": offset,
    }

    return params




