import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# Project folders
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "kansas_shift_share_2021_2025.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "outputs"


# Load shift-share results
df = pd.read_csv(DATA_FILE)

print("Shift-share dataset loaded.")
print("Shape:", df.shape)


# Sort industries by competitive effect
chart_df = df.sort_values(
    "competitive_effect",
    ascending=True
)


# Create horizontal bar chart
plt.figure(figsize=(12, 10))

plt.barh(
    chart_df["industry_name"],
    chart_df["competitive_effect"]
)

# Zero reference line
plt.axvline(
    x=0,
    linestyle="--"
)

plt.xlabel("Competitive Effect (Estimated Jobs)")
plt.ylabel("Industry")

plt.title(
    "Kansas Industry Shift-Share Competitive Effect, 2021–2025"
)

plt.tight_layout()


# Save chart
chart_file = (
    OUTPUT_DIR
    / "final_shift_share_competitive_effect.png"
)

plt.savefig(
    chart_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


print("\nShift-share chart saved:")
print(chart_file)

