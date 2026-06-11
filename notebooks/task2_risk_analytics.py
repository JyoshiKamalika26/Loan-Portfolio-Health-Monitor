import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "processed" / "clean_loan_data.csv"
df = pd.read_csv(DATA_FILE)
print("Dataset Shape:", df.shape)
# Overall NPA Rate
npa_rate = (df["is_npa"].sum() / len(df)) * 100
print(f"\nOverall NPA Rate: {npa_rate:.2f}%")
# NPA by Grade
npa_grade = df.groupby("grade")["is_npa"].mean() * 100
print("\nNPA BY GRADE")
print(npa_grade)
# NPA by Home Ownership
npa_home = df.groupby("home_ownership")["is_npa"].mean() * 100
print("\nNPA BY HOME OWNERSHIP")
print(npa_home)
# NPA by Purpose
npa_purpose = df.groupby("purpose")["is_npa"].mean() * 100
print("\nNPA BY PURPOSE")
print(npa_purpose.sort_values(ascending=False).head(10))
# NPA by Verification Status
npa_verify = df.groupby("verification_status")["is_npa"].mean() * 100
print("\nNPA BY VERIFICATION STATUS")
print(npa_verify)
# NPA by Issue Year
npa_year = df.groupby("issue_year")["is_npa"].mean() * 100
print("\nNPA BY ISSUE YEAR")
print(npa_year)
# Employment Length Analysis
if "emp_length" in df.columns:
    emp_risk = df.groupby("emp_length")["is_npa"].mean() * 100
    print("\nNPA BY EMPLOYMENT LENGTH")
    print(emp_risk)
# Vintage Analysis
vintage = df.groupby("issue_year")["is_npa"].mean() * 100
print("\nVINTAGE ANALYSIS")
print(vintage)
# Repayment Health
loan_status_summary = df["loan_status"].value_counts(normalize=True) * 100
print("\nREPAYMENT HEALTH")
print(loan_status_summary)
# Early Warning Flags
conditions = [
    ((df["grade_numeric"] >= 6) & (df["dti"] > 20)),
    (df["grade_numeric"] >= 4)
]
choices = ["High Risk", "Medium Risk"]
df["risk_flag"] = np.select(
    conditions,
    choices,
    default="Low Risk"
)
print("\nRISK FLAG COUNTS")
print(df["risk_flag"].value_counts())
high_risk_accounts = df[df["risk_flag"] == "High Risk"]
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "flagged_accounts.csv"
high_risk_accounts.to_csv(OUTPUT_FILE, index=False)
print("\nFlagged Accounts Saved Successfully")
print(OUTPUT_FILE)
print("\nTASK 2 COMPLETED")
print(f"Total Loans: {len(df):,}")
print(f"NPA Rate: {npa_rate:.2f}%")
print(f"High Risk Loans: {len(high_risk_accounts):,}")
fig, axes = plt.subplots(1, 2, figsize=(18, 6))

# Chart 1: Vintage Trend
vintage = df.groupby("issue_year")["is_npa"].mean() * 100

axes[0].plot(
    vintage.index,
    vintage.values,
    marker="o"
)
axes[0].set_title("NPA Rate by Vintage Year")
axes[0].set_xlabel("Issue Year")
axes[0].set_ylabel("NPA Rate (%)")
axes[0].grid(True)

# Chart 2: Risk Heatmap
pivot = pd.pivot_table(
    df,
    values="is_npa",
    index="grade",
    columns="purpose",
    aggfunc="mean"
) * 100

sns.heatmap(
    pivot,
    annot=True,
    cmap="Reds",
    fmt=".1f",
    ax=axes[1]
)

axes[1].set_title("Risk Concentration Heatmap")

plt.tight_layout()
plt.show()