#### Preamble ####
# Purpose: Cleans the raw labour rates and characteristics recorded by Statistics Canada
# Author: Arusan Surendiran
# Date: 
# Contact: arusan.surendiran@utoronto.ca
# License: MIT
# Pre-requisites: 03-clean_transit_data.py

#### Workspace setup ####
import pandas as pd
from utility_functions import print_unique_values, check_id_consistency

#### Clean data ####

# Read in the raw data
parquet_path = "data/01-raw_data/commute_times.parquet"
commute_data = pd.read_parquet(parquet_path)

transit_data_path = "data/02-analysis_data/clean_transit_data.parquet"
transit_data = pd.read_parquet(transit_data_path)

print(check_id_consistency(
    df1=transit_data,
    df2=commute_data,
    id_col1="CMA_ID",
    id_col2="DGUID",
    name_col1="CMA",
    name_col2="GEO",
    label1="Transit Data",
    label2="Commute Data"))

# There are inconsistencies with Ottawa-Gatineau, Ontario/Quebec (DGUID ‘2021S0503505’) in the commute data.
# In the transit data, Ottawa-Gatineau is split into two parts: Ontario part (DGUID ‘2021S050535505’) and Quebec part (DGUID ‘2021S050524505’).
# To resolve this, we will split the Ottawa-Gatineau data in the commute dataset into two separate entries, one for each part.

unified_dguid = '2021S0503505'
id_quebec_part = '2021S050524505'
id_ontario_part = '2021S050535505'


# Isolate rows for the unified DGUID
ottawa_unified_rows = commute_data[commute_data['DGUID'] == unified_dguid].copy()

# Split Dataset: Quebec Part
ottawa_quebec_part = ottawa_unified_rows.copy()
ottawa_quebec_part['DGUID'] = id_quebec_part
ottawa_quebec_part['GEO'] = 'Ottawa-Gatineau, Quebec part, Ontario/Quebec'

# Split Dataset 2: Ontario Part
ottawa_ontario_part = ottawa_unified_rows.copy()
ottawa_ontario_part['DGUID'] = id_ontario_part
ottawa_ontario_part['GEO'] = 'Ottawa-Gatineau, Ontario part, Ontario/Quebec'

# Combine the new split datasets ---
ottawa_split_data = pd.concat([ottawa_quebec_part, ottawa_ontario_part])

# Filter out original unified DGUID rows from the main DataFrame and add the split rows
commute_data_filter = commute_data[commute_data['DGUID'] != unified_dguid].copy()
commute_data = pd.concat([commute_data_filter, ottawa_split_data])


# Check ID consistency again after adjustments, should show no inconsistencies now
print(check_id_consistency(
    df1=transit_data,
    df2=commute_data,
    id_col1="CMA_ID",
    id_col2="DGUID",
    name_col1="CMA",
    name_col2="GEO",
    label1="Transit Data",
    label2="Commute Data"))


# Keep only relevant columns
relevant_cols = [
    "GEO",
    "DGUID",
    "Main mode of commuting (21)",
    "Commuting duration (7)",
    "VALUE"
]
commute_data = commute_data[relevant_cols].copy()

commute_data = commute_data.rename(columns={
    "GEO": "CMA",
    "DGUID": "CMA_ID",
    "Main mode of commuting (21)": "Commute_Mode",
    "Commuting duration (7)": "Average_Commute_Duration",
    "VALUE": "Commute_Value"
})

# Create a copy of the cleaned data to be saved
clean_commute_data = transit_data.copy()

#### Save data ####
csv_path = "data/02-analysis_data/clean_commute_data.csv"
parquet_path = "data/02-analysis_data/clean_commute_data.parquet"

clean_commute_data.to_csv(csv_path, index=False)
clean_commute_data.to_parquet(parquet_path)