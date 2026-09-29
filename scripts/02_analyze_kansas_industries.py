import pandas as pd
from pathlib import Path

# Project folders
PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "kansas_industry_q1_2025.csv"
)

# Load cleaned industry data
df = pd.read_csv(PROCESSED_DATA)

print("Dataset loaded successfully.")

print("\nNumber of industries:")
print(len(df))

print("\nColumns:")
print(df.columns.tolist())

# Sort industries by year-over-year employment growth
growth_df = df[
    [
        "industry_name",
        "avg_quarterly_employment",
        "oty_month3_emplvl_pct_chg"
    ]
].sort_values(
    "oty_month3_emplvl_pct_chg",
    ascending=False
)

print("\nIndustries ranked by employment growth:")
print(growth_df.to_string(index=False))

# Rank industries by employment location quotient
lq_df = df[
    [
        "industry_name",
        "avg_quarterly_employment",
        "lq_month3_emplvl"
    ]
].sort_values(
    "lq_month3_emplvl",
    ascending=False
)

print("\nIndustries ranked by Location Quotient:")
print(lq_df.to_string(index=False))

# Classify industries by growth and concentration
def classify_industry(row):
    growth = row["oty_month3_emplvl_pct_chg"]
    lq = row["lq_month3_emplvl"]

    if growth > 0 and lq > 1:
        return "Growing and Specialized"
    elif growth > 0 and lq <= 1:
        return "Growing but Less Specialized"
    elif growth <= 0 and lq > 1:
        return "Specialized but Declining"
    else:
        return "Declining and Less Specialized"


df["industry_category"] = df.apply(classify_industry, axis=1)

competitiveness_df = df[
    [
        "industry_name",
        "oty_month3_emplvl_pct_chg",
        "lq_month3_emplvl",
        "industry_category"
    ]
].sort_values(
    ["industry_category", "oty_month3_emplvl_pct_chg"],
    ascending=[True, False]
)

print("\nIndustry competitiveness classification:")
print(competitiveness_df.to_string(index=False))

import matplotlib.pyplot as plt

# Create competitiveness scatter plot
plt.figure(figsize=(12, 8))

plt.scatter(
    df["lq_month3_emplvl"],
    df["oty_month3_emplvl_pct_chg"]
)

# Add industry labels
for _, row in df.iterrows():
    plt.annotate(
        row["industry_code"],
        (
            row["lq_month3_emplvl"],
            row["oty_month3_emplvl_pct_chg"]
        )
    )

# Reference lines
plt.axvline(x=1.0, linestyle="--")
plt.axhline(y=0, linestyle="--")

plt.xlabel("Location Quotient")
plt.ylabel("Year-over-Year Employment Growth (%)")
plt.title("Kansas Industry Competitiveness: Growth vs. Concentration")

plt.tight_layout()

# Save chart
chart_file = (
    PROJECT_ROOT
    / "outputs"
    / "kansas_growth_vs_location_quotient.png"
)

plt.savefig(chart_file)

print("\nCompetitiveness chart saved:")
print(chart_file)

plt.show()

# Rank industries by average weekly wage
wage_df = df[
    [
        "industry_name",
        "avg_wkly_wage",
        "oty_avg_wkly_wage_pct_chg"
    ]
].sort_values(
    "avg_wkly_wage",
    ascending=False
)

print("\nIndustries ranked by average weekly wage:")
print(wage_df.to_string(index=False))

# Create a competitiveness scorecard
scorecard_df = df[
    [
        "industry_name",
        "avg_quarterly_employment",
        "oty_month3_emplvl_pct_chg",
        "lq_month3_emplvl",
        "avg_wkly_wage",
        "oty_avg_wkly_wage_pct_chg",
        "industry_category"
    ]
].copy()

# Sort by employment growth
scorecard_df = scorecard_df.sort_values(
    "oty_month3_emplvl_pct_chg",
    ascending=False
)

print("\nKansas Industry Competitiveness Scorecard:")
print(scorecard_df.to_string(index=False))

