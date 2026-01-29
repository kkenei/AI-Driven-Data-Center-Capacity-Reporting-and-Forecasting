import pandas as pd
from constants import DATA_CENTERS

# -----------------------------
# Function: enrich_daily
# Purpose: Add derived metrics to daily operational data (Sheet1)
# -----------------------------
def enrich_daily(dc_name, df):
    # Calculate % utilization of power, racks, and cooling
    df["Power_Utilization_%"] = (df["Used_Power_kW"] / df["Total_Power_kW"]) * 100
    df["Rack_Utilization_%"] = (df["Used_Racks"] / df["Total_Racks"]) * 100
    df["Cooling_Utilization_%"] = (df["Used_Cooling_kW"] / df["Total_Cooling_kW"]) * 100
    
    # Estimate daily energy consumption (kWh) assuming 24h operation
    df["Daily_Energy_kWh"] = df["Used_Power_kW"] * 24
    return df

# -----------------------------
# Function: enrich_monthly
# Purpose: Add derived metrics to monthly validated data (Sheet3)
# -----------------------------
def enrich_monthly(dc_name, df):
    dc = DATA_CENTERS[dc_name]  # Load constants for this data center
    
    # Remaining racks available for sale
    df["Remaining_Racks"] = dc["SELLABLE_RACKS"] - df["Total_Contracted"]
    
    # % of racks sold vs. total available
    df["Space_Fill_%"] = (df["Total_Contracted"] / dc["SELLABLE_RACKS"]) * 100
    
    # Remaining facility load capacity (kW)
    df["Remaining_Load_kW"] = dc["SELLABLE_LOAD_KW"] - df["Avg_Total_Load"]
    
    # % of facility load consumed
    df["Load_Fill_%"] = (df["Avg_Total_Load"] / dc["SELLABLE_LOAD_KW"]) * 100
    
    # Remaining IT headroom before hitting design limit
    df["Available_IT_kW"] = dc["DESIGN_IT_CAPACITY_KW"] - df["Avg_IT_Load"]
    
    # % utilization of IT design capacity
    df["Utilization_%"] = (df["Avg_IT_Load"] / dc["DESIGN_IT_CAPACITY_KW"]) * 100
    
    # Monthly energy consumption (kWh) ~730 hours/month
    df["Energy_kWh"] = df["Avg_Total_Load"] * 730
    
    # Demand ratio: actual load vs. contracted load
    df["Demand_Ratio"] = df["Avg_Total_Load"] / (
        df["Total_Contracted"] * dc["CONTRACT_DENSITY_KW_PER_RACK"]
    )
    
    # Actual density per rack (kW/rack)
    df["Actual_Density_kW_per_Rack"] = df["Avg_IT_Load"] / df["Total_Contracted"]
    return df

# -----------------------------
# Main ETL Process
# Purpose: Read Excel sheets, enrich data, and save outputs
# -----------------------------
def main():
    # --- Daily Operational Data (Sheet1) ---
    daily_df = pd.read_excel(
        "data/raw/Colocation_Capacity_Forecasting_2025_2026_v1.0.xlsx",
        sheet_name="Operational_Daily"
    )
    enriched_daily = []
    for dc_name in DATA_CENTERS.keys():
        dc_df = daily_df[daily_df["DataCenter"] == dc_name].copy()
        enriched_daily.append(enrich_daily(dc_name, dc_df))
    final_daily = pd.concat(enriched_daily)
    final_daily.to_csv("data/processed/enriched_daily.csv", index=False)
    
    # --- Monthly Validated Data (Sheet3) ---
    monthly_df = pd.read_excel(
        "data/raw/Colocation_Capacity_Forecasting_2025_2026_v1.0.xlsx",
        sheet_name="Monthly_Validated"
    )
    enriched_monthly = []
    for dc_name in DATA_CENTERS.keys():
        dc_df = monthly_df[monthly_df["DataCentre"] == dc_name].copy()
        enriched_monthly.append(enrich_monthly(dc_name, dc_df))
    final_monthly = pd.concat(enriched_monthly)
    final_monthly.to_csv("data/processed/enriched_monthly.csv", index=False)

# Entry point
if __name__ == "__main__":
    main()
