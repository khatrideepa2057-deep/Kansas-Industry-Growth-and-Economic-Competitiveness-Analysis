import pandas as pd
import requests
from pathlib import Path

# Project folders
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

# BLS QCEW API
BLS_BASE_URL = "https://data.bls.gov/cew/data/api"

# Kansas state-level area code
KANSAS_AREA_CODE = "20000"

# We will compare the same quarter across multiple years
YEARS = [2021, 2022, 2023, 2024, 2025]
QUARTER = 1

print("Years to download:", YEARS)
print("Quarter:", QUARTER)

# Download Q1 Kansas data for each year
for year in YEARS:
    url = f"{BLS_BASE_URL}/{year}/{QUARTER}/area/{KANSAS_AREA_CODE}.csv"

    print(f"\nDownloading {year} Q{QUARTER}...")
    print("URL:", url)

    response = requests.get(url)

    print("Status code:", response.status_code)

    output_file = RAW_DATA_DIR / f"kansas_qcew_{year}_q{QUARTER}.csv"

    with open(output_file, "wb") as file:
        file.write(response.content)

    print("Saved:", output_file)

    # Combine all years into one dataset
all_years = []

for year in YEARS:
    file_path = RAW_DATA_DIR / f"kansas_qcew_{year}_q{QUARTER}.csv"

    yearly_df = pd.read_csv(file_path)

    # Keep private-sector, statewide, 2-digit NAICS industries
    yearly_df = yearly_df[
        (yearly_df["own_code"] == 5) &
        (yearly_df["agglvl_code"] == 54)
    ].copy()

    # Calculate average quarterly employment
    yearly_df["avg_quarterly_employment"] = yearly_df[
        ["month1_emplvl", "month2_emplvl", "month3_emplvl"]
    ].mean(axis=1)

    all_years.append(yearly_df)

# Stack all years together
multiyear_df = pd.concat(all_years, ignore_index=True)

print("\nCombined dataset created.")
print("Number of rows:", len(multiyear_df))

print("\nRows by year:")
print(multiyear_df["year"].value_counts().sort_index())

# Check industry codes for each year
for year in YEARS:
    print(f"\nIndustry codes for {year}:")

    codes = (
        multiyear_df[
            multiyear_df["year"] == year
        ]["industry_code"]
        .astype(str)
        .tolist()
    )

    print(codes)
    print("Number of industries:", len(codes))

    # Remove unclassified establishments
multiyear_df = multiyear_df[
    multiyear_df["industry_code"].astype(str) != "99"
].copy()

print("\nAfter removing industry code 99:")
print("Number of rows:", len(multiyear_df))

print("\nRows by year:")
print(multiyear_df["year"].value_counts().sort_index())

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

multiyear_df["industry_code"] = multiyear_df["industry_code"].astype(str)

multiyear_df["industry_name"] = multiyear_df["industry_code"].map(industry_names)

print("\nCheck industry names:")
print(
    multiyear_df[
        ["year", "industry_code", "industry_name"]
    ].head(25).to_string(index=False)
)


# Select columns for the historical analysis
historical_df = multiyear_df[
    [
        "industry_code",
        "industry_name",
        "year",
        "qtr",
        "avg_quarterly_employment",
        "avg_wkly_wage",
        "lq_month3_emplvl"
    ]
].copy()

# Save cleaned multi-year dataset
historical_file = (
    PROCESSED_DATA_DIR
    / "kansas_industry_multiyear_2021_2025.csv"
)

historical_df.to_csv(historical_file, index=False)

print("\nHistorical dataset saved:")
print(historical_file)

print("\nHistorical dataset shape:")
print(historical_df.shape)

