"""
etl.py
------
Monthly + Forecast ETL pipeline for Colocation Capacity Reporting.

This script:
1. Loads Monthly_Raw and Monthly_Validated sheets from the raw Excel file.
2. Enriches them with calculated metrics (utilization %, IT load %, PUE, contracted load, energy consumption, carbon emissions, etc.).
3. Merges design constants from constants.py for each data center.
4. Generates extended Prophet forecasts (36 months horizon) for contracted racks.
5. Exports both enriched validated dataset and forecast dataset to CSV for Power BI dashboards.

Author: Kenneth @ TippleK Data Centres
"""

import os
import pandas as pd
import calendar
from constants import DATA_CENTERS   # import design metadata (rack density, design capacity, carbon factor, etc.)
from prophet import Prophet          # forecasting library

# --- Project Paths ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
RAW_FILE = os.path.join(PROJECT_ROOT, "data/raw/Colocation_Capacity_Data.xlsx")
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "data/enriched/enriched_monthly.csv")
FORECAST_FILE = os.path.join(PROJECT_ROOT, "data/forecast/forecast_racks.csv")

# --- Enrichment Function ---
def enrich(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enrich a monthly dataframe with calculated metrics and design comparisons.
    Business context: aligns raw operational data with design constants
    and produces KPIs for executive dashboards.
    """

    # --- Operational KPIs ---
    df["Rack_Utilization_%"] = (
        (df["Reserved_Racks"] + df["Decommissioned_Racks"])
        / df["Total_Contracted_Racks"] * 100
    )
    df["IT_Load_%"] = df["Avg_IT_Load_kW"] / df["Avg_Total_Load_kW"] * 100
    df["Remaining_Capacity"] = (
        df["Total_Contracted_Racks"] - (df["Reserved_Racks"] + df["Decommissioned_Racks"])
    )
    df["PUE"] = df["Avg_Total_Load_kW"] / df["Avg_IT_Load_kW"]

    # --- Merge design constants ---
    df["Design_Total_Racks"] = df["Data_Center_Name"].map(lambda dc: DATA_CENTERS[dc]["Design_Total_Racks"])
    df["Design_Total_Footprint_m2"] = df["Data_Center_Name"].map(lambda dc: DATA_CENTERS[dc]["Design_Total_Footprint_m2"])
    df["Design_IT_Capacity_kW"] = df["Data_Center_Name"].map(lambda dc: DATA_CENTERS[dc]["Design_IT_Capacity_kW"])
    df["Design_Total_Load_kW"] = df["Data_Center_Name"].map(lambda dc: DATA_CENTERS[dc]["Design_Total_Load_kW"])
    df["PUE_Target"] = df["Data_Center_Name"].map(lambda dc: DATA_CENTERS[dc]["PUE_Target"])
    df["Rack_Density_kW"] = df["Data_Center_Name"].map(lambda dc: DATA_CENTERS[dc]["Rack_Density_kW"])
    df["Rack_Footprint_m2"] = df["Data_Center_Name"].map(lambda dc: DATA_CENTERS[dc]["Rack_Footprint_m2"])
    df["Carbon_Factor_tCO2_per_kWh"] = df["Data_Center_Name"].map(lambda dc: DATA_CENTERS[dc]["Carbon_Factor_tCO2_per_kWh"])
    df["Design_Space_m2"] = df["Data_Center_Name"].map(lambda dc: DATA_CENTERS[dc]["Gross_White_Space_m2"])

    # --- Derived denominators ---
    df["Design_Space_Racks"] = df["Design_Total_Racks"] * df["Rack_Footprint_m2"]

    # --- Derived metrics ---
    df["Contracted_Load_kW"] = df["Total_Contracted_Racks"] * df["Rack_Density_kW"]
    df["Contracted_Space_m2"] = df["Total_Contracted_Racks"] * df["Rack_Footprint_m2"]
    df["Remaining_Load_kW"] = df["Design_IT_Capacity_kW"] - df["Contracted_Load_kW"]
    df["Remaining_Space_m2"] = df["Design_Space_Racks"] - df["Contracted_Space_m2"]
    df["Remaining_Racks"] = df["Design_Total_Racks"] - df["Total_Contracted_Racks"]

    df["Facility_Power_kW"] = df["Avg_Total_Load_kW"]
    df["Cooling_Load_kW"] = df["Facility_Power_kW"] - df["Avg_IT_Load_kW"]

    # --- Energy & Carbon ---
    df["Hours_in_Month"] = df["Reporting_Date"].apply(lambda d: calendar.monthrange(d.year, d.month)[1] * 24)
    df["Energy_Consumption_kWh"] = df["Facility_Power_kW"] * df["Hours_in_Month"]
    df["Carbon_Emissions_tCO2"] = df["Energy_Consumption_kWh"] * df["Carbon_Factor_tCO2_per_kWh"]

    # --- Ratios & Comparisons ---
    df["Rack_Utilization_vs_Design_%"] = df["Total_Contracted_Racks"] / df["Design_Total_Racks"] * 100
    df["IT_Load_vs_Design_%"] = df["Avg_IT_Load_kW"] / df["Design_IT_Capacity_kW"] * 100
    df["Total_Load_vs_Design_%"] = df["Avg_Total_Load_kW"] / df["Design_Total_Load_kW"] * 100
    df["PUE_vs_Target"] = df["PUE"] / df["PUE_Target"]
    df["Fill_Ratio_%"] = df["Contracted_Load_kW"] / df["Design_IT_Capacity_kW"] * 100
    df["Remaining_vs_Design_%"] = df["Remaining_Space_m2"] / df["Design_Space_m2"] * 100
    df["Remaining_vs_Design_Racks_%"] = df["Remaining_Space_m2"] / df["Design_Space_Racks"] * 100

    return df

# --- Forecast Function ---
def forecast_racks(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a 36-month forecast of Total_Contracted_Racks using Prophet.
    Produces baseline, lower, and upper confidence intervals.
    """

    forecasts = []
    for dc in df["Data_Center_Name"].unique():
        dc_df = df[df["Data_Center_Name"] == dc][["Reporting_Date", "Total_Contracted_Racks"]].rename(
            columns={"Reporting_Date": "ds", "Total_Contracted_Racks": "y"}
        )

        # Fit Prophet model
        model = Prophet()
        model.fit(dc_df)

        # Extend horizon to 36 months
        future = model.make_future_dataframe(periods=120, freq="ME")
        forecast = model.predict(future)

        # Add metadata
        forecast["Metric"] = "Total_Contracted_Racks"
        forecast["Horizon"] = "36m"
        forecast["Data_Center_Name"] = dc

        forecasts.append(forecast[["ds", "yhat", "yhat_lower", "yhat_upper", "Metric", "Horizon", "Data_Center_Name"]])

    return pd.concat(forecasts, ignore_index=True)

# --- Main ETL Process ---
def main():
    print("Starting ETL pipeline...")

    # 1. Load Monthly Sheets from Excel
    print("Loading raw Excel file...")
    df_raw = pd.read_excel(RAW_FILE, sheet_name="Monthly_Raw")
    df_validated = pd.read_excel(RAW_FILE, sheet_name="Monthly_Validated")

    # 2. Apply enrichment
    print("Enriching Monthly_Validated...")
    df_validated_enriched = enrich(df_validated)

    # 3. Export enriched validated dataset
    print(f"Exporting enriched dataset to {OUTPUT_FILE}...")
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df_validated_enriched.to_csv(OUTPUT_FILE, index=False)

    # 4. Generate extended forecast (36 months)
    print("Generating 36-month forecast...")
    df_forecast = forecast_racks(df_validated)

    # 5. Export forecast dataset
    print(f"Exporting forecast dataset to {FORECAST_FILE}...")
    os.makedirs(os.path.dirname(FORECAST_FILE), exist_ok=True)
    df_forecast.to_csv(FORECAST_FILE, index=False)

    print("ETL pipeline complete ✅")

# --- Entry Point ---
if __name__ == "__main__":
    main()
