#### Preamble ####
# Purpose: Cleans the raw plane data recorded by two observers..... [...UPDATE THIS...]
# Author: Rohan Alexander [...UPDATE THIS...]
# Date: 6 April 2023 [...UPDATE THIS...]
# Contact: rohan.alexander@utoronto.ca [...UPDATE THIS...]
# License: MIT
# Pre-requisites: [...UPDATE THIS...]
# Any other information needed? [...UPDATE THIS...]

#### Workspace setup ####
import pandas as pd

#### Clean data ####

# Read in the raw data
parquet_path = "data/01-raw_data/public_transport_access.parquet"
transit_data = pd.read_parquet(parquet_path)

# Drop Census Metropolitan Areas (CMAs) with missing values
# Analysis verified that 1 CMA had no recorded data for public transit access
missing_mask = transit_data['VALUE'].isna()
cmas_to_drop = transit_data.loc[missing_mask, 'GEO'].unique()
transit_data = transit_data[~transit_data['GEO'].isin(cmas_to_drop)].copy()

# Keep only relevant columns
relevant_cols = [
    "GEO",
    "DGUID",
    "Distance-capacity public transit service area",
    "Demographic and socio-economic",
    "Sustainable Development Goals (SDGs) 11.2.1 indicator",
    "UOM",
    "VALUE"
]
transit_data = transit_data[relevant_cols].copy()

# Rename columns for clarity
transit_data = transit_data.rename(columns={
    "GEO": "CMA",
    "DGUID": "CMA_ID",
    "Distance-capacity public transit service area": "Transit_Distance_Category",
    "Demographic and socio-economic": "Profile_Characteristic",
    "Sustainable Development Goals (SDGs) 11.2.1 indicator": "Population_Measure",
    "UOM": "Population_Measure_Unit",
    "VALUE": "Population_Value"
})


# Change the values in 'CMA' by remove ", Census metropolitan area (CMA)" to make it cleaner
transit_data['CMA'] = transit_data['CMA'].str.replace(", Census metropolitan area (CMA)", "", regex=False)

# Create a copy of the cleaned data to be saved
clean_transit_data = transit_data.copy()


#### Save data ####
csv_path = "data/02-analysis_data/clean_transit_data.csv"
parquet_path = "data/02-analysis_data/clean_transit_data.parquet"

clean_transit_data.to_csv(csv_path, index=False)
clean_transit_data.to_parquet(parquet_path)