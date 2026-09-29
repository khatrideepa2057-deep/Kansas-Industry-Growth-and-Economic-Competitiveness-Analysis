import pandas as pd
from pathlib import Path


# Project folders
PROJECT_ROOT = Path(__file__).resolve().parents[1]

BLS_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "kansas_industry_multiyear_2021_2025.csv"
)

BEA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "kansas_industry_gdp_2021_2025.csv"
)


# Load datasets
bls_df = pd.read_csv(BLS_FILE)
bea_df = pd.read_csv(BEA_FILE)


print("BLS dataset shape:")
print(bls_df.shape)

print("\nBEA dataset shape:")
print(bea_df.shape)

print("\nBLS industries:")
print(bls_df["industry_name"].nunique())

print("\nBEA industries:")
print(bea_df["industry_name"].nunique())


# Merge BLS and BEA datasets
combined_df = bls_df.merge(
    bea_df,
    on=["industry_name", "year"],
    how="inner"
)

print("\nCombined dataset shape:")
print(combined_df.shape)

print("\nCombined dataset columns:")
print(combined_df.columns.tolist())

print("\nFirst 10 combined rows:")
print(combined_df.head(10).to_string(index=False))


# ---------------------------------------------------------
# GDP GROWTH: 2021 TO 2025
# ---------------------------------------------------------

gdp_2021 = combined_df[combined_df["year"] == 2021][
    [
        "industry_code",
        "industry_name",
        "gdp_millions"
    ]
].copy()

gdp_2025 = combined_df[combined_df["year"] == 2025][
    [
        "industry_code",
        "gdp_millions"
    ]
].copy()


gdp_2021 = gdp_2021.rename(
    columns={
        "gdp_millions": "gdp_2021"
    }
)

gdp_2025 = gdp_2025.rename(
    columns={
        "gdp_millions": "gdp_2025"
    }
)


gdp_growth_df = gdp_2021.merge(
    gdp_2025,
    on="industry_code"
)


gdp_growth_df["gdp_growth_pct_2021_2025"] = (
    (
        gdp_growth_df["gdp_2025"]
        - gdp_growth_df["gdp_2021"]
    )
    / gdp_growth_df["gdp_2021"]
) * 100


gdp_growth_df = gdp_growth_df.sort_values(
    "gdp_growth_pct_2021_2025",
    ascending=False
)


print("\n2021-2025 Industry GDP Growth:")

print(
    gdp_growth_df[
        [
            "industry_name",
            "gdp_2021",
            "gdp_2025",
            "gdp_growth_pct_2021_2025"
        ]
    ].to_string(index=False)
)


# ---------------------------------------------------------
# EMPLOYMENT GROWTH: 2021 TO 2025
# ---------------------------------------------------------

employment_2021 = combined_df[
    combined_df["year"] == 2021
][
    [
        "industry_code",
        "avg_quarterly_employment"
    ]
].copy()


employment_2025 = combined_df[
    combined_df["year"] == 2025
][
    [
        "industry_code",
        "industry_name",
        "avg_quarterly_employment",
        "avg_wkly_wage",
        "lq_month3_emplvl"
    ]
].copy()


employment_2021 = employment_2021.rename(
    columns={
        "avg_quarterly_employment": "employment_2021"
    }
)


employment_2025 = employment_2025.rename(
    columns={
        "avg_quarterly_employment": "employment_2025",
        "avg_wkly_wage": "wage_2025",
        "lq_month3_emplvl": "lq_2025"
    }
)


full_competitiveness_df = employment_2025.merge(
    employment_2021,
    on="industry_code"
)


full_competitiveness_df[
    "employment_growth_pct_2021_2025"
] = (
    (
        full_competitiveness_df["employment_2025"]
        - full_competitiveness_df["employment_2021"]
    )
    / full_competitiveness_df["employment_2021"]
) * 100


# ---------------------------------------------------------
# WAGE GROWTH: 2021 TO 2025
# ---------------------------------------------------------

wage_2021 = combined_df[
    combined_df["year"] == 2021
][
    [
        "industry_code",
        "avg_wkly_wage"
    ]
].copy()


wage_2021 = wage_2021.rename(
    columns={
        "avg_wkly_wage": "wage_2021"
    }
)


full_competitiveness_df = full_competitiveness_df.merge(
    wage_2021,
    on="industry_code"
)


full_competitiveness_df[
    "wage_growth_pct_2021_2025"
] = (
    (
        full_competitiveness_df["wage_2025"]
        - full_competitiveness_df["wage_2021"]
    )
    / full_competitiveness_df["wage_2021"]
) * 100


# ---------------------------------------------------------
# ADD GDP GROWTH TO FINAL TABLE
# ---------------------------------------------------------

full_competitiveness_df = full_competitiveness_df.merge(
    gdp_growth_df[
        [
            "industry_code",
            "gdp_2021",
            "gdp_2025",
            "gdp_growth_pct_2021_2025"
        ]
    ],
    on="industry_code"
)


# Final column order
full_competitiveness_df = full_competitiveness_df[
    [
        "industry_code",
        "industry_name",
        "employment_2021",
        "employment_2025",
        "employment_growth_pct_2021_2025",
        "wage_2021",
        "wage_2025",
        "wage_growth_pct_2021_2025",
        "gdp_2021",
        "gdp_2025",
        "gdp_growth_pct_2021_2025",
        "lq_2025"
    ]
]


print("\nFull Kansas Industry Competitiveness Table:")

print(
    full_competitiveness_df
    .sort_values(
        "employment_growth_pct_2021_2025",
        ascending=False
    )
    .to_string(index=False)
)


# ---------------------------------------------------------
# FINAL STRATEGIC INDUSTRY GROUPS
# ---------------------------------------------------------

def classify_industry(row):

    employment_growth = row[
        "employment_growth_pct_2021_2025"
    ]

    gdp_growth = row[
        "gdp_growth_pct_2021_2025"
    ]

    lq = row["lq_2025"]


    if employment_growth > 0 and gdp_growth > 0 and lq > 1:
        return "Growing and Specialized"

    elif employment_growth > 0 and gdp_growth > 0 and lq <= 1:
        return "Growing but Less Specialized"

    elif employment_growth > 0 and gdp_growth <= 0:
        return "Employment Growth but GDP Decline"

    elif employment_growth <= 0 and gdp_growth > 0 and lq > 1:
        return "Specialized with Employment Decline"

    elif employment_growth <= 0 and gdp_growth > 0:
        return "GDP Growth but Employment Decline"

    else:
        return "Declining Employment and GDP"


full_competitiveness_df["strategic_group"] = (
    full_competitiveness_df.apply(
        classify_industry,
        axis=1
    )
)


print("\nFinal Strategic Industry Groups:")

print(
    full_competitiveness_df[
        [
            "industry_name",
            "employment_growth_pct_2021_2025",
            "wage_growth_pct_2021_2025",
            "gdp_growth_pct_2021_2025",
            "lq_2025",
            "strategic_group"
        ]
    ]
    .sort_values(
        [
            "strategic_group",
            "employment_growth_pct_2021_2025"
        ],
        ascending=[True, False]
    )
    .to_string(index=False)
)


# ---------------------------------------------------------
# SAVE FINAL INTEGRATED DATASET
# ---------------------------------------------------------

FINAL_OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "kansas_industry_full_competitiveness_2021_2025.csv"
)


full_competitiveness_df.to_csv(
    FINAL_OUTPUT_FILE,
    index=False
)


print("\nFinal integrated competitiveness dataset saved:")
print(FINAL_OUTPUT_FILE)

print("\nFinal dataset shape:")
print(full_competitiveness_df.shape)

