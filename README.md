# Colocation Capacity Intelligence

Data-driven capacity reporting & forecasting for colocation data centers.

## Current stack
- Source data: Excel
- Processing & forecasting: Python (pandas + prophet)
- Visualization: Power BI (.pbip format)
- Version control: Git

## Quick start (on this server)
1. Activate virtual environment:   `source .venv/bin/activate`
2. Install dependencies:           `pip install -r src/python/requirements.txt`
3. Run ETL:                        `python src/python/01_etl_clean.py`

## Folder structure
- data/raw/          → original Excel files (not committed)
- data/processed/    → cleaned CSVs & forecasts
- src/python/        → ETL & forecasting scripts
- src/powerbi/       → Power BI project files (.pbip)

## Latest Progress (February 2, 2026)

✅ **ETL Pipeline**
- Stabilized enrichment logic:
  - Corrected Facility Power mapping to `Avg_Total_Load_kW`.
  - Fixed enrichment order (define Facility Power before Cooling Load).
- Added mapping for `Design_Total_Racks` and `Design_Total_Footprint_m2`.
- Derived denominators:
  - `Design_Space_m2` from `Gross_White_Space_m2`.
  - `Design_Space_Racks` from `Design_Total_Racks × Rack_Footprint_m2`.
- Pipeline now consistently produces `enriched_monthly.csv` with design constants and KPIs.

✅ **KPI Dictionary**
- Documented in `docs/KPI_Dictionary.md`.
- Structured into Capacity, Space/Load, Efficiency, and Forecast/Anomalies groups.
- Standardized naming conventions (Installed, Used, Available, Utilization).
- Extended to include new denominators for executive vs technical views.

✅ **Power BI Model**
- Designed star schema for clean drill‑downs:
  - Fact tables: `enriched_monthly`, `forecast`, `forecast_quality`, `forecast_anomalies`.
  - Dimension tables: `Calendar`, `Data_Center_Metadata`.
- Relationships established via `Date` and `Data_Center_Name`.
- Supports drill‑down from portfolio → country → site → rack.

✅ **Executive Readiness**
- Progress Report updated in `docs/Progress_Report.md` for stakeholder visibility.
- KPI dictionary aligned with Global Adoption Playbook.
- ETL + Power BI integration now demo‑ready for executive presentation.
