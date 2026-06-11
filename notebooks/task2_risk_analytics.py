import pandas as pd
import numpy as np
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

# LOAD DATA

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "processed" / "clean_loan_data.csv"

print("Reading Dataset:")
print(DATA_FILE)

df = pd.read_csv(DATA_FILE)

print("\nDataset Shape:")
print(df.shape)

# KPI 1 - NPA RATE

npa_rate = (df["is_npa"].sum() / len(df)) * 100

print("OVERALL NPA RATE")
print(f"NPA Rate: {npa_rate:.2f}%")

# NPA BY GRADE

npa_grade = (
    df.groupby("grade")["is_npa"]
    .mean() * 100
    ).sort_values()

print("\nNPA BY GRADE")
print(npa_grade)

plt.figure(figsize=(8,5))
sns.barplot(x=npa_grade.index, y=npa_grade.values)
plt.title("NPA Rate by Grade")
plt.ylabel("NPA %")
plt.show()

# NPA BY HOME OWNERSHIP

npa_home = (
    df.groupby("home_ownership")["is_npa"]
    .mean() * 100
    ).sort_values(ascending=False)

print("\nNPA BY HOME OWNERSHIP")
print(npa_home)

plt.figure(figsize=(8,5))
sns.barplot(x=npa_home.index, y=npa_home.values)
plt.title("NPA Rate by Home Ownership")
plt.ylabel("NPA %")
plt.xticks(rotation=45)
plt.show()

# NPA BY PURPOSE

npa_purpose = (
    df.groupby("purpose")["is_npa"]
    .mean() * 100
    ).sort_values(ascending=False)

print("\nTOP 10 RISKY PURPOSES")
print(npa_purpose.head(10))

plt.figure(figsize=(12,6))
sns.barplot(
    x=npa_purpose.head(10).index,
    y=npa_purpose.head(10).values
)

plt.title("Top Risky Loan Purposes")
plt.ylabel("NPA %")
plt.xticks(rotation=45)
plt.show()

# NPA BY VERIFICATION STATUS

npa_verify = (
    df.groupby("verification_status")["is_npa"]
    .mean() * 100
    ).sort_values(ascending=False)

print("\nNPA BY VERIFICATION STATUS")
print(npa_verify)

plt.figure(figsize=(8,5))
sns.barplot(
    x=npa_verify.index,
    y=npa_verify.values
)

plt.title("NPA by Verification Status")
plt.ylabel("NPA %")
plt.xticks(rotation=30)
plt.show()

# NPA BY ISSUE YEAR

npa_year = (
    df.groupby("issue_year")["is_npa"]
    .mean() * 100
)

print("\nNPA BY ISSUE YEAR")
print(npa_year)

plt.figure(figsize=(10,5))
plt.plot(
    npa_year.index,
    npa_year.values,
    marker="o"
)

plt.title("NPA Trend by Issue Year")
plt.ylabel("NPA %")
plt.grid(True)
plt.show()

# EMPLOYMENT LENGTH ANALYSIS

if "emp_length" in df.columns:

    emp_risk = (
        df.groupby("emp_length")["is_npa"]
        .mean() * 100
    )

    print("\nNPA BY EMPLOYMENT LENGTH")
    print(emp_risk)

    plt.figure(figsize=(10,5))
    plt.plot(
        emp_risk.index,
        emp_risk.values,
        marker="o"
    )

    plt.title("NPA by Employment Length")
    plt.ylabel("NPA %")
    plt.grid(True)
    plt.show()
    
# VINTAGE ANALYSIS

vintage = (
    df.groupby("issue_year")["is_npa"]
    .mean() * 100
)

print("\nVINTAGE ANALYSIS")
print(vintage)

plt.figure(figsize=(10,5))
plt.plot(
    vintage.index,
    vintage.values,
    marker="o"
)

plt.title("Vintage Analysis")
plt.ylabel("Default Rate (%)")
plt.xlabel("Issue Year")
plt.grid(True)
plt.show()

# REPAYMENT HEALTH

loan_status_summary = (
    df["loan_status"]
    .value_counts(normalize=True)
    * 100
)

print("\nREPAYMENT HEALTH")
print(loan_status_summary)

plt.figure(figsize=(8,8))

loan_status_summary.head(6).plot(
    kind="pie",
    autopct="%1.1f%%"
)

plt.ylabel("")
plt.title("Loan Status Distribution")
plt.show()

# RISK HEATMAP

risk_cols = [
    "loan_amnt",
    "annual_inc",
    "dti",
    "int_rate",
    "loan_to_income",
    "grade_numeric",
    "is_npa"
]

risk_cols = [
    col for col in risk_cols
    if col in df.columns
]

corr = df[risk_cols].corr()

plt.figure(figsize=(10,6))

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm"
)

plt.title("Risk Correlation Heatmap")
plt.show()

# EARLY WARNING FLAGS

conditions = [

    (
        (df["grade_numeric"] >= 6)
        &
        (df["dti"] > 20)
    ),

    (
        (df["grade_numeric"] >= 4)
    )
]

choices = [
    "High Risk",
    "Medium Risk"
]

df["risk_flag"] = np.select(
    conditions,
    choices,
    default="Low Risk"
)

print("\nRISK FLAG COUNTS")
print(df["risk_flag"].value_counts())

# FLAGGED ACCOUNTS

high_risk_accounts = (
    df[df["risk_flag"] == "High Risk"]
)

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "flagged_accounts.csv"
)

high_risk_accounts.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nFlagged Accounts Saved Successfully")
print(OUTPUT_FILE)

# TOP RISK SUMMARY

print("TASK 2 COMPLETED")

print(f"Total Loans : {len(df):,}")
print(f"NPA Rate    : {npa_rate:.2f}%")
print(f"High Risk   : {len(high_risk_accounts):,}")