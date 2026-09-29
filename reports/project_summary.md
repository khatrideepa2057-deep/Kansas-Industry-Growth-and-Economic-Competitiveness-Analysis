# Kansas Industry Growth and Economic Competitiveness Analysis

## Project Goal

This project analyzes which Kansas industries are growing, declining, becoming more concentrated, and showing signs of economic competitiveness.

The analysis combines employment, wages, industry concentration, GDP growth, national benchmarking, and shift-share analysis.

## Data Sources

- U.S. Bureau of Labor Statistics (BLS) Quarterly Census of Employment and Wages (QCEW)
- U.S. Bureau of Economic Analysis (BEA) Regional GDP by Industry

## Analysis Period

2021–2025

## Key Measures

- Employment growth
- Average weekly wages
- Wage growth
- Location Quotient
- Nominal GDP growth
- U.S. industry benchmark growth
- Shift-share national growth effect
- Shift-share industry mix effect
- Shift-share competitive effect

## Key Findings

### Growing and Specialized Industries

Several Kansas industries showed both employment growth and an employment concentration above the national average.

- Manufacturing
- Transportation and Warehousing
- Wholesale Trade
- Agriculture, Forestry, Fishing and Hunting

Manufacturing was especially notable, with approximately 9.8% employment growth from 2021 to 2025, 37.2% nominal GDP growth, and a 2025 Location Quotient of 1.50.

### Employment Growth

The fastest employment growth occurred in:

- Arts, Entertainment, and Recreation
- Other Services
- Construction
- Accommodation and Food Services
- Professional, Scientific, and Technical Services

### Industry GDP

Arts, Entertainment, and Recreation showed the highest nominal GDP growth among the analyzed industries.

Professional, Scientific, and Technical Services, Construction, and Manufacturing also experienced substantial nominal GDP growth.

Because BEA SAGDP2 uses current dollars, these GDP growth rates are nominal and are not adjusted for inflation.

### Industry Concentration

Manufacturing had the highest 2025 Location Quotient at 1.50.

Other industries with above-average Kansas concentration included:

- Agriculture, Forestry, Fishing and Hunting
- Mining, Quarrying, and Oil and Gas Extraction
- Utilities
- Transportation and Warehousing
- Wholesale Trade

### Shift-Share Findings

Shift-share analysis was used to separate Kansas employment change into:

1. National Growth Effect
2. Industry Mix Effect
3. Competitive Effect

Manufacturing showed the strongest positive competitive effect, at approximately 9,665 jobs.

Construction and Agriculture also showed positive competitive effects.

Several industries grew in Kansas but still underperformed their national industry benchmarks, including Health Care and Social Assistance and Accommodation and Food Services.

## Tools Used

- Python
- pandas
- requests
- matplotlib
- BLS QCEW API
- BEA Regional API
- VS Code

## Project Outputs

The project produced:

- Cleaned BLS employment and wage datasets
- Multi-year Kansas industry dataset
- BEA GDP-by-industry dataset
- Integrated BLS + BEA competitiveness dataset
- U.S. benchmark dataset
- Shift-share dataset
- Employment growth visualizations
- GDP growth visualizations
- Location Quotient competitiveness chart
- Employment vs. GDP growth chart
- Shift-share competitive-effect chart

