#### Preamble ####
# Purpose: Merges cleaned transit, labour, and commute datasets for analysis
# Author: Arusan Surendiran
# Date:
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
transit_category = '500 metres from all public transit stops'
transit_characteristics = [
    'Total - Age groups of the population - 100% data',
    '15 to 64 years',
    '65 years and over',
    'Total - Population aged 15 years and over by labour force status - 25% sample data'
]

transit_filter = transit_data[
    (transit_data['Year'].isin(transit_years)) &
    (transit_data['Transit_Distance_Category'] == transit_category) &
    (transit_data['Transit_Profile_Characteristic'].isin(transit_characteristics)) &
    (transit_data['Transit_Unit_of_Measure'] == 'Percent')
]

transit_pivot = transit_filter.pivot_table(
    # Keep Year and Distance for more detail
    index=['CMA_ID', 'Transit_Distance_Category'],
    columns=['Transit_Profile_Characteristic', 'Year'],
    values='Transit_Value'
).reset_index()

# Clean Column Names
transit_pivot.columns = [''.join(map(str, col)).strip()
                         for col in transit_pivot.columns.values]


# LABOUR DATA

rate_metrics = ['Unemployment rate', 'Participation rate', 'Employment rate']
labour_years = ['2023', '2024']

# Labour metrics
is_rate_percent = (
    (labour_data['Labour_Metric'].isin(rate_metrics)) &
    (labour_data['Labour_Unit_of_Measure'] == 'Percent')
)

# Population, in 'Persons in thousands'
is_population = (
    (labour_data['Labour_Metric'] == 'Population') &
    (labour_data['Labour_Unit_of_Measure'] == 'Persons in thousands')
)

labour_filter = labour_data[
    (is_rate_percent | is_population) &
    (labour_data['Labour_Data_Type'] == 'Seasonally adjusted') &
    (labour_data['Year'].isin(labour_years))
]

# The labour data contains monthly entries; for our analysis, we will compute 
# annual averages.

# Compute mean of Labour_Value grouped by CMA_ID and Year, for Annual Metric
labour_aggregated = labour_filter.groupby(['CMA_ID', 'Labour_Metric', 'Year']).agg(
    Aggregated_Value=('Labour_Value', 'mean')
).reset_index()

labour_pivot = labour_aggregated.pivot_table(
    index=['CMA_ID'],
    columns=['Labour_Metric', 'Year'],
    values='Aggregated_Value'
).reset_index()

labour_pivot.columns = [''.join(map(str, col)).strip()
                        for col in labour_pivot.columns.values]


# COMMUTE DATA

commute_metrics = [
    'Total - Main mode of commuting',
    'Car, truck or van',
    'Public transit']

commute_filter = commute_data[
    (commute_data['Commute_Mode'].isin(commute_metrics))]


commute_pivot = commute_filter.pivot_table(
    index='CMA_ID',
    columns='Commute_Mode',
    values='Commute_Value'
).reset_index()

# Clean up column names by adding a prefix
rename_map = {}
for col in commute_pivot.columns:
    if col != 'CMA_ID':
        rename_map[col] = f'Commute_Avg_{col}'

commute_pivot.rename(columns=rename_map, inplace=True)


# MERGE DATASETS

# 1. Merge Commute and Transit data
first_merge = pd.merge(
    transit_pivot,
    commute_pivot,
    on='CMA_ID',
    how='left'
)

# 2. Merge with Labour data
second_merge = pd.merge(
    first_merge,
    labour_pivot,
    on='CMA_ID',
    how='left'
)

# Add the Census Metropolitan Area (CMA) names as a column
cma_mapping = transit_data[['CMA_ID', 'CMA']
                           ].drop_duplicates().reset_index(drop=True)
cma_mapping = cma_mapping.rename(columns={'CMA': 'CMA_Name'})

# Final merged dataset for analysis
analysis_data = pd.merge(
    second_merge,
    cma_mapping,
    on='CMA_ID',
    how='left'
)

# Reorder columns to have CMA_Name after CMA_ID
cols = analysis_data.columns.tolist()
cols.insert(1, cols.pop(cols.index('CMA_Name')))
analysis_data = analysis_data[cols]


# Polish the analysis dataset with clear column names.

# 1. Replace anything that is not alphanumeric or underscore with nothing
analysis_data.columns = analysis_data.columns.str.replace(
    r'[^a-zA-Z0-9_]', '', regex=True)

# 2. If a column starts with a digit, prefix it with 'Col_'
analysis_data.columns = [
    f"Col_{c}" if c[0].isdigit() else c
    for c in analysis_data.columns
]


# Create new variables for analysis

# 1. Log of population (in thousands) for better scaling
analysis_data['Log_Pop_2023'] = np.log(analysis_data['Population2023'])
analysis_data['Log_Pop_2024'] = np.log(analysis_data['Population2024'])

# 2. Transit Penalty Variable: Difference in average commute times between public transit and car/truck/van
analysis_data['Transit_Penalty'] = analysis_data['Commute_Avg_Publictransit'] - \
    analysis_data['Commute_Avg_Cartruckorvan']


print("Final analysis_data columns:")
for col in analysis_data.columns:
    print(col)

#### Save data ####
csv_path = "data/02-analysis_data/analysis_data.csv"
parquet_path = "data/02-analysis_data/analysis_data.parquet"

analysis_data.to_csv(csv_path, index=False)
analysis_data.to_parquet(parquet_path)
