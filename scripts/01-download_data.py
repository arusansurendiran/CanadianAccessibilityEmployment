#### Preamble ####
# Purpose: Saves Statistics Canada CSV datasets as Parquet files for access
# Author: Arusan Surendiran
# Date: 25 December 2025
# Contact: arusan.surendiran@utoronto.ca
# License: MIT
# Pre-requisites: None
# The data was retrieved as .csv files from the following links on 1 December 2025:

# Public Transit Access:
# https://www150.statcan.gc.ca/t1/tbl1/en/cv!recreate.action?pid=2310031301&selectedNodeIds=1D14,1D94,1D122,1D154,1D170,1D197,1D223,1D317,1D334,1D372,1D394,1D411,1D470,1D474,1D479,1D498,1D504,1D508,1D518,1D523,1D530,1D555,1D559,1D572,1D595,1D608,1D621,1D648,1D689,1D726,1D746,1D784,1D798,1D835,1D847,1D865,1D878,1D933,1D943,1D963,1D1054,1D1100,2D1,2D2,2D3,2D4,3D1,4D1,5D1,5D2,5D3,5D6,5D56,5D57,5D58,5D59,5D60&checkedLevels=5D1&refPeriods=20230101,20240101&dimensionLayouts=layout3,layout2,layout2,layout2,layout2,layout2,layout2&vectorDisplay=false

# Labour Rates:
# https://www150.statcan.gc.ca/t1/tbl1/en/cv!recreate.action?pid=1410045901&selectedNodeIds=3D1&checkedLevels=0D3,0D4,1D1,3D1&refPeriods=20230101,20241201&dimensionLayouts=layout3,layout2,layout2,layout2,layout2&vectorDisplay=false

# Commute Times:
# https://www150.statcan.gc.ca/t1/tbl1/en/cv!recreate.action?pid=9810050401&selectedNodeIds=3D2,3D11,3D12,4D7&checkedLevels=0D1,1D1,2D1&refPeriods=20210101,20210101&dimensionLayouts=layout3,layout2,layout2,layout2,layout2&vectorDisplay=false


#### Workspace setup ####
import pandas as pd
import os


#### Download data ####
raw_transit_path = "data/01-raw_data/public_transport_access.csv"
raw_labour_path = "data/01-raw_data/labour_rates.csv"
raw_commute_path = "data/01-raw_data/commute_times.csv"


#### Save data ####
public_transport_data = pd.read_csv(raw_transit_path)
labour_data = pd.read_csv(raw_labour_path)
commute_data = pd.read_csv(raw_commute_path)


### Save as Parquet files ###
transit_path = "data/01-raw_data/public_transport_access.parquet"
labour_path = "data/01-raw_data/labour_rates.parquet"
commute_path = "data/01-raw_data/commute_times.parquet"

public_transport_data.to_parquet(transit_path, index=False)
labour_data.to_parquet(labour_path, index=False)
commute_data.to_parquet(commute_path, index=False)
