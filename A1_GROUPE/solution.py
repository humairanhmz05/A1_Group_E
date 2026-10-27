import numpy as np

SURVEY_YEARS = [2016, 2019, 2020, 2022, 2024]
POVERTY_YEARS = [2019, 2020, 2022, 2024]

REGIONS = {
    "Northern": ["Perlis", "Kedah", "Pulau Pinang", "Perak"],
    "Central": [
        "Selangor",
        "W.P. Kuala Lumpur",
        "W.P. Putrajaya",
        "Negeri Sembilan",
    ],
    "Southern": ["Melaka", "Johor"],
    "East Coast": ["Kelantan", "Terengganu", "Pahang"],
    "East Malaysia": ["Sabah", "Sarawak", "W.P. Labuan"],
}


def get_year(record: dict) -> int:
    """Get survey year from a record.
    Owner: Role 2. Reviewed by: Role 1.
    """
    return int(record["date"][:4])


def to_float(value) -> float:
    """Convert None to np.nan and other values to float.
    Owner: Role 2. Reviewed by: Role 1.
    """
    if value is None:
        return np.nan
    return float(value)

def validate_records(records: list[dict], required_keys: tuple[str, ...]) -> None:
    """Raise an informative exception if records are not usable."""

    if not isinstance(records, list):
        raise TypeError("records must be a list")

    if len(records) == 0:
        raise ValueError("records must not be empty")

    seen = set()

    for record in records:
        if not isinstance(record, dict):
            raise TypeError("Every record must be a dictionary")

        for key in required_keys:
            if key not in record:
                raise KeyError(
                    f"Record is missing required key: {key}"
                )

        key = (record["state"], record["date"])

        if key in seen:
            raise ValueError(
                f"Duplicate record found: {key}"
            )

        seen.add(key)

def index_by_key(records: list[dict]) -> dict:
    """Create a dictionary indexed by (state, year).
    Owner: Role 2. Reviewed by: Role 1.
    """
    indexed = {}

    for record in records:
        key = (record["state"], get_year(record))

        if key in indexed:
            raise ValueError(f"Duplicate key found: {key}")

        indexed[key] = record

    return indexed

def join_records(
    income_records: list[dict],
    poverty_records: list[dict]
) -> tuple:
    """Join income and poverty records using (state, year).
    Owner: Role 2. Reviewed by: Role 1.
    """
    income_index = index_by_key(income_records)
    poverty_index = index_by_key(poverty_records)

    income_keys = set(income_index.keys())
    poverty_keys = set(poverty_index.keys())

    common_keys = income_keys & poverty_keys
    income_only = income_keys - poverty_keys
    poverty_only = poverty_keys - income_keys

    joined = []

    for key in sorted(common_keys):
        joined.append({
            "state": key[0],
            "year": key[1],
            "income": income_index[key],
            "poverty": poverty_index[key]
        })

    return joined, sorted(income_only), sorted(poverty_only)       



def to_float(value) -> float:
    """Convert None to np.nan and other values to float.
    Owner: Role 2. Reviewed by: Role 1.
    """
    if value is None:
        return np.nan

    return float(value)
    