# Group Contributions (CONTRIBUTIONS.md)

This document outlines the individual roles, ownership, code reviews, and key problem-solving contributions of each group member for Assignment 1 (Malaysian Household Income Audit). All members have reviewed and agreed to these contributions prior to submission.

## 1. Naurah (Matric: 314171)
* **Role:** Role 1 — Data Steward
* **Owned Functions & Notebook Sections:**
  * Task 1: Record inspection, `validate_records()`, and dataset structural validation.
  * Task 3: Focus-state vector calculations (median income changes, per-year dynamic gaps, Boolean masks for income drops, and mean-median gaps).
  * Extra Responsibilities: Initial dataset download via `fetch_data.py`, creation of `requirements.txt`, and the Setup section of `README.md`.
* **What Reviewed:** Task 2 functions (`index_by_key`, `join_records`, `to_float`).
* **Most Important Problem Found/Fixed as Reviewer:** Identified that `join_records` required strict checking for unmatched keys between the income and poverty datasets, ensuring missing years or states raised appropriate warnings or were handled cleanly without breaking matrix construction.


## 2. Irdina (Matric: 313819)
* **Role:** Role 2 — Structures Engineer
* **Owned Functions & Notebook Sections:**
  * Task 2: `index_by_key()`, `join_records()`, `to_float()`, and construction of the `MEDIAN`, `MEAN`, and `POVERTY` NumPy matrices (shape and row/column alignment).
* **What Reviewed:** Task 1 (`validate_records`) and Task 3 calculations.
* **Most Important Problem Found/Fixed as Reviewer:** Pointed out that `validate_records` needed a robust duplicate-detection check for `(state, date)` pairs to prevent indexing collisions during matrix shaping in Task 2.


## 3. Humaira (Matric: 313374)
* **Role:** Role 3 — Matrix Analyst A
* **Owned Functions & Notebook Sections:**
  * Task 4.1 to 4.5: State median statistics, 2016–2024 growth rates, highest/lowest income tracking by year, vectorized relative income index broadcasting, and threshold filtering (indices below 0.8 in 2024).
* **What Reviewed:** Task 4.6–4.7 and Task 5.1.
* **Most Important Problem Found/Fixed as Reviewer:** Resolved a broadcasting dimension alignment issue in the relative income index calculation to ensure division matched 1D state medians against the 16x5 matrix correctly.


## 4. Ainul (Matric: 313994)
* **Role:** Role 4 — Matrix Analyst B
* **Owned Functions & Notebook Sections:**
  * Task 4.6 to 4.7: Regional unweighted means using Boolean masks, region dictionary validation, and the absolute poverty/income divergence matrix.
  * Task 5.1: `build_state_profile()` function for JSON-serializable state profiles.
* **What Reviewed:** Task 4.1–4.5.
* **Most Important Problem Found/Fixed as Reviewer:** Caught a dictionary serialization bug in `build_state_profile()` where NumPy data types (like `np.float64`) caused `json.dumps()` to fail, enforcing native Python type conversions.


## 5. Khairina (Matric: 313989)
* **Role:** Role 5 — Integration & Test Lead
* **Owned Functions & Notebook Sections:**
  * Task 5.2: Comprehensive test suite and assertions (covering Tasks 1–5.1, boundary/error cases, and the focus-state matric function).
  * Task 5.3: Assembly of the focus-state comparison table and final group interpretation (200–300 words).
  * Task 5.4: Reproducibility verification (Python/NumPy versions and fresh kernel `Run All` validation).
  * Final Integration: Assembly and structuring of `assignment1.ipynb` and `README.md`.
* **What Reviewed:** Every function across all tasks.
* **Most Important Problem Found/Fixed as Reviewer:** Identified and resolved an import scope error regarding `get_focus_state` and matrix dependencies during the integration phase, ensuring the notebook executes cleanly from a fresh kernel without missing variable references.
