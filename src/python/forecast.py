import pandas as pd
from prophet import Prophet

# -----------------------------
# Function: forecast_metric
# Purpose: Forecast a given metric (e.g., racks, IT load, total load)
# -----------------------------
def forecast_metric(df, metric, periods=12):
    # Prepare data for Prophet
    ts = df[["Date", metric]].rename(columns={"Date": "ds", metric: "y"})
    
    # Fit model
    model = Prophet()
    model.fit(ts)
    
    # Create future dataframe (monthly, using 'ME' for month-end)
    future = model.make_future_dataframe(periods=periods, freq="ME")
    
    # Forecast
    forecast = model.predict(future)
    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]

# -----------------------------
# Main Forecasting Process
# -----------------------------
def main():
    # Load enriched monthly dataset
    df = pd.read_csv("data/processed/enriched_monthly.csv", parse_dates=["Date"])
    
    results = []
    for dc in df["DataCentre"].unique():
        dc_df = df[df["DataCentre"] == dc]
        
        # Forecast racks, IT load, total load
        racks_fc = forecast_metric(dc_df, "Total_Contracted")
        it_fc = forecast_metric(dc_df, "Avg_IT_Load")
        total_fc = forecast_metric(dc_df, "Avg_Total_Load")
        
        # Tag forecasts with DC name
        racks_fc["DataCentre"] = dc
        it_fc["DataCentre"] = dc
        total_fc["DataCentre"] = dc
        
        # Add metric labels
        results.append(racks_fc.assign(Metric="Total_Contracted"))
        results.append(it_fc.assign(Metric="Avg_IT_Load"))
        results.append(total_fc.assign(Metric="Avg_Total_Load"))
    
    # Concatenate all forecasts
    final_fc = pd.concat(results)
    final_fc.to_csv("data/processed/forecast.csv", index=False)

# Entry point
if __name__ == "__main__":
    main()
