#### Preamble ####
# Purpose: Create regression models for participation rates
# Author: Arusan Surendiran
# Date: 25 December 2025
# Contact: arusan.surendiran@utoronto.ca
# License: MIT


#### Workspace setup ####
library(tidyverse)
library(arrow)
library(lme4)
library(lmerTest)

#### Read data ####
model_data <- read_parquet("data/02-analysis_data/analysis_data.parquet")

# Linear Mixed Model Regression for Participation Rates

formula_participation <- Participation_Rate ~
  Transit_Access_Prop +
    Commute_Ratio +
    Log_Population +
    as.factor(Year) +
    (1 | CMA_ID)

participation_model <- lmer(formula = formula_participation, data = model_data)

print(summary(participation_model))

#### Save models ####

saveRDS(
  participation_model,
  file = "models/participation_model.rds"
)
)