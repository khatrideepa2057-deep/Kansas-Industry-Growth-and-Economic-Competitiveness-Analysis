import pandas as pd
from pathlib import Path


# Project folders
PROJECT_ROOT = Path(__file__).resolve().parents[1]

KANSAS_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "kansas_industry_full_competitiveness_2021_2025.csv"
)

US_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "us_industry_employment_growth_2021_2025.csv"
)


# Load data
ks_df = pd.read_csv(KANSAS_FILE)
us_df = pd.read_csv(US_FILE)


print("Kansas dataset shape:")
print(ks_df.shape)

print("\nU.S. benchmark dataset shape:")
print(us_df.shape)


# ---------------------------------------------------------
# CALCULATE OVERALL U.S. EMPLOYMENT GROWTH RATE
# ---------------------------------------------------------

us_total_2021 = us_df["us_employment_2021"].sum()
us_total_2025 = us_df["us_employment_2025"].sum()

us_overall_growth_rate = (
    (us_total_2025 - us_total_2021)
    / us_total_2021
)

print("\nOverall U.S. employment growth rate:")
print(us_overall_growth_rate * 100)


# ---------------------------------------------------------
# MERGE KANSAS AND U.S. INDUSTRY DATA
# ---------------------------------------------------------

shift_share_df = ks_df.merge(
    us_df[
        [
            "industry_code",
            "us_employment_2021",
            "us_employment_2025",
            "us_growth_pct_2021_2025"
        ]
    ],
    on="industry_code",
    how="inner"
)


# Convert U.S. industry growth percentage to decimal
shift_share_df["us_industry_growth_rate"] = (
    shift_share_df["us_growth_pct_2021_2025"] / 100
)


# Kansas actual employment change
shift_share_df["actual_ks_change"] = (
    shift_share_df["employment_2025"]
    - shift_share_df["employment_2021"]
)


# ---------------------------------------------------------
# NATIONAL GROWTH EFFECT
# ---------------------------------------------------------

shift_share_df["national_growth_effect"] = (
    shift_share_df["employment_2021"]
    * us_overall_growth_rate
)


# ---------------------------------------------------------
# INDUSTRY MIX EFFECT
# ---------------------------------------------------------

shift_share_df["industry_mix_effect"] = (
    shift_share_df["employment_2021"]
    * (
        shift_share_df["us_industry_growth_rate"]
        - us_overall_growth_rate
    )
)


# ---------------------------------------------------------
# COMPETITIVE EFFECT
# ---------------------------------------------------------

ks_industry_growth_rate = (
    (
        shift_share_df["employment_2025"]
        - shift_share_df["employment_2021"]
    )
    / shift_share_df["employment_2021"]
)

shift_share_df["competitive_effect"] = (
    shift_share_df["employment_2021"]
    * (
        ks_industry_growth_rate
        - shift_share_df["us_industry_growth_rate"]
    )
)


# ---------------------------------------------------------
# CHECK THE SHIFT-SHARE IDENTITY
# ---------------------------------------------------------

shift_share_df["explained_change"] = (
    shift_share_df["national_growth_effect"]
    + shift_share_df["industry_mix_effect"]
    + shift_share_df["competitive_effect"]
)


shift_share_df["difference_check"] = (
    shift_share_df["actual_ks_change"]
    - shift_share_df["explained_change"]
)


# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------

result_df = shift_share_df[
    [
        "industry_name",
        "employment_2021",
        "employment_2025",
        "actual_ks_change",
        "national_growth_effect",
        "industry_mix_effect",
        "competitive_effect",
        "difference_check"
    ]
].sort_values(
    "competitive_effect",
    ascending=False
)


print("\nKansas Shift-Share Results:")
print(result_df.to_string(index=False))


# Save shift-share results
SHIFT_SHARE_OUTPUT = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "kansas_shift_share_2021_2025.csv"
)

result_df.to_csv(
    SHIFT_SHARE_OUTPUT,
    index=False
)

print("\nShift-share dataset saved:")
print(SHIFT_SHARE_OUTPUT)

print("\nDataset shape:")
print(result_df.shape)

