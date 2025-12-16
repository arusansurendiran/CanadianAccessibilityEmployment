#### Preamble ####
# Purpose: Downloads and saves the data from Statistics Canada as a parquet
# Author: Arusan Surendiran
# Date: 1 December 2025
# Contact: arusan.surendiran@utoronto.ca
# License: MIT
# Pre-requisites: Download the Public Transit and Unemployment data from Statistics Canada
# The data was retrieved from the following link on 1 December 2025:
# https://www150.statcan.gc.ca/t1/tbl1/en/cv.action?pid=2310031301


#### Workspace setup ####
import pandas as pd
import os


#### Download data ####
raw_transit_path = "data/01-raw_data/public_transport_access.csv"
raw_labour_path = "data/01-raw_data/labour_rates1.csv"
raw_commute_path = "data/01-raw_data/commute_times1.csv"


#### Save data ####
public_transport_data = pd.read_csv(raw_transit_path)
labour_data = pd.read_csv(raw_labour_path)
commute_data = pd.read_csv(raw_commute_path)


transit_path = "data/01-raw_data/public_transport_access.parquet"
labour_path = "data/01-raw_data/labour_rates2.parquet"
commute_path = "data/01-raw_data/commute_times.parquet"

public_transport_data.to_parquet(transit_path, index=False)
labour_data.to_parquet(labour_path, index=False)
commute_data.to_parquet(commute_path, index=False)
