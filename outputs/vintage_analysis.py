import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Project root folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Load cleaned dataset
df = pd.read_csv(
    BASE_DIR / "data" / "processed" / "clean_loan_data.csv"
)

# Vintage Analysis
vintage = (
    df.groupby("issue_year")["is_npa"]
      .mean() * 100
)

print("\nNPA Rate by Vintage Year")
print(vintage)

# Create chart
plt.figure(figsize=(10, 5))

plt.plot(
    vintage.index,
    vintage.values,
    marker="o",
    linewidth=2
)

plt.title("NPA Rate by Vintage Year")
plt.xlabel("Issue Year")
plt.ylabel("NPA Rate (%)")
plt.grid(True)

# Save PNG
plt.savefig(
    BASE_DIR / "outputs" / "vintage_analysis.png",
    bbox_inches="tight"
)

print("Vintage chart saved successfully!")