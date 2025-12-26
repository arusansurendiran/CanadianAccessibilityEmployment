# An Analysis of Public Transit Access and Labour Force Outcomes across Canadian Cities, 2023 and 2024

## Overview


This repository contains the code and data used to analyse public transit accessibility across Canadian metropolitan cities, with data  sourced from Statistics Canada. Using a linear mixed-effects model to account for city-specific differences, the study analyzes the impact of transit proximity, population size, and relative commute times in 2023 and 2024.

To reproduce the analysis, please follow these steps:
1. Clone the repository to your local machine.
2. Ensure you have the required dependencies installed. You can find these in the `scripts/requirements.txt` file for Python and the `paper/_quarto.yml` file for R/Quarto.
3. Run the data cleaning scripts located in the `scripts/` directory to process the raw data.
4. Execute the modeling scripts to fit the linear mixed-effects model.
5. Finally, render the Quarto document in the `paper/` directory to generate the final report.


## File Structure

The repo is structured as:

-   `data/01-raw_data` contains the raw data as obtained from Statistics Canada.
-   `data/02-analysis_data` contains the cleaned dataset that was constructed.
-   `model` contains the fitted multiple regression model. 
-   `other` contains details about LLM chat interactions, and fonts for polished Quarto document rendering.
-   `paper` contains the files used to generate the paper, including the Quarto document and reference bibliography file, as well as the PDF of the paper. 
-   `scripts` contains the Python and R scripts used to download, clean and model data.

## Reproducible Instructions

To acesss this project, clone this repo or download as a ZIP file. Move the downloaded folder to where you want to work on your own computer.

Run scripts/00-utility_functions.py to set up utility functions.
Run scripts/01-download_data.py to download the raw dataset.
Run three scripts/02.x-clean_xxx_data.py to clean datasets.
Run scripts/03-analysis_data.py to summarize the datasets for the model.
Run scripts/04-test_data.py to validate the cleaned data.
Run scripts/05-install_packages.R to install required R packages.
Run scripts/06_model_data.R to model the data
Run outputs/canadian-transit-labour-analysis.qmd and render to generate the PDF of this paper.

## Statement on LLM usage

Aspects of the code and paper were written with the help of the Google Gemini and GitHub Copilot autocomplete. The complete chat history is available in other/llm_usage/gemini-usage.txt.