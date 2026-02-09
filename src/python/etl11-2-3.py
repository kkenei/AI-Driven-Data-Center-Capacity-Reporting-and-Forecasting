"""
etl.py
------
Monthly-only ETL pipeline for Colocation Capacity Reporting.

This script:
1. Loads Monthly_Raw and Monthly_Validated sheets from the raw Excel file.
2. Enriches them with calculated metrics (utilization %, IT load %, PUE, contracted load, energy consumption, carbon emissions, etc.).
3. Merges design constants from constants.py for each data center.
4. Exports the enriched validated dataset to CSV for Power BI dashboards.

Author: Kenneth @ TippleK Data Centres
"""

import os
import pandas as pd
import calendar
from constants import DATA_CENTERS   # import design metadata (rack density, design capacity, carbon factor, etc.)

# --- Project Paths ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
RAW_FILE = os.path.join(PROJECT_ROOT, "data/raw/Colocation_Capacity_Data.xlsx")
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "data/enriched/enriched_monthly.csv")

# --- Enrichment Function ---
def enrich(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enrich a monthly dataframe with calculated metrics and design comparisons.
    Business context: aligns raw operational data with design constants
    and produces KPIs for executive dashboards.
    """

    # --- Operational KPIs ---
    # Rack Utilization % = (Reserved + Decommissioned racks) ÷ Total contracted racks
    df["Rack_Utilization_%"] = (
        (df["Reserved_Racks"] + df["Decommissioned_Racks"])
        / df["Total_Contracted_Racks"] * 100
    )

    # IT Load % = Average IT load ÷ Average total load
    df["IT_Load_%"] = df["Avg_IT_Load_kW"] / df["Avg_Total_Load_kW"] * 100

    # Remaining Capacity (racks) = Total contracted racks – (Reserved + Decommissioned)
    df["Remaining_Capacity"] = (
        df["Total_Contracted_Racks"] - (df["Reserved_Racks"] + df["Decommissioned_Racks"])
    )

    # PUE (Power Usage Effectiveness) = Average total load ÷ Average IT load
    df["PUE"] = df["Avg_Total_Load_kW"] / df["Avg_IT_Load_kW"]

    # --- Merge design constants from constants.py ---
    # These values anchor operational metrics against design capacity
    df["Design_Total_Racks"] = df["Data_Center_Name"].map(lambda dc: DATA_CENTERS[dc]["Design_Total_Racks"])
    df["Design_Total_Footprint_m2"] = df["Data_Center_Name"].map(lambda dc: DATA_CENTERS[dc]["Design_Total_Footprint_m2"])
    df["Design_IT_Capacity_kW"] = df["Data_Center_Name"].map(lambda dc: DATA_CENTERS[dc]["Design_IT_Capacity_kW"])
    df["Design_Total_Load_kW"] = df["Data_Center_Name"].map(lambda dc: DATA_CENTERS[dc]["Design_Total_Load_kW"])
    df["PUE_Target"] = df["Data_Center_Name"].map(lambda dc: DATA_CENTERS[dc]["PUE_Target"])
    df["Rack_Density_kW"] = df["Data_Center_Name"].map(lambda dc: DATA_CENTERS[dc]["Rack_Density_kW"])
    df["Rack_Footprint_m2"] = df["Data_Center_Name"].map(lambda dc: DATA_CENTERS[dc]["Rack_Footprint_m2"])
    df["Carbon_Factor_tCO2_per_kWh"] = df["Data_Center_Name"].map(lambda dc: DATA_CENTERS[dc]["Carbon_Factor_tCO2_per_kWh"])

    # --- Derived design denominators ---
    # Gross white space (executive denominator)
    df["Design_Space_m2"] = df["Data_Center_Name"].map(lambda dc: DATA_CENTERS[dc]["Gross_White_Space_m2"])

    # Rack footprint space (technical denominator)
    df["Design_Space_Racks"] = df["Design_Total_Racks"] * df["Rack_Footprint_m2"]

    # --- Derived metrics ---
    # Contracted load = racks sold × rack density
    df["Contracted_Load_kW"] = df["Total_Contracted_Racks"] * df["Rack_Density_kW"]

    # Contracted space = racks sold × rack footprint
    df["Contracted_Space_m2"] = df["Total_Contracted_Racks"] * df["Rack_Footprint_m2"]

    # Remaining load = design IT capacity – contracted load
    df["Remaining_Load_kW"] = df["Design_IT_Capacity_kW"] - df["Contracted_Load_kW"]

    # Remaining space = design rack footprint – contracted space
    df["Remaining_Space_m2"] = df["Design_Space_Racks"] - df["Contracted_Space_m2"]

    # Remaining racks = design racks – contracted racks
    df["Remaining_Racks"] = df["Design_Total_Racks"] - df["Total_Contracted_Racks"]

    # Facility Power (kW) = Avg Total Load (kW)
    df["Facility_Power_kW"] = df["Avg_Total_Load_kW"]

    # Cooling Load (kW) = Facility Power – IT Load
    df["Cooling_Load_kW"] = df["Facility_Power_kW"] - df["Avg_IT_Load_kW"]

    # --- Energy & Carbon ---
    # Hours in month based on Reporting_Date
    df["Hours_in_Month"] = df["Reporting_Date"].apply(lambda d: calendar.monthrange(d.year, d.month)[1] * 24)

    # Energy Consumption (kWh) = Facility Power × Hours in Month
    df["Energy_Consumption_kWh"] = df["Facility_Power_kW"] * df["Hours_in_Month"]

    # Carbon Emissions (tCO2) = Energy Consumption × Carbon Factor
    df["Carbon_Emissions_tCO2"] = df["Energy_Consumption_kWh"] * df["Carbon_Factor_tCO2_per_kWh"]

    # --- Ratios & Comparisons ---
    df["Rack_Utilization_vs_Design_%"] = df["Total_Contracted_Racks"] / df["Design_Total_Racks"] * 100
    df["IT_Load_vs_Design_%"] = df["Avg_IT_Load_kW"] / df["Design_IT_Capacity_kW"] * 100
    df["Total_Load_vs_Design_%"] = df["Avg_Total_Load_kW"] / df["Design_Total_Load_kW"] * 100
    df["PUE_vs_Target"] = df["PUE"] / df["PUE_Target"]
    df["Fill_Ratio_%"] = df["Contracted_Load_kW"] / df["Design_IT_Capacity_kW"] * 100

    # Remaining vs design space (gross white space)
    df["Remaining_vs_Design_%"] = df["Remaining_Space_m2"] / df["Design_Space_m2"] * 100

    # Remaining vs design rack footprint space
    df["Remaining_vs_Design_Racks_%"] = df["Remaining_Space_m2"] / df["Design_Space_Racks"] * 100

    return df

# --- Main ETL Process ---
def main():
    print("Starting ETL pipeline...")

    # 1. Load Monthly Sheets from Excel
    print("Loading raw Excel file...")
    df_raw = pd.read_excel(RAW_FILE, sheet_name="Monthly_Raw")
    df_validated = pd.read_excel(RAW_FILE, sheet_name="Monthly_Validated")

    # 2. Apply enrichment to both sheets
    print("Enriching Monthly_Raw...")
    df_raw_enriched = enrich(df_raw)

    print("Enriching Monthly_Validated...")
    df_validated_enriched = enrich(df_validated)

    # 3. Export enriched validated dataset to CSV
    print(f"Exporting enriched dataset to {OUTPUT_FILE}...")
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df_validated_enriched.to_csv(OUTPUT_FILE, index=False)

    print("ETL pipeline complete ✅")

# --- Entry Point ---
if __name__ == "__main__":
    main()
