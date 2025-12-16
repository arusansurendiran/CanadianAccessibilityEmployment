#### Preamble ####
# Purpose: Defines utility functions for data processing tasks
# Author: Arusan Surendiran
# Date: 1 December 2025
# Contact: arusan.surendiran@utoronto.ca
# License: MIT
# Pre-requisites: None

#### Workspace setup ####
import pandas as pd

#### Define utility functions ####

def print_unique_values(df):

    """Prints unique values for each column in a DataFrame, showing up to 10 for columns with many unique values."""
    for col in df.columns:
        unique_vals = df[col].unique().tolist()
        num_unique = len(unique_vals)
        print(f"--- {col} ({num_unique} unique values) ---")
        if num_unique < 15:
            print(unique_vals)
        else:
            print(unique_vals[:10])
            print(f"... and {num_unique - 10} more")
        print("\n")
        


def check_id_consistency(df1, df2, id_col1, id_col2, name_col1=None, name_col2=None, label1="Dataset 1", label2="Dataset 2"):
    """
    Compares unique identifiers between two DataFrames to check for consistency.

    Args:
        df1, df2: The DataFrames to compare.
        id_col1, id_col2: The names of the ID columns to match on.
        name_col1, name_col2: (Optional) Descriptive columns to display alongside IDs. 
                              If None, only IDs are displayed.
        label1, label2: (Optional) String labels for the print output.
    """
    
    # Get unique IDs as sets
    ids_1 = set(df1[id_col1].unique())
    ids_2 = set(df2[id_col2].unique())

    # Find intersection and differences
    common_ids = ids_1 & ids_2
    only_in_1 = ids_1 - ids_2
    only_in_2 = ids_2 - ids_1
    
    # Helper to select columns for display
    cols_1 = [id_col1, name_col1] if name_col1 else [id_col1]
    cols_2 = [id_col2, name_col2] if name_col2 else [id_col2]

    print(f"--- Comparison: {label1} vs. {label2} ---\n")

    # Only in Dataset 1
    print(f"IDs only in {label1}: ({len(only_in_1)})")
    if only_in_1:
        display_df = df1[df1[id_col1].isin(only_in_1)][cols_1].drop_duplicates()
        print(display_df.to_string(index=False))
    else:
        print("None")
    print("-" * 40)

    # Only in Dataset 2
    print(f"IDs only in {label2}: ({len(only_in_2)})")
    if only_in_2:
        display_df = df2[df2[id_col2].isin(only_in_2)][cols_2].drop_duplicates()
        print(display_df.to_string(index=False))
    else:
        print("None")
    print("-" * 40)

    # Common to both
    print(f"IDs present in BOTH: ({len(common_ids)})")
    if common_ids:
        # Defaults to showing descriptive info from DF1
        display_df = df1[df1[id_col1].isin(common_ids)][cols_1].drop_duplicates()
        print(display_df.head(3).to_string(index=False)) # Limiting to 10 rows for readability
        if len(common_ids) > 3:
            print(f"...and {len(common_ids) - 3} more.")
    else:
        print("None")


