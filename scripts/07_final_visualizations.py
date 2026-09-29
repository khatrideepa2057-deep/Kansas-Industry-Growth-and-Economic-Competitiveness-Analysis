import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# Project folders
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "kansas_industry_full_competitiveness_2021_2025.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "outputs"


# Load final dataset
df = pd.read_csv(DATA_FILE)

print("Final dataset loaded.")
print("Shape:", df.shape)


# ---------------------------------------------------------
# CHART 1: Employment Growth
# ---------------------------------------------------------

employment_df = df.sort_values(
    "employment_growth_pct_2021_2025",
    ascending=True
)

plt.figure(figsize=(12, 10))

plt.barh(
    employment_df["industry_name"],
    employment_df["employment_growth_pct_2021_2025"]
)

plt.axvline(x=0, linestyle="--")

plt.xlabel("Employment Growth, 2021–2025 (%)")
plt.ylabel("Industry")
plt.title("Kansas Industry Employment Growth, 2021–2025")

plt.tight_layout()

employment_chart = (
    OUTPUT_DIR
    / "final_employment_growth_2021_2025.png"
)

plt.savefig(employment_chart)
plt.close()

print("\nSaved:", employment_chart)


# ---------------------------------------------------------
# CHART 2: Nominal GDP Growth
# ---------------------------------------------------------

gdp_df = df.sort_values(
    "gdp_growth_pct_2021_2025",
    ascending=True
)

plt.figure(figsize=(12, 10))

plt.barh(
    gdp_df["industry_name"],
    gdp_df["gdp_growth_pct_2021_2025"]
)

plt.axvline(x=0, linestyle="--")

plt.xlabel("Nominal GDP Growth, 2021–2025 (%)")
plt.ylabel("Industry")
plt.title("Kansas Industry Nominal GDP Growth, 2021–2025")

plt.tight_layout()

gdp_chart = (
    OUTPUT_DIR
    / "final_gdp_growth_2021_2025.png"
)

plt.savefig(gdp_chart)
plt.close()

print("Saved:", gdp_chart)


# ---------------------------------------------------------
# CHART 3: Employment Growth vs Location Quotient
# ---------------------------------------------------------

plt.figure(figsize=(12, 8))

plt.scatter(
    df["lq_2025"],
    df["employment_growth_pct_2021_2025"]
)

for _, row in df.iterrows():
    plt.annotate(
        row["industry_code"],
        (
            row["lq_2025"],
            row["employment_growth_pct_2021_2025"]
        )
    )

plt.axvline(x=1.0, linestyle="--")
plt.axhline(y=0, linestyle="--")

plt.xlabel("2025 Location Quotient")
plt.ylabel("Employment Growth, 2021–2025 (%)")

plt.title(
    "Kansas Industry Competitiveness: "
    "Employment Growth vs. Specialization"
)

plt.tight_layout()

competitiveness_chart = (
    OUTPUT_DIR
    / "final_growth_vs_lq.png"
)

plt.savefig(competitiveness_chart)
plt.close()

print("Saved:", competitiveness_chart)


# ---------------------------------------------------------
# CHART 4: Employment Growth vs GDP Growth
# ---------------------------------------------------------

plt.figure(figsize=(12, 8))

plt.scatter(
    df["employment_growth_pct_2021_2025"],
    df["gdp_growth_pct_2021_2025"]
)

for _, row in df.iterrows():
    plt.annotate(
        row["industry_code"],
        (
            row["employment_growth_pct_2021_2025"],
            row["gdp_growth_pct_2021_2025"]
        )
    )

plt.axvline(x=0, linestyle="--")
plt.axhline(y=0, linestyle="--")

plt.xlabel("Employment Growth, 2021–2025 (%)")
plt.ylabel("Nominal GDP Growth, 2021–2025 (%)")

plt.title(
    "Kansas Industry Employment Growth vs. Nominal GDP Growth"
)

plt.tight_layout()

growth_relationship_chart = (
    OUTPUT_DIR
    / "final_employment_vs_gdp_growth.png"
)

plt.savefig(growth_relationship_chart)
plt.close()

print("Saved:", growth_relationship_chart)

