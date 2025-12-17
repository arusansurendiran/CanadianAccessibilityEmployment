#### Preamble ####
# Purpose: Create regression models for participation and unemployment rates
# Author: Arusan Surendiran
# Date:
# Contact: arusan.surendiran@utoronto.ca
# License: MIT


#### Workspace setup ####
library(tidyverse)
library(arrow)

#### Read data ####
model_data <- read_parquet("data/02-analysis_data/analysis_data.parquet")

# Regression Model for Participation Rates: Year 2024

formula_final <- Participationrate2024 ~ Col_15to64years2024 +
  Transit_Penalty + Log_Pop_2024

participation_model_2024 <- lm(
  formula = formula_final,
  data = model_data
)

cat("REGRESSION MODEL: Participation Rates, 2024\n")
print(summary(participation_model_2024))

#### Save model ####
saveRDS(
  participation_model_2024,
  file = "models/participation_model_2024.rds"
)

# Regression Model for Participation Rates: Year 2023

formula_final <- Participationrate2023 ~ Col_15to64years2023 +
  Transit_Penalty + Log_Pop_2023

participation_model_2023 <- lm(
  formula = formula_final,
  data = model_data
)

cat("REGRESSION MODEL: Participation Rates, 2023\n")
print(summary(participation_model_2023))

#### Save model ####
saveRDS(
  participation_model_2023,
  file = "models/participation_model_2023.rds"
)

# Regression Model for Unemployment Rates: Year 2024

formula_final <- Unemploymentrate2024 ~ Col_15to64years2024 +
  Transit_Penalty + Log_Pop_2024

unemployment_model_2024 <- lm(
  formula = formula_final,
  data = model_data
)

cat("REGRESSION MODEL: Unemployment Rates, 2024\n")
print(summary(unemployment_model_2024))

#### Save model ####
saveRDS(
  unemployment_model_2024,
  file = "models/unemployment_model_2024.rds"
)

# Regression Model for Unemployment Rates: Year 2023

formula_final <- Unemploymentrate2023 ~ Col_15to64years2023 +
  Transit_Penalty + Log_Pop_2023

unemployment_model_2023 <- lm(
  formula = formula_final,
  data = model_data
)

cat("REGRESSION MODEL: Unemployment Rates, 2023\n")
print(summary(unemployment_model_2023))

#### Save model ####
saveRDS(
  unemployment_model_2023,
  file = "models/unemployment_model_2023.rds"
)