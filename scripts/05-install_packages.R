#### Preamble ####
# Purpose: Install all necessary packages for this paper's replication
# Author: Arusan Surendiran
# Date: 25 December 2025
# Contact: arusan.surendiran@utoronto.ca
# License: MIT
# Pre-requisites: None

# List of packages to install
packages <- c(
  "tidyverse",
  "arrow",
  "lme4",
  "lmerTest"
)

# Install packages if they are not already installed
for (package in packages) {
  if (!requireNamespace(package, quietly = TRUE)) {
    install.packages(package, dependencies = TRUE)
  }
}

# Load all packages
lapply(packages, library, character.only = TRUE)

print("Check complete: All packages installed and loaded.")
