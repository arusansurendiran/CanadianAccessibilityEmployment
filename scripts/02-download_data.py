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

print("--- DEBUG INFO ---")
print(f"1. Current working directory: {os.getcwd()}")

#### Download data ####
raw_data_path = "../data/01-raw_data/public_transport_access.csv"


#### Save data ####
public_transport_data = pd.read_csv(raw_data_path)


output_path = "../data/01-raw_data/public_transport_access.parquet"
public_transport_data.to_parquet(output_path, index=False)
