"""
solution.py

Shared constants and functions for Assignment 1.
"""

import json
import numpy as np

# =====================
# Constants
# =====================

SURVEY_YEARS = [2016, 2019, 2020, 2022, 2024]

POVERTY_YEARS = [2019, 2020, 2022, 2024]

REGIONS = {
    "Northern": [
        "Perlis",
        "Kedah",
        "Pulau Pinang",
        "Perak"
    ],
    "Central": [
        "Selangor",
        "W.P. Kuala Lumpur",
        "W.P. Putrajaya"
    ],
    "Southern": [
        "Negeri Sembilan",
        "Melaka",
        "Johor"
    ],
    "East Coast": [
        "Kelantan",
        "Terengganu",
        "Pahang"
    ],
    "East Malaysia": [
        "Sabah",
        "Sarawak",
        "W.P. Labuan"
    ]
}

# =====================
# Data Loading Functions
# =====================

def load_json(filepath):
    """
    Load a JSON file and return its contents.

    Owner: Nurul (role 2).
    Reviewed by: <name> (role 1).
    """
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

# =====================
# Analysis Functions
# =====================

def get_state_income(data, state):
    """
    Return income data for a given state.

    Owner: <name> (role).
    Reviewed by: <name> (role).
    """
    return [row for row in data if row["state"] == state]


def get_state_poverty(data, state):
    """
    Return poverty data for a given state.

    Owner: <name> (role).
    Reviewed by: <name> (role).
    """
    return [row for row in data if row["state"] == state]


def calculate_average(values):
    """
    Calculate arithmetic mean.

    Owner: <name> (role).
    Reviewed by: <name> (role).
    """
    return np.mean(values)


def calculate_growth_rate(old_value, new_value):
    """
    Calculate percentage growth rate.

    Owner: <name> (role).
    Reviewed by: <name> (role).
    """
    return ((new_value - old_value) / old_value) * 100


# =====================
# Focus State Function
# =====================

def focus_state(data, state):
    """
    Filter records for the selected focus state.

    Owner: <name> (role).
    Reviewed by: <name> (role).
    """
    return [record for record in data if record["state"] == state]