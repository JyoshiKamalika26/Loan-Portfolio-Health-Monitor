import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

# ===================================================
# PATHS
# ===================================================
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "processed" / "clean_loan_data.csv"

OUTPUT_DIR = BASE_DIR / "outputs" / "charts"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# ===================================================
# LOAD DATA
# ===================================================
df = pd.read_csv(DATA_FILE)

print("Dataset Shape:", df.shape)

# ===================================================
# CREATE DASHBOARD
# ===================================================
fig, axes = plt.subplots(2, 3, figsize=(18, 10))

# 1. Loan Status Distribution
df["loan_status"].value_counts().plot(
    kind="bar",
    ax=axes[0, 0]
)

axes[0, 0].set_title("Loan Status Distribution")

# ===================================================
# 2. Loan Amount by Grade
# ===================================================
sns.boxplot(
    data=df,
    x="grade",
    y="loan_amnt",
    ax=axes[0, 1]
)

axes[0, 1].set_title("Loan Amount by Grade")

# ===================================================
# 3. NPA by Purpose
# ===================================================
purpose_npa = (
    df.groupby("purpose")["is_npa"]
    .mean()
    * 100
).sort_values(ascending=False).head(10)

sns.barplot(
    x=purpose_npa.index,
    y=purpose_npa.values,
    ax=axes[0, 2]
)

axes[0, 2].tick_params(
    axis="x",
    rotation=45
)

axes[0, 2].set_title("NPA by Purpose")

# ===================================================
# 4. NPA by Home Ownership
# ===================================================
home_npa = (
    df.groupby("home_ownership")["is_npa"]
    .mean()
    * 100
)

sns.barplot(
    x=home_npa.index,
    y=home_npa.values,
    ax=axes[1, 0]
)

axes[1, 0].set_title(" \n \n NPA by Home Ownership")

# ===================================================
# 5. Loans Issued Per Year
# ===================================================
df["issue_year"].value_counts().sort_index().plot(
    kind="line",
    marker="o",
    ax=axes[1, 1]
)

axes[1, 1].set_title("Loans Issued Per Year")

# ===================================================
# 6th Panel Empty
# ===================================================
axes[1, 2].axis("off")

plt.tight_layout()

# ===================================================
# SAVE IMAGE
# ===================================================
plt.savefig(
    OUTPUT_DIR / "eda_dashboard.png",
    dpi=300,
    bbox_inches="tight"
)

print("\nEDA Dashboard saved successfully!")

plt.show()