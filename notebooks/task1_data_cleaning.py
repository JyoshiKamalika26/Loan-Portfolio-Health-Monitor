import pandas as pd
import numpy as np
from pathlib import Path

# PROJECT ROOT
BASE_DIR = Path(__file__).resolve().parent.parent

# FILE PATHS
RAW_DATA = BASE_DIR / "data" / "raw" / "Lending club loan data.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "clean_loan_data.csv"

print("Reading File From:")
print(RAW_DATA)

# LOAD DATASET
df = pd.read_csv(RAW_DATA, low_memory=False)

# DATASET PROFILING
print("\nDataset Shape:", df.shape)
print("\nTotal Columns:", len(df.columns))

print("\nFirst 20 Columns:")
print(df.columns[:20].tolist())

print("\nDataset Info:")
print(df.info())

# MISSING VALUE ANALYSIS
null_count = df.isnull().sum()
null_percent = (null_count / len(df)) * 100

null_report = pd.DataFrame({
    "null_count": null_count,
    "null_percent": null_percent
})

null_report = null_report.sort_values(
    "null_percent",
    ascending=False
)

print("\nTop 10 Most Missing Columns:")
print(null_report.head(10))

# DROP HIGHLY MISSING COLUMNS
df = df.dropna(
    axis=1,
    thresh=len(df) * 0.60
)

# DROP USELESS IDS
df = df.drop(
    columns=["id", "member_id"],
    errors="ignore"
)

print("\nShape After Cleaning:")
print(df.shape)

# DATE CLEANING
date_cols = [
    "issue_d",
    "last_pymnt_d",
    "earliest_cr_line"
]

for col in date_cols:
    if col in df.columns:
        df[col] = pd.to_datetime(
            df[col],
            format="%b-%Y",
            errors="coerce"
        )

# CLEAN INTEREST RATE
if "int_rate" in df.columns:
    df["int_rate"] = (
        df["int_rate"]
        .astype(str)
        .str.replace("%", "", regex=False)
    )

    df["int_rate"] = pd.to_numeric(
        df["int_rate"],
        errors="coerce"
    )

# CLEAN REVOL UTIL
if "revol_util" in df.columns:
    df["revol_util"] = (
        df["revol_util"]
        .astype(str)
        .str.replace("%", "", regex=False)
    )

    df["revol_util"] = pd.to_numeric(
        df["revol_util"],
        errors="coerce"
    )

# CLEAN EMP LENGTH
if "emp_length" in df.columns:

    df["emp_length"] = (
        df["emp_length"]
        .astype(str)
        .str.replace("years", "", regex=False)
        .str.replace("year", "", regex=False)
        .str.replace("+", "", regex=False)
        .str.replace("< 1", "0", regex=False)
        .str.strip()
    )

    df["emp_length"] = pd.to_numeric(
        df["emp_length"],
        errors="coerce"
    )

# REMOVE EDGE CASES
if "loan_status" in df.columns:
    df = df[
        ~df["loan_status"]
        .astype(str)
        .str.contains(
            "Does not meet the credit policy",
            na=False
        )
    ]

# FEATURE ENGINEERING

# NPA FLAG
df["is_npa"] = (
    df["loan_status"]
    .isin(["Charged Off", "Default"])
    .astype(int)
)

# ISSUE YEAR
if "issue_d" in df.columns:
    df["issue_year"] = df["issue_d"].dt.year

# ISSUE MONTH
if "issue_d" in df.columns:
    df["issue_month"] = df["issue_d"].dt.month

# LOAN TO INCOME
if (
    "loan_amnt" in df.columns and
    "annual_inc" in df.columns
):
    df["loan_to_income"] = (
        df["loan_amnt"] /
        df["annual_inc"]
    )

# LOAN AGE
if (
    "issue_d" in df.columns and
    "last_pymnt_d" in df.columns
):
    df["loan_age_months"] = (
        (df["last_pymnt_d"] - df["issue_d"])
        .dt.days
    ) / 30

# GRADE NUMERIC
grade_map = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
    "F": 6,
    "G": 7
}

if "grade" in df.columns:
    df["grade_numeric"] = (
        df["grade"].map(grade_map)
    )

# COLUMN TYPE ANALYSIS
num_cols = df.select_dtypes(
    include=["int64", "float64"]
).columns

cat_cols = df.select_dtypes(
    include=["object"]
).columns

print("\nNumerical Columns:", len(num_cols))
print("Categorical Columns:", len(cat_cols))

print("\nNPA Distribution:")
print(df["is_npa"].value_counts())

# SAVE CLEANED DATA
<<<<<<< HEAD
df.to_csv(
    OUTPUT_FILE,
    index=False
)

=======
df.to_csv("data/processed/clean_loan_data.csv",index=False)
>>>>>>> db0b7a1589414591ab3076120e5a0ac4e7531605
print("\nCleaned dataset saved successfully!")

print("\nSaved To:")
print(OUTPUT_FILE)

print("\nFinal Shape:")
print(df.shape)