import pandas as pd
import requests
from pathlib import Path


# Project folders
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


# BLS QCEW API
BLS_BASE_URL = "https://data.bls.gov/cew/data/api"


# U.S. national area code
US_AREA_CODE = "US000"


# Years and quarter for comparison
YEARS = [2021, 2025]
QUARTER = 1


print("U.S. benchmark setup complete.")
print("Years:", YEARS)
print("Quarter:", QUARTER)

# Download U.S. QCEW data for each benchmark year
for year in YEARS:
    url = f"{BLS_BASE_URL}/{year}/{QUARTER}/area/{US_AREA_CODE}.csv"

    print(f"\nDownloading U.S. data for {year} Q{QUARTER}...")
    print("URL:", url)

    response = requests.get(url)

    print("Status code:", response.status_code)

    output_file = RAW_DATA_DIR / f"us_qcew_{year}_q{QUARTER}.csv"

    with open(output_file, "wb") as file:
        file.write(response.content)

    print("Saved:", output_file)

    # Industry names used in the Kansas analysis
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


# Combine cleaned U.S. benchmark data
us_years = []

for year in YEARS:
    file_path = RAW_DATA_DIR / f"us_qcew_{year}_q{QUARTER}.csv"

    yearly_df = pd.read_csv(file_path)

    # Keep private-sector, national, 2-digit NAICS industries
    yearly_df = yearly_df[
        (yearly_df["own_code"] == 5) &
        (yearly_df["agglvl_code"] == 14)
    ].copy()

    # Standardize industry codes as text
    yearly_df["industry_code"] = yearly_df["industry_code"].astype(str)

    # Keep only the same 19 industries used for Kansas
    yearly_df = yearly_df[
        yearly_df["industry_code"].isin(industry_names.keys())
    ].copy()

    # Add readable names
    yearly_df["industry_name"] = yearly_df["industry_code"].map(
        industry_names
    )

    # Calculate average quarterly employment
    yearly_df["avg_quarterly_employment"] = yearly_df[
        [
            "month1_emplvl",
            "month2_emplvl",
            "month3_emplvl"
        ]
    ].mean(axis=1)

    us_years.append(yearly_df)


us_df = pd.concat(
    us_years,
    ignore_index=True
)


print("\nClean U.S. benchmark dataset:")
print(
    us_df[
        [
            "year",
            "industry_code",
            "industry_name",
            "avg_quarterly_employment"
        ]
    ].to_string(index=False)
)

print("\nRows by year:")
print(
    us_df["year"]
    .value_counts()
    .sort_index()
)

print("\nTotal rows:")
print(len(us_df))

# Get 2021 and 2025 U.S. employment
us_2021 = us_df[us_df["year"] == 2021][
    [
        "industry_code",
        "industry_name",
        "avg_quarterly_employment"
    ]
].copy()

us_2025 = us_df[us_df["year"] == 2025][
    [
        "industry_code",
        "avg_quarterly_employment"
    ]
].copy()


# Rename employment columns
us_2021 = us_2021.rename(
    columns={
        "avg_quarterly_employment": "us_employment_2021"
    }
)

us_2025 = us_2025.rename(
    columns={
        "avg_quarterly_employment": "us_employment_2025"
    }
)


# Merge 2021 and 2025
us_growth_df = us_2021.merge(
    us_2025,
    on="industry_code"
)


# Calculate U.S. employment growth
us_growth_df["us_growth_pct_2021_2025"] = (
    (
        us_growth_df["us_employment_2025"]
        - us_growth_df["us_employment_2021"]
    )
    / us_growth_df["us_employment_2021"]
) * 100


us_growth_df = us_growth_df.sort_values(
    "us_growth_pct_2021_2025",
    ascending=False
)


print("\nU.S. Industry Employment Growth, 2021-2025:")
print(
    us_growth_df[
        [
            "industry_name",
            "us_employment_2021",
            "us_employment_2025",
            "us_growth_pct_2021_2025"
        ]
    ].to_string(index=False)
)

# Save U.S. benchmark growth dataset
us_output_file = (
    PROCESSED_DATA_DIR
    / "us_industry_employment_growth_2021_2025.csv"
)

us_growth_df.to_csv(
    us_output_file,
    index=False
)

print("\nU.S. benchmark dataset saved:")
print(us_output_file)

print("\nDataset shape:")
print(us_growth_df.shape)

# Save U.S. benchmark growth dataset
us_output_file = (
    PROCESSED_DATA_DIR
    / "us_industry_employment_growth_2021_2025.csv"
)

us_growth_df.to_csv(
    us_output_file,
    index=False
)

print("\nU.S. benchmark dataset saved:")
print(us_output_file)

print("\nDataset shape:")
print(us_growth_df.shape)

