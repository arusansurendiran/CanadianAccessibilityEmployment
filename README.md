# An Analysis of Public Transit Access and Labour Force Outcomes across Canadian Cities, 2023 and 2024

## Overview


This repository contains the code and data used to analyse public transit accessibility across Canadian metropolitan cities, with data  sourced from Statistics Canada. Using a linear mixed-effects model to account for city-specific differences, the study analyzes the impact of transit proximity, population size, and relative commute times in 2023 and 2024.

## File Structure

The repo is structured as:

-   `data/01-raw_data` contains the raw data as obtained from Statistics Canada.
-   `data/02-analysis_data` contains the cleaned dataset that was constructed.
-   `model` contains the fitted multiple regression model. 
-   `other` contains details about LLM chat interactions, and fonts for polished Quarto document rendering.
-   `paper` contains the files used to generate the paper, including the Quarto document and reference bibliography file, as well as the PDF of the paper. 
-   `scripts` contains the Python and R scripts used to download, clean and model data.


## Statement on LLM usage

Aspects of the code and paper were written with the help of the Google Gemini. The complete chat history is available in other/llm_usage/gemini-usage.txt.