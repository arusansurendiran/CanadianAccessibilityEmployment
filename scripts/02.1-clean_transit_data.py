#### Preamble ####
# Purpose: Cleans the raw public transit data recorded by Statistics Canada
# Author: Arusan Surendiran
# Date:
# Contact: arusan.surendiran@utoronto.ca
# License: MIT
# Pre-requisites: 01-download_data.py

#### Workspace setup ####
import pandas as pd
from utility_functions import print_unique_values

#### Clean data ####

# Read in the raw data
parquet_path = "data/01-raw_data/public_transport_access.parquet"
transit_data = pd.read_parquet(parquet_path)

# Drop Census Metropolitan Areas (CMAs) with missing values
missing_mask = transit_data['VALUE'].isna()
cmas_to_drop = transit_data.loc[missing_mask, 'GEO'].unique()
print("CMAs with missing values in VALUE:", cmas_to_drop)

# Analysis verified that 1 CMA had no recorded data for public transit access, so we will drop it entirely
transit_data = transit_data[~transit_data['GEO'].isin(cmas_to_drop)].copy()

# Keep only relevant columns
relevant_cols = [
    "GEO",
    "REF_DATE",
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
    "REF_DATE": "Year",
    "DGUID": "CMA_ID",
    "Distance-capacity public transit service area": "Transit_Distance_Category",
    "Demographic and socio-economic": "Transit_Profile_Characteristic",
    "Sustainable Development Goals (SDGs) 11.2.1 indicator": "Measure",
    "UOM": "Transit_Unit_of_Measure",
    "VALUE": "Transit_Value"
})

# Change the values in 'CMA' by removing the string ", Census metropolitan area (CMA)" to make it cleaner
transit_data['CMA'] = transit_data['CMA'].str.replace(
    ", Census metropolitan area (CMA)", "", regex=False)

# Create a copy of the cleaned data to be saved
clean_transit_data = transit_data.copy()

#### Save data ####
csv_path = "data/02-analysis_data/clean_transit_data.csv"
parquet_path = "data/02-analysis_data/clean_transit_data.parquet"

clean_transit_data.to_csv(csv_path, index=False)
clean_transit_data.to_parquet(parquet_path)

# print_unique_values(clean_transit_data)
