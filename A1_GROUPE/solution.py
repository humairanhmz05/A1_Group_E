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
