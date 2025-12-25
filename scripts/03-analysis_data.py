#### Preamble ####
# Purpose: Merge cleaned transit, labour, and commute datasets for analysis
# Author: Arusan Surendiran
# Date: 25 December 2025
# Contact: arusan.surendiran@utoronto.ca
# License: MIT
# Pre-requisites: 01-download_data.py, 02.1-clean_transit_data.py,
# 02.2-clean_labour_data.py, 02.3-clean_commute_data.py

#### Workspace setup ####
import pandas as pd
import numpy as np

# Read in the cleaned datasets
transit_data_path = "data/02-analysis_data/clean_transit_data.parquet"
labour_data_path = "data/02-analysis_data/clean_labour_data.parquet"
commute_data_path = "data/02-analysis_data/clean_commute_data.parquet"

transit_data = pd.read_parquet(transit_data_path)
labour_data = pd.read_parquet(labour_data_path)
commute_data = pd.read_parquet(commute_data_path)

# Pivot each dataset into a wide format for analysis and merging.

# TRANSIT DATA

# Characteristics of interest to keep for analysis
transit_years = [2023, 2024]
transit_category = "500 metres from all public transit stops"
transit_characteristics = ["15 to 64 years"]

transit_filter = transit_data[
    (transit_data["Year"].isin(transit_years))
    & (transit_data["Transit_Distance_Category"] == transit_category)
    & (transit_data["Transit_Profile_Characteristic"].isin(transit_characteristics))
    & (transit_data["Transit_Unit_of_Measure"] == "Percent")
]

transit_pivot = transit_filter.pivot_table(
    # Keep Year and Distance for more detail
    index=["CMA_ID", "Year"],
    columns=["Transit_Profile_Characteristic"],
    values="Transit_Value",
).reset_index()


# LABOUR DATA

rate_metrics = ["Unemployment rate", "Participation rate"]
labour_years = ["2023", "2024"]

# Labour metrics
is_rate_percent = (labour_data["Labour_Metric"].isin(rate_metrics)) & (
    labour_data["Labour_Unit_of_Measure"] == "Percent"
)

# Population, in 'Persons in thousands'
is_population = (labour_data["Labour_Metric"] == "Population") & (
    labour_data["Labour_Unit_of_Measure"] == "Persons in thousands"
)

labour_filter = labour_data[
    (is_rate_percent | is_population)
    & (labour_data["Labour_Data_Type"] == "Seasonally adjusted")
    & (labour_data["Year"].isin(labour_years))
]

# The labour data contains monthly entries; for our analysis, we will compute annual averages.

# Compute mean of Labour_Value grouped by CMA_ID and Year, for Annual Metric
labour_aggregated = (
    labour_filter.groupby(["CMA_ID", "Labour_Metric", "Year"])
    .agg(Aggregated_Value=("Labour_Value", "mean"))
    .reset_index()
)

# Ensure Year is integer for proper pivoting with transit data
labour_aggregated["Year"] = labour_aggregated["Year"].astype(int)

labour_pivot = labour_aggregated.pivot_table(
    index=["CMA_ID", "Year"], columns=["Labour_Metric"], values="Aggregated_Value"
).reset_index()


# COMMUTE DATA

commute_metrics = ["Car, truck or van", "Public transit"]

commute_filter = commute_data[(commute_data["Commute_Mode"].isin(commute_metrics))]


commute_pivot = commute_filter.pivot_table(
    index="CMA_ID", columns="Commute_Mode", values="Commute_Value"
).reset_index()

# Clean up column names by adding a prefix
rename_map = {}
for col in commute_pivot.columns:
    if col != "CMA_ID":
        rename_map[col] = f"Commute_Avg_{col}"

commute_pivot.rename(columns=rename_map, inplace=True)


# MERGE DATASETS

# 1. Merge Commute and Transit data
first_merge = pd.merge(transit_pivot, commute_pivot, on="CMA_ID", how="left")

# 2. Merge with Labour data
second_merge = pd.merge(first_merge, labour_pivot, on=["CMA_ID", "Year"], how="left")

# Add the Census Metropolitan Area (CMA) names as a column
cma_mapping = transit_data[["CMA_ID", "CMA"]].drop_duplicates().reset_index(drop=True)
cma_mapping = cma_mapping.rename(columns={"CMA": "CMA_Name"})

# Final merged dataset
analysis_data = pd.merge(second_merge, cma_mapping, on="CMA_ID", how="left")

# Rename columns for clarity
rename_dict = {
    "15 to 64 years": "Transit_Access_Prop",
    "Commute_Avg_Car, truck or van": "Avg_Commute_Car",
    "Commute_Avg_Public transit": "Avg_Commute_Transit",
    "Participation rate": "Participation_Rate",
    "Unemployment rate": "Unemployment_Rate",
}

analysis_data = analysis_data.rename(columns=rename_dict)

# Construct new variables

# 1. Commute Ratio (Transit time relative to Car time)
analysis_data["Commute_Ratio"] = (
    analysis_data["Avg_Commute_Transit"] / analysis_data["Avg_Commute_Car"]
)

# 2. Log Population (Logarithm of Population to reduce skewness)
analysis_data["Log_Population"] = np.log10(analysis_data["Population"])

final_cols = [
    "CMA_ID",
    "CMA_Name",
    "Year",
    "Population",
    "Log_Population",
    "Transit_Access_Prop",
    "Avg_Commute_Car",
    "Avg_Commute_Transit",
    "Commute_Ratio",
    "Participation_Rate",
    "Unemployment_Rate"
]

analysis_data = analysis_data[final_cols]

#### Save data ####

csv_path = "data/02-analysis_data/analysis_data.csv"
parquet_path = "data/02-analysis_data/analysis_data.parquet"

analysis_data.to_csv(csv_path, index=False)
analysis_data.to_parquet(parquet_path)
