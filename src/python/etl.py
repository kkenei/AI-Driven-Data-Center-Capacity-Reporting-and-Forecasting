import pandas as pd
import glob
import os
from constants import DATA_CENTERS

# -----------------------------
# Utility: get latest Excel file in data/raw
# -----------------------------
def get_latest_excel():
    raw_dir = os.path.join(os.path.dirname(__file__), "../../data/raw")
    files = glob.glob(os.path.join(raw_dir, "*.xlsx"))
    if not files:
        raise FileNotFoundError("No Excel files found in data/raw/")
    return max(files, key=os.path.getctime)

# -----------------------------
# Function: enrich_daily
# -----------------------------
def enrich_daily(dc_name, df):
    df["Power_Utilization_%"] = (df["Used_Power_kW"] / df["Total_Power_kW"]) * 100
    df["Rack_Utilization_%"] = (df["Used_Racks"] / df["Total_Racks"]) * 100
    df["Cooling_Utilization_%"] = (df["Used_Cooling_kW"] / df["Total_Cooling_kW"]) * 100
    df["Daily_Energy_kWh"] = df["Used_Power_kW"] * 24
    return df

# -----------------------------
# Function: enrich_monthly
# -----------------------------
def enrich_monthly(dc_name, df):
    dc = DATA_CENTERS[dc_name]
    df["Remaining_Racks"] = dc["SELLABLE_RACKS"] - df["Total_Contracted"]
    df["Space_Fill_%"] = (df["Total_Contracted"] / dc["SELLABLE_RACKS"]) * 100
    df["Remaining_Load_kW"] = dc["SELLABLE_LOAD_KW"] - df["Avg_Total_Load"]
    df["Load_Fill_%"] = (df["Avg_Total_Load"] / dc["SELLABLE_LOAD_KW"]) * 100
    df["Available_IT_kW"] = dc["DESIGN_IT_CAPACITY_KW"] - df["Avg_IT_Load"]
    df["Utilization_%"] = (df["Avg_IT_Load"] / dc["DESIGN_IT_CAPACITY_KW"]) * 100
    df["Energy_kWh"] = df["Avg_Total_Load"] * 730
    df["Demand_Ratio"] = df["Avg_Total_Load"] / (
        df["Total_Contracted"] * dc["CONTRACT_DENSITY_KW_PER_RACK"]
    )
    df["Actual_Density_kW_per_Rack"] = df["Avg_IT_Load"] / df["Total_Contracted"]
    return df

# -----------------------------
# Main ETL Process
# -----------------------------
def main():
    latest_file = get_latest_excel()
    print(f"[INFO] Using latest Excel file: {latest_file}")

    # --- Daily Operational Data ---
    daily_df = pd.read_excel(latest_file, sheet_name="Operational_Daily")
    enriched_daily = []
    for dc_name in DATA_CENTERS.keys():
        dc_df = daily_df[daily_df["DataCenter"] == dc_name].copy()
        enriched_daily.append(enrich_daily(dc_name, dc_df))
    final_daily = pd.concat(enriched_daily)
    final_daily.to_csv("data/processed/enriched_daily.csv", index=False)
    print("[INFO] Saved enriched_daily.csv")

    # --- Monthly Validated Data ---
    monthly_validated_df = pd.read_excel(latest_file, sheet_name="Monthly_Validated")
    enriched_monthly = []
    for dc_name in DATA_CENTERS.keys():
        dc_df = monthly_validated_df[monthly_validated_df["DataCentre"] == dc_name].copy()
        enriched_monthly.append(enrich_monthly(dc_name, dc_df))
    final_monthly = pd.concat(enriched_monthly)
    final_monthly.to_csv("data/processed/enriched_monthly.csv", index=False)
    print("[INFO] Saved enriched_monthly.csv")

    # --- Monthly Raw Data (internal review) ---
    monthly_raw_df = pd.read_excel(latest_file, sheet_name="Monthly_Raw")
    enriched_raw = []
    for dc_name in DATA_CENTERS.keys():
        dc_df = monthly_raw_df[monthly_raw_df["DataCentre"] == dc_name].copy()
        enriched_raw.append(enrich_monthly(dc_name, dc_df))
    final_raw = pd.concat(enriched_raw)
    final_raw.to_csv("data/processed/enriched_monthly_raw.csv", index=False)
    print("[INFO] Saved enriched_monthly_raw.csv")

# Entry point
if __name__ == "__main__":
    main()
