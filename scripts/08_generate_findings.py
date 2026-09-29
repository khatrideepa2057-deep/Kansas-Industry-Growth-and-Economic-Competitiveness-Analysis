import pandas as pd
from pathlib import Path


# Project folders
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "kansas_industry_full_competitiveness_2021_2025.csv"
)


# Load final dataset
df = pd.read_csv(DATA_FILE)


# Fastest employment growth
top_employment = df.sort_values(
    "employment_growth_pct_2021_2025",
    ascending=False
).head(5)


# Fastest nominal GDP growth
top_gdp = df.sort_values(
    "gdp_growth_pct_2021_2025",
    ascending=False
).head(5)


# Highest specialization
top_lq = df.sort_values(
    "lq_2025",
    ascending=False
).head(5)


# Highest weekly wages
top_wages = df.sort_values(
    "wage_2025",
    ascending=False
).head(5)


# Growing and specialized industries
growing_specialized = df[
    df["strategic_group"] == "Growing and Specialized"
].sort_values(
    "employment_growth_pct_2021_2025",
    ascending=False
)


print("\nTOP 5 INDUSTRIES BY EMPLOYMENT GROWTH")
print(
    top_employment[
        [
            "industry_name",
            "employment_growth_pct_2021_2025"
        ]
    ].to_string(index=False)
)


print("\nTOP 5 INDUSTRIES BY NOMINAL GDP GROWTH")
print(
    top_gdp[
        [
            "industry_name",
            "gdp_growth_pct_2021_2025"
        ]
    ].to_string(index=False)
)


print("\nTOP 5 INDUSTRIES BY 2025 LOCATION QUOTIENT")
print(
    top_lq[
        [
            "industry_name",
            "lq_2025"
        ]
    ].to_string(index=False)
)


print("\nTOP 5 INDUSTRIES BY 2025 AVERAGE WEEKLY WAGE")
print(
    top_wages[
        [
            "industry_name",
            "wage_2025"
        ]
    ].to_string(index=False)
)


print("\nGROWING AND SPECIALIZED INDUSTRIES")
print(
    growing_specialized[
        [
            "industry_name",
            "employment_growth_pct_2021_2025",
            "gdp_growth_pct_2021_2025",
            "lq_2025"
        ]
    ].to_string(index=False)
)

