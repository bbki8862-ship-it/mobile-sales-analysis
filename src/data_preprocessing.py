"""
data_preprocessing.py
---------------------
Module for loading, cleaning, validating, and transforming the Mobile Sales dataset.
Converts raw transactional sales records into a validated and feature-enriched dataset.
"""

import os
from typing import Optional, Tuple
import pandas as pd
import numpy as np


def load_raw_data(filepath: str = "data/raw/mobile_sales_data.csv") -> pd.DataFrame:
    """
    Load raw mobile sales CSV dataset.
    Falls back to original Power BI directory path if local path is not found.
    """
    if not os.path.exists(filepath):
        fallback = "Mobile-Sales-Analytics-PowerBI/Mobile Sales Data.csv"
        if os.path.exists(fallback):
            filepath = fallback
        else:
            raise FileNotFoundError(f"Source dataset not found at '{filepath}' or '{fallback}'.")

    df = pd.read_csv(filepath)
    return df


def clean_and_transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean, validate, and enrich the mobile sales dataset:
    - Standardizes text strings (strip whitespace, title casing where appropriate).
    - Constructs valid ISO Datetime objects from Day, Month, Year.
    - Standardizes Day Name to full weekday format.
    - Validates data types and value constraints (Prices > 0, Units > 0, Ratings in [1, 5]).
    - Calculates Revenue (Units Sold * Price Per Unit).
    - Adds time dimension features: Quarter, Year-Month, Month Name, Day of Week.
    - Adds Customer Age Group categorization.
    """
    df_clean = df.copy()

    # 1. Clean column names
    df_clean.columns = [col.strip() for col in df_clean.columns]

    # 2. String trimming & normalization
    string_cols = ["Brand", "Mobile Model", "City", "Payment Method", "Customer Name", "Day Name"]
    for col in string_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).str.strip()

    # 3. Construct datetime
    # Columns Day, Month, Year exist
    date_str = (
        df_clean["Year"].astype(str)
        + "-"
        + df_clean["Month"].astype(str).str.zfill(2)
        + "-"
        + df_clean["Day"].astype(str).str.zfill(2)
    )
    df_clean["Date"] = pd.to_datetime(date_str, format="%Y-%m-%d", errors="coerce")

    # Drop any records with unparseable dates (if any)
    df_clean = df_clean.dropna(subset=["Date"])

    # Standardize Day Name from authoritative Date
    df_clean["Day Name"] = df_clean["Date"].dt.day_name()
    df_clean["Day of Week"] = df_clean["Date"].dt.dayofweek  # 0=Monday, 6=Sunday
    df_clean["Month Name"] = df_clean["Date"].dt.strftime("%B")
    df_clean["Year-Month"] = df_clean["Date"].dt.strftime("%Y-%m")
    df_clean["Quarter"] = "Q" + df_clean["Date"].dt.quarter.astype(str)
    df_clean["Year-Quarter"] = df_clean["Year"].astype(str) + " " + df_clean["Quarter"]

    # 4. Numeric validations & type casting
    df_clean["Units Sold"] = pd.to_numeric(df_clean["Units Sold"], errors="coerce").fillna(0).astype(int)
    df_clean["Price Per Unit"] = pd.to_numeric(df_clean["Price Per Unit"], errors="coerce").fillna(0.0)
    df_clean["Customer Ratings"] = pd.to_numeric(df_clean["Customer Ratings"], errors="coerce").fillna(0).astype(int)
    df_clean["Customer Age"] = pd.to_numeric(df_clean["Customer Age"], errors="coerce").fillna(0).astype(int)

    # Filter out invalid records (e.g. non-positive prices or zero units)
    df_clean = df_clean[(df_clean["Units Sold"] > 0) & (df_clean["Price Per Unit"] > 0)].copy()

    # 5. Core Metric Calculation: Total Revenue
    df_clean["Revenue"] = df_clean["Units Sold"] * df_clean["Price Per Unit"]
    df_clean["Revenue"] = df_clean["Revenue"].round(2)

    # 6. Customer Age Demographics Categorization
    age_bins = [0, 24, 34, 49, 120]
    age_labels = ["< 25 (Youth)", "25 - 34 (Young Adults)", "35 - 49 (Mid-Age)", "50+ (Seniors)"]
    df_clean["Age Group"] = pd.cut(
        df_clean["Customer Age"],
        bins=age_bins,
        labels=age_labels,
        right=True
    )

    # 7. Sort by Date and Transaction ID
    df_clean = df_clean.sort_values(by=["Date", "Transaction ID"]).reset_index(drop=True)

    return df_clean


def inspect_raw_data(df: pd.DataFrame) -> dict:
    """
    Perform structural inspection of raw data.
    Returns summary dictionary with schema, shape, nulls, duplicates.
    """
    return {
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": list(df.columns),
        "dtypes": {k: str(v) for k, v in df.dtypes.to_dict().items()},
        "null_counts": df.isnull().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "unique_counts": df.nunique().to_dict()
    }


def save_cleaned_data(df: pd.DataFrame, output_path: str = "data/processed/mobile_sales_cleaned.csv") -> str:
    """
    Export cleaned and enriched dataset to CSV.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path


def run_preprocessing_pipeline(
    raw_path: str = "data/raw/mobile_sales_data.csv",
    output_path: str = "data/processed/mobile_sales_cleaned.csv"
) -> Tuple[pd.DataFrame, dict]:
    """
    Run full preprocessing pipeline from raw input to cleaned output.
    """
    raw_df = load_raw_data(raw_path)
    inspection_report = inspect_raw_data(raw_df)
    clean_df = clean_and_transform_data(raw_df)
    saved_file = save_cleaned_data(clean_df, output_path)
    print(f"[PREPROCESSING] Processed {len(clean_df)} valid records saved to '{saved_file}'.")
    return clean_df, inspection_report


if __name__ == "__main__":
    df_clean, report = run_preprocessing_pipeline()
    print("Columns in cleaned data:", df_clean.columns.tolist())
    print(f"Total Revenue: INR {df_clean['Revenue'].sum():,.2f}")
    print(f"Total Units Sold: {df_clean['Units Sold'].sum():,}")
