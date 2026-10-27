import numpy as np
import json

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
    Owner: Irdina(Role 2). Reviewed by: Naurah(Role 1).
    """
    return int(record["date"][:4])


def to_float(value) -> float:
    """Convert None to np.nan and other values to float.
    Owner: Irdina(Role 2). Reviewed by: Naurah(Role 1).
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
    Owner: Irdina(Role 2). Reviewed by: Naurah(Role 1).
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
    Owner: Irdina(Role 2). Reviewed by: Naurah(Role 1).
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
    Owner: Irdina(Role 2). Reviewed by: Naurah(Role 1).
    """
    if value is None:
        return np.nan

    return float(value)

def build_state_region_map(
    states: list[str],
    regions: dict[str, list[str]],
) -> dict[str, str]:
    """Map every state to exactly one region.

    Owner: Ainul (role 4).
    Reviewed by: Humaira (role 3).
    """
    if len(states) != len(set(states)):
        raise ValueError("The states list contains duplicate states.")

    memberships = {state: [] for state in states}

    for region_name, region_states in regions.items():
        for state in region_states:
            if state not in memberships:
                raise ValueError(
                    f"Region {region_name!r} contains unknown state {state!r}."
                )
            memberships[state].append(region_name)

    invalid = {
        state: assigned_regions
        for state, assigned_regions in memberships.items()
        if len(assigned_regions) != 1
    }

    if invalid:
        raise ValueError(
            f"Every state must belong to exactly one region: {invalid}"
        )

    return {
        state: assigned_regions[0]
        for state, assigned_regions in memberships.items()
    }


def calculate_region_means(
    states: list[str],
    years: list[int],
    median: np.ndarray,
    regions: dict[str, list[str]],
) -> dict[str, np.ndarray]:
    """Calculate unweighted mean state median income for each region and year.

    Owner: Ainul (role 4).
    Reviewed by: Humaira (role 3).
    """
    median = np.asarray(median, dtype=float)

    if median.shape != (len(states), len(years)):
        raise ValueError("MEDIAN shape does not match states and years.")

    state_to_region = build_state_region_map(states, regions)
    result = {}

    for region_name in regions:
        mask = np.array(
            [state_to_region[state] == region_name for state in states],
            dtype=bool,
        )

        region_values = median[mask, :]

        # Calculate across all years at once, ignoring missing values.
        valid = np.isfinite(region_values)
        totals = np.sum(np.where(valid, region_values, 0.0), axis=0)
        counts = np.sum(valid, axis=0)

        result[region_name] = np.divide(
            totals,
            counts,
            out=np.full(len(years), np.nan),
            where=counts > 0,
        )

    return result


def calculate_flagged_periods(
    states: list[str],
    income_years: list[int],
    median: np.ndarray,
    poverty_years: list[int],
    poverty: np.ndarray,
) -> tuple[np.ndarray, list[tuple[str, str]]]:
    """Flag periods when median income rises but absolute poverty does not fall.

    Owner: Ainul (role 4).
    Reviewed by: Humaira (role 3).
    """
    median = np.asarray(median, dtype=float)
    poverty = np.asarray(poverty, dtype=float)

    if median.shape != (len(states), len(income_years)):
        raise ValueError("MEDIAN shape does not match states and income years.")

    if poverty.shape != (len(states), len(poverty_years)):
        raise ValueError("POVERTY shape does not match states and poverty years.")

    periods = [(2019, 2020), (2020, 2022), (2022, 2024)]

    # Find the required columns from their year labels.
    income_indices = [
        (income_years.index(start), income_years.index(end))
        for start, end in periods
    ]
    poverty_indices = [
        (poverty_years.index(start), poverty_years.index(end))
        for start, end in periods
    ]

    flags = np.column_stack([
        (
            (median[:, income_end] > median[:, income_start])
            & (poverty[:, poverty_end] >= poverty[:, poverty_start])
        )
        for (income_start, income_end), (poverty_start, poverty_end)
        in zip(income_indices, poverty_indices)
    ])

    flagged = [
        (states[row], f"{start}-{end}")
        for row, column in zip(*np.where(flags))
        for start, end in [periods[column]]
    ]

    return flags, flagged


def build_state_profile(
    state: str,
    states: list[str],
    years: list[int],
    median: np.ndarray,
    mean: np.ndarray,
    poverty: np.ndarray,
    poverty_years: list[int],
    regions: dict[str, list[str]],
) -> dict:
    """Return a JSON-serializable profile for one state.

    Owner: Ainul (role 4).
    Reviewed by: Humaira (role 3).
    """
    if state not in states:
        raise ValueError(f"Unknown state: {state!r}")

    median = np.asarray(median, dtype=float)
    mean = np.asarray(mean, dtype=float)
    poverty = np.asarray(poverty, dtype=float)

    if median.shape != (len(states), len(years)):
        raise ValueError("MEDIAN shape does not match states and years.")

    if mean.shape != (len(states), len(years)):
        raise ValueError("MEAN shape does not match states and years.")

    if poverty.shape != (len(states), len(poverty_years)):
        raise ValueError("POVERTY shape does not match states and poverty years.")

    state_to_region = build_state_region_map(states, regions)
    row = states.index(state)

    def json_number(value):
        """Convert a NumPy number to a standard JSON-compatible value."""
        number = float(value)
        return number if np.isfinite(number) else None

    first_income = median[row, 0]
    last_income = median[row, -1]

    if (
        np.isfinite(first_income)
        and np.isfinite(last_income)
        and first_income != 0
    ):
        growth_percent = float(
            (last_income - first_income) / first_income * 100
        )
    else:
        growth_percent = None

    latest_values = median[:, -1]
    latest_state_income = latest_values[row]
    valid_latest = np.isfinite(latest_values)

    if np.isfinite(latest_state_income):
        national_median_of_state_medians = float(
            np.median(latest_values[valid_latest])
        )

        if national_median_of_state_medians != 0:
            relative_index = float(
                latest_state_income / national_median_of_state_medians
            )
        else:
            relative_index = None

        rank = int(
            1 + np.sum(
                latest_values[valid_latest] > latest_state_income
            )
        )
    else:
        relative_index = None
        rank = None

    region_name = state_to_region[state]
    region_means = calculate_region_means(
        states, years, median, regions
    )
    region_mean_latest = region_means[region_name][-1]

    if np.isfinite(latest_state_income) and np.isfinite(region_mean_latest):
        above_region_mean = bool(latest_state_income > region_mean_latest)
    else:
        above_region_mean = None

    _, all_flags = calculate_flagged_periods(
        states, years, median, poverty_years, poverty
    )
    state_flags = [
        period for flagged_state, period in all_flags
        if flagged_state == state
    ]

    profile = {
        "state": state,
        "region": region_name,
        "median_income_by_year": {
            str(year): json_number(median[row, col])
            for col, year in enumerate(years)
        },
        "mean_income_by_year": {
            str(year): json_number(mean[row, col])
            for col, year in enumerate(years)
        },
        "growth_percent_first_to_last": growth_percent,
        "relative_income_index_latest_year": relative_index,
        "rank_latest_year": rank,
        "region_mean_median_latest_year": json_number(region_mean_latest),
        "above_region_mean_latest_year": above_region_mean,
        "absolute_poverty_by_year": {
            str(year): json_number(poverty[row, col])
            for col, year in enumerate(poverty_years)
        },
        "flagged_periods": state_flags,
    }

    # Verify that the returned profile can be serialized.
    json.dumps(profile)

    return profile