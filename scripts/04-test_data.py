#### Preamble ####
# Purpose: Test the analysis dataset is saved correctly.
# Author: Arusan Surendiran
# Date: 25 December 2025
# Contact: arusan.surendiran@utoronto.ca
# License: MIT
# Pre-requisites: 01-download_data.py, 02.1-clean_transit_data.py,
# 02.2-clean_labour_data.py, 02.3-clean_commute_data.py, 03-analysis_data.py


#### Workspace setup ####
import pandas as pd

### Read in the analysis dataset
analysis_data_path = "data/02-analysis_data/analysis_data.parquet"
analysis_data = pd.read_parquet(analysis_data_path)


#### Data Validation ####

# Initialize the pass variable
all_tests_passed = True

# 1. Check for Missing Values
missing_counts = analysis_data.isnull().sum()

if missing_counts.any():
    print("FAIL: Missing values detected!")
    print(missing_counts[missing_counts > 0])
    all_tests_passed = False
else:
    print("No missing values found.")

# 2. Verify Years (2023 and 2024 only)
expected_years = {2023, 2024}
actual_years = set(analysis_data["Year"].unique())

if actual_years == expected_years:
    print(f"Year range is correct.")
else:
    print(f"FAIL: Unexpected years found: {actual_years}")
    all_tests_passed = False

# 3. Check Numeric Column Types
numeric_cols = [
    "Population", "Log_Population", "Transit_Access_Prop", 
    "Avg_Commute_Car", "Avg_Commute_Transit", "Commute_Ratio", 
    "Participation_Rate", "Unemployment_Rate"
]

non_numeric_cols = [col for col in numeric_cols if not pd.api.types.is_numeric_dtype(analysis_data[col])]

if not non_numeric_cols:
    print("All analysis columns are numeric.")
else:
    print(f"FAIL: The following columns are NOT numeric: {non_numeric_cols}")
    all_tests_passed = False


# 4. Check the number of unique CMAs
expected_cma_count = 41
actual_cma_count = analysis_data["CMA_Name"].nunique()
if actual_cma_count == expected_cma_count:
    print(f"Correct number of CMAs: {actual_cma_count}")
else:
    print(f"FAIL: Expected {expected_cma_count} CMAs, found {actual_cma_count}")
    all_tests_passed = False


# Final Test Result
if all_tests_passed:
    print("PASS: All tests passed.")
else:
    print("One or more tests failed.")