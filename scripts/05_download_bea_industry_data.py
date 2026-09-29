import os
import pandas as pd
import requests
from pathlib import Path
from dotenv import load_dotenv


# Project folders
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


# Load the BEA API key from the .env file
load_dotenv(PROJECT_ROOT / ".env", override=True)

BEA_API_KEY = os.getenv("BEA_API_KEY")

if BEA_API_KEY:
    BEA_API_KEY = BEA_API_KEY.strip()

print("API key length:", len(BEA_API_KEY) if BEA_API_KEY else 0)

if not BEA_API_KEY:
    raise ValueError("BEA_API_KEY was not found in the .env file.")

print("BEA API key loaded successfully.")


# BEA API base URL
BEA_API_URL = "https://apps.bea.gov/api/data"


# Kansas state GeoFIPS
KANSAS_GEOFIPS = "20000"


# Years for comparison
YEARS = "2021,2022,2023,2024,2025"


print("BEA script setup complete.")
print("Kansas GeoFIPS:", KANSAS_GEOFIPS)
print("Years:", YEARS)


# Request Kansas annual GDP by industry
params = {
    "UserID": BEA_API_KEY,
    "method": "GetData",
    "datasetname": "Regional",
    "TableName": "SAGDP2",
    "LineCode": "ALL",
    "GeoFips": KANSAS_GEOFIPS,
    "Year": YEARS,
    "ResultFormat": "JSON"
}

response = requests.get(
    BEA_API_URL,
    params=params,
    timeout=30
)

print("\nBEA status code:")
print(response.status_code)

response.raise_for_status()

data = response.json()

print("\nBEA GDP data received successfully.")

print("\nBEA Results keys:")
print(data["BEAAPI"]["Results"].keys())


# Inspect BEA GDP rows
bea_rows = data["BEAAPI"]["Results"]["Data"]

print("\nNumber of BEA GDP rows:")
print(len(bea_rows))

print("\nFirst 10 BEA GDP rows:")
for row in bea_rows[:10]:
    print(row)

    # Convert BEA rows into a pandas DataFrame
bea_df = pd.DataFrame(bea_rows)

# Clean extra spaces from industry descriptions
bea_df["Description"] = bea_df["Description"].str.strip()

# Convert GDP values to numeric
bea_df["DataValue"] = pd.to_numeric(
    bea_df["DataValue"],
    errors="coerce"
)

print("\nBEA dataset shape:")
print(bea_df.shape)

print("\nUnique industry descriptions:")
print(
    bea_df[
        ["Code", "Description"]
    ]
    .drop_duplicates()
    .to_string(index=False)
)

# BEA line codes that match our 19 BLS industry sectors
bea_industry_codes = {
    "SAGDP2-3": "Agriculture, Forestry, Fishing and Hunting",
    "SAGDP2-6": "Mining, Quarrying, and Oil and Gas Extraction",
    "SAGDP2-10": "Utilities",
    "SAGDP2-11": "Construction",
    "SAGDP2-12": "Manufacturing",
    "SAGDP2-34": "Wholesale Trade",
    "SAGDP2-35": "Retail Trade",
    "SAGDP2-36": "Transportation and Warehousing",
    "SAGDP2-45": "Information",
    "SAGDP2-51": "Finance and Insurance",
    "SAGDP2-56": "Real Estate and Rental and Leasing",
    "SAGDP2-60": "Professional, Scientific, and Technical Services",
    "SAGDP2-64": "Management of Companies and Enterprises",
    "SAGDP2-65": "Administrative and Support and Waste Management",
    "SAGDP2-69": "Educational Services",
    "SAGDP2-70": "Health Care and Social Assistance",
    "SAGDP2-76": "Arts, Entertainment, and Recreation",
    "SAGDP2-79": "Accommodation and Food Services",
    "SAGDP2-82": "Other Services"
}

# Keep only the 19 comparable industries
bea_sector_df = bea_df[
    bea_df["Code"].isin(bea_industry_codes.keys())
].copy()

# Add standardized industry names matching the BLS dataset
bea_sector_df["industry_name"] = (
    bea_sector_df["Code"].map(bea_industry_codes)
)

# Rename important columns
bea_sector_df = bea_sector_df.rename(
    columns={
        "TimePeriod": "year",
        "DataValue": "gdp_millions"
    }
)

# Convert year to numeric
bea_sector_df["year"] = pd.to_numeric(
    bea_sector_df["year"],
    errors="coerce"
)

print("\nFiltered BEA industry dataset:")
print(
    bea_sector_df[
        [
            "Code",
            "industry_name",
            "year",
            "gdp_millions"
        ]
    ].head(25).to_string(index=False)
)

print("\nNumber of filtered BEA rows:")
print(len(bea_sector_df))

print("\nRows by year:")
print(
    bea_sector_df["year"]
    .value_counts()
    .sort_index()
)

# Select final BEA columns
bea_clean_df = bea_sector_df[
    [
        "industry_name",
        "year",
        "gdp_millions"
    ]
].copy()

# Save cleaned BEA GDP data
bea_output_file = (
    PROCESSED_DATA_DIR
    / "kansas_industry_gdp_2021_2025.csv"
)

bea_clean_df.to_csv(
    bea_output_file,
    index=False
)

print("\nClean BEA GDP dataset saved:")
print(bea_output_file)

print("\nDataset shape:")
print(bea_clean_df.shape)



