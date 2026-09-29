import pandas as pd
import requests
from pathlib import Path

# Project folders
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

print("Project folder:", PROJECT_ROOT)
print("Raw data folder:", RAW_DATA_DIR)

# BLS Quarterly Census of Employment and Wages (QCEW) data source
BLS_BASE_URL = "https://data.bls.gov/cew/data/api"

# Analysis settings
YEAR = 2025
QUARTER = 1

# Kansas state-level QCEW area code
KANSAS_AREA_CODE = "20000"

# Build the download URL
url = f"{BLS_BASE_URL}/{YEAR}/{QUARTER}/area/{KANSAS_AREA_CODE}.csv"

print("BLS download URL:")
print(url)

# Download the BLS data
response = requests.get(url)

print("Status code:", response.status_code)

# Save the downloaded file
output_file = RAW_DATA_DIR / f"kansas_qcew_{YEAR}_q{QUARTER}.csv"

with open(output_file, "wb") as file:
    file.write(response.content)

print("Saved file:", output_file)

# Load the downloaded CSV into pandas
df = pd.read_csv(output_file)

print("\nFirst 5 rows:")
print(df.head())

print("\nColumns:")
print(df.columns.tolist())

print("\nNumber of rows:", len(df))

# Inspect industry and ownership codes
print("\nIndustry codes:")
print(df["industry_code"].head(30).to_string(index=False))

print("\nOwnership codes:")
print(df["own_code"].value_counts().sort_index())

print("\nAggregation level codes:")
print(df["agglvl_code"].value_counts().sort_index())

# Keep private-sector, statewide, 2-digit NAICS industries
sector_df = df[
    (df["own_code"] == 5) &
    (df["agglvl_code"] == 54)
].copy()

print("\nPrivate-sector Kansas industries:")
print(
    sector_df[
        [
            "industry_code",
            "month1_emplvl",
            "month2_emplvl",
            "month3_emplvl",
            "avg_wkly_wage",
            "lq_month3_emplvl"
        ]
    ].to_string(index=False)
)

print("\nNumber of sector records:", len(sector_df))

# Add readable industry names
industry_names = {
    "11": "Agriculture, Forestry, Fishing and Hunting",
    "21": "Mining, Quarrying, and Oil and Gas Extraction",
    "22": "Utilities",
    "23": "Construction",
    "31-33": "Manufacturing",
    "42": "Wholesale Trade",
    "44-45": "Retail Trade",
    "48-49": "Transportation and Warehousing",
    "51": "Information",
    "52": "Finance and Insurance",
    "53": "Real Estate and Rental and Leasing",
    "54": "Professional, Scientific, and Technical Services",
    "55": "Management of Companies and Enterprises",
    "56": "Administrative and Support and Waste Management",
    "61": "Educational Services",
    "62": "Health Care and Social Assistance",
    "71": "Arts, Entertainment, and Recreation",
    "72": "Accommodation and Food Services",
    "81": "Other Services"
}

sector_df["industry_name"] = sector_df["industry_code"].map(industry_names)

print("\nIndustry names:")
print(
    sector_df[
        ["industry_code", "industry_name"]
    ].to_string(index=False)
)


# Calculate average employment for the quarter
sector_df["avg_quarterly_employment"] = sector_df[
    ["month1_emplvl", "month2_emplvl", "month3_emplvl"]
].mean(axis=1)

print("\nQuarterly average employment:")
print(
    sector_df[
        ["industry_name", "avg_quarterly_employment"]
    ]
    .sort_values("avg_quarterly_employment", ascending=False)
    .to_string(index=False)
)

# Select important columns for analysis
clean_df = sector_df[
    [
        "industry_code",
        "industry_name",
        "year",
        "qtr",
        "avg_quarterly_employment",
        "avg_wkly_wage",
        "lq_month3_emplvl",
        "oty_month3_emplvl_pct_chg",
        "oty_avg_wkly_wage_pct_chg"
    ]
].copy()

# Save cleaned data
processed_file = PROJECT_ROOT / "data" / "processed" / "kansas_industry_q1_2025.csv"

clean_df.to_csv(processed_file, index=False)

print("\nProcessed dataset saved:")
print(processed_file)

