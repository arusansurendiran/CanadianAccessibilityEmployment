#### Preamble ####
# Purpose: Cleans the raw labour rates and characteristics recorded by Statistics Canada
# Author: Arusan Surendiran
# Date: 
# Contact: arusan.surendiran@utoronto.ca
# License: MIT
# Pre-requisites: 02-clean_transit_data.py

#### Workspace setup ####
import pandas as pd
from utility_functions import print_unique_values, check_id_consistency

#### Clean data ####

# Read in the raw data
parquet_path = "data/01-raw_data/labour_rates.parquet"
labour_data = pd.read_parquet(parquet_path)

transit_data_path = "data/02-analysis_data/clean_transit_data.parquet"
transit_data = pd.read_parquet(transit_data_path)

# Check the unique IDs and names in the labour data
print(check_id_consistency(
    df1=transit_data,
    df2=labour_data,
    id_col1="CMA_ID",
    id_col2="DGUID",
    name_col1="CMA",
    name_col2="GEO",
    label1="Transit Data",
    label2="Labour Data"))

# To ensure consistency between datasets, we identified that the DGUID ‘2021S05031’ in the labour data corresponded to 
# St. John’s, matching the CMA_ID ‘2021S0503001’ in the transit data. Based on this partial match in city names, we 
# manually replaced the DGUID in the labour data to enable accurate merging.

labour_data['DGUID'] = labour_data['DGUID'].replace('2021S05031', '2021S0503001')

# No data was found for Saguenay, Quebec (DGUID ‘2021S0503408’) in the transit dataset, so this city was excluded.
# For Ottawa-Gatineau, Ontario/Quebec (DGUID ‘2021S0503505’), the city is split into Ontario and Quebec parts in 
# the transit data, which are already represented as separate entries; therefore, the combined DGUID was not used.

to_drop = ['2021S0503408', '2021S0503505']
labour_data = labour_data[~labour_data['DGUID'].isin(to_drop)].copy()

# Check ID consistency again after adjustments, should show no inconsistencies now
print(check_id_consistency(
    df1=transit_data,
    df2=labour_data,
    id_col1="CMA_ID",
    id_col2="DGUID",
    name_col1="CMA",
    name_col2="GEO",
    label1="Transit Data",
    label2="Labour Data"))

# Keep only relevant columns
relevant_cols = [
    "REF_DATE",
    "GEO",
    "DGUID",
    "Labour force characteristics",
    "Data type",
    "UOM",
    "VALUE"
]
clean_labour_data = labour_data[relevant_cols].copy()

clean_labour_data = labour_data.rename(columns={
    "REF_DATE": "Time_Period",
    "GEO": "CMA",
    "DGUID": "CMA_ID",
    "Labour force characteristics": "Labour_Metric",
    "Data type": "Labour_Data_Type",
    "UOM": "Labour_Unit_of_Measure",
    "VALUE": "Labour_Value"
})

# Create a 'Year' column by splitting the 'Time_Period' string
clean_labour_data['Year'] = clean_labour_data['Time_Period'].str.split('-').str[0]

#### Save data ####
csv_path = "data/02-analysis_data/clean_labour_data.csv"
parquet_path = "data/02-analysis_data/clean_labour_data.parquet"

clean_labour_data.to_csv(csv_path, index=False)
clean_labour_data.to_parquet(parquet_path)