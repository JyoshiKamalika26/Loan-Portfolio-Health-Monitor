import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Project root folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Load cleaned dataset
df = pd.read_csv(
    BASE_DIR / "data" / "processed" / "clean_loan_data.csv"
)

# Grade vs Purpose Heatmap
heatmap_data = pd.pivot_table(
    df,
    values="is_npa",
    index="grade",
    columns="purpose",
    aggfunc="mean"
) * 100

print("\nRisk Heatmap Data")
print(heatmap_data)

# Create Heatmap
plt.figure(figsize=(14, 8))

sns.heatmap(
    heatmap_data,
    annot=True,
    fmt=".1f",
    cmap="Reds"
)

plt.title("NPA Rate by Grade and Purpose")
plt.xlabel("Loan Purpose")
plt.ylabel("Loan Grade")

# Save PNG
plt.savefig(
    BASE_DIR / "outputs" / "risk_heatmap.png",
    bbox_inches="tight"
)

print("Heatmap saved successfully!")