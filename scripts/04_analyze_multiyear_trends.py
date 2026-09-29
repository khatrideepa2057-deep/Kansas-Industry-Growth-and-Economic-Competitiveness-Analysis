import pandas as pd
from pathlib import Path

# Project folders
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "kansas_industry_multiyear_2021_2025.csv"
)

# Load historical dataset
df = pd.read_csv(DATA_FILE)

print("Historical dataset loaded successfully.")

print("\nShape:")
print(df.shape)

print("\nYears:")
print(sorted(df["year"].unique()))

print("\nNumber of industries:")
print(df["industry_name"].nunique())

# Get 2021 and 2025 employment values
employment_2021 = df[df["year"] == 2021][
    ["industry_code", "industry_name", "avg_quarterly_employment"]
].copy()

employment_2025 = df[df["year"] == 2025][
    ["industry_code", "avg_quarterly_employment"]
].copy()

# Rename columns
employment_2021 = employment_2021.rename(
    columns={"avg_quarterly_employment": "employment_2021"}
)

employment_2025 = employment_2025.rename(
    columns={"avg_quarterly_employment": "employment_2025"}
)

# Merge 2021 and 2025 data
growth_df = employment_2021.merge(
    employment_2025,
    on="industry_code"
)

# Calculate total employment growth percentage
growth_df["employment_growth_pct_2021_2025"] = (
    (growth_df["employment_2025"] - growth_df["employment_2021"])
    / growth_df["employment_2021"]
) * 100

growth_df = growth_df.sort_values(
    "employment_growth_pct_2021_2025",
    ascending=False
)

print("\n2021-2025 Employment Growth:")
print(
    growth_df[
        [
            "industry_name",
            "employment_2021",
            "employment_2025",
            "employment_growth_pct_2021_2025"
        ]
    ].to_string(index=False)
)

# Get 2021 and 2025 wage values
wage_2021 = df[df["year"] == 2021][
    ["industry_code", "industry_name", "avg_wkly_wage"]
].copy()

wage_2025 = df[df["year"] == 2025][
    ["industry_code", "avg_wkly_wage"]
].copy()

# Rename wage columns
wage_2021 = wage_2021.rename(
    columns={"avg_wkly_wage": "wage_2021"}
)

wage_2025 = wage_2025.rename(
    columns={"avg_wkly_wage": "wage_2025"}
)

# Merge 2021 and 2025 wage data
wage_growth_df = wage_2021.merge(
    wage_2025,
    on="industry_code"
)

# Calculate wage growth percentage
wage_growth_df["wage_growth_pct_2021_2025"] = (
    (wage_growth_df["wage_2025"] - wage_growth_df["wage_2021"])
    / wage_growth_df["wage_2021"]
) * 100

wage_growth_df = wage_growth_df.sort_values(
    "wage_growth_pct_2021_2025",
    ascending=False
)

print("\n2021-2025 Average Weekly Wage Growth:")
print(
    wage_growth_df[
        [
            "industry_name",
            "wage_2021",
            "wage_2025",
            "wage_growth_pct_2021_2025"
        ]
    ].to_string(index=False)
)

# Get 2025 location quotient
lq_2025 = df[df["year"] == 2025][
    ["industry_code", "lq_month3_emplvl"]
].copy()

lq_2025 = lq_2025.rename(
    columns={"lq_month3_emplvl": "lq_2025"}
)

# Combine employment growth, wage growth, and 2025 LQ
competitiveness_df = growth_df.merge(
    wage_growth_df[
        ["industry_code", "wage_growth_pct_2021_2025"]
    ],
    on="industry_code"
)

competitiveness_df = competitiveness_df.merge(
    lq_2025,
    on="industry_code"
)

# Keep important columns
competitiveness_df = competitiveness_df[
    [
        "industry_code",
        "industry_name",
        "employment_growth_pct_2021_2025",
        "wage_growth_pct_2021_2025",
        "lq_2025"
    ]
]

print("\nMulti-Year Industry Competitiveness Table:")
print(
    competitiveness_df
    .sort_values(
        "employment_growth_pct_2021_2025",
        ascending=False
    )
    .to_string(index=False)
)

# Classify multi-year industry competitiveness
def classify_multiyear(row):
    growth = row["employment_growth_pct_2021_2025"]
    lq = row["lq_2025"]

    if growth > 0 and lq > 1:
        return "Growing and Specialized"
    elif growth > 0 and lq <= 1:
        return "Growing but Less Specialized"
    elif growth <= 0 and lq > 1:
        return "Specialized but Declining"
    else:
        return "Declining and Less Specialized"


competitiveness_df["strategic_group"] = competitiveness_df.apply(
    classify_multiyear,
    axis=1
)

print("\nMulti-Year Strategic Groups:")
print(
    competitiveness_df[
        [
            "industry_name",
            "employment_growth_pct_2021_2025",
            "wage_growth_pct_2021_2025",
            "lq_2025",
            "strategic_group"
        ]
    ]
    .sort_values(
        ["strategic_group", "employment_growth_pct_2021_2025"],
        ascending=[True, False]
    )
    .to_string(index=False)
)

import matplotlib.pyplot as plt

# Create multi-year competitiveness scatter plot
plt.figure(figsize=(12, 8))

plt.scatter(
    competitiveness_df["lq_2025"],
    competitiveness_df["employment_growth_pct_2021_2025"]
)

# Add industry code labels
for _, row in competitiveness_df.iterrows():
    plt.annotate(
        row["industry_code"],
        (
            row["lq_2025"],
            row["employment_growth_pct_2021_2025"]
        )
    )

# Reference lines
plt.axvline(x=1.0, linestyle="--")
plt.axhline(y=0, linestyle="--")

plt.xlabel("2025 Location Quotient")
plt.ylabel("Employment Growth, 2021–2025 (%)")

plt.title(
    "Kansas Industry Competitiveness: "
    "2021–2025 Employment Growth vs. 2025 Location Quotient"
)

plt.tight_layout()

# Save chart
chart_file = (
    PROJECT_ROOT
    / "outputs"
    / "kansas_multiyear_growth_vs_lq.png"
)

plt.savefig(chart_file)

print("\nMulti-year competitiveness chart saved:")
print(chart_file)

plt.show()

# Create employment growth bar chart
growth_chart_df = competitiveness_df.sort_values(
    "employment_growth_pct_2021_2025",
    ascending=True
)

plt.figure(figsize=(12, 10))

plt.barh(
    growth_chart_df["industry_name"],
    growth_chart_df["employment_growth_pct_2021_2025"]
)

plt.axvline(x=0, linestyle="--")

plt.xlabel("Employment Growth, 2021–2025 (%)")
plt.ylabel("Industry")
plt.title("Kansas Industry Employment Growth, 2021–2025")

plt.tight_layout()

growth_chart_file = (
    PROJECT_ROOT
    / "outputs"
    / "kansas_industry_employment_growth_2021_2025.png"
)

plt.savefig(growth_chart_file)

print("\nEmployment growth chart saved:")
print(growth_chart_file)

plt.show()

# Save final competitiveness table
final_output_file = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "kansas_industry_competitiveness_2021_2025.csv"
)

competitiveness_df.to_csv(
    final_output_file,
    index=False
)

print("\nFinal competitiveness dataset saved:")
print(final_output_file)


