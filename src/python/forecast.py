# Import core libraries
import pandas as pd                          # For data manipulation and CSV I/O
from prophet import Prophet                  # Facebook Prophet for time series forecasting
from sklearn.metrics import (                # Accuracy metrics for evaluating forecasts
    mean_absolute_percentage_error,
    mean_squared_error
)
import numpy as np                           # For numerical operations (e.g., sqrt)
import os                                    # For file/directory handling

# -----------------------------
# Function: forecast_metric
# Purpose: Forecast a given metric for a given horizon
# -----------------------------
def forecast_metric(df, metric, periods=12, horizon_label="12m"):
    # Prepare dataset: Prophet requires 'ds' (date) and 'y' (value)
    ts = df[["Reporting_Date", metric]].rename(columns={"Reporting_Date": "ds", metric: "y"})
    ts = ts.dropna()  # Remove rows with missing values

    # Initialize and fit Prophet model
    model = Prophet()
    model.fit(ts)

    # Create future dates (monthly frequency, 'ME' = month-end)
    future = model.make_future_dataframe(periods=periods, freq="ME")

    # Generate forecast
    forecast = model.predict(future)

    # Extract relevant forecast columns
    result = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].copy()
    # Add metadata for clarity
    result["Metric"] = metric
    result["Horizon"] = horizon_label
    return result

# -----------------------------
# Function: evaluate_forecast
# Purpose: Calculate forecast accuracy metrics (MAPE, RMSE)
# -----------------------------
def evaluate_forecast(df, metric):
    # Prepare dataset
    ts = df[["Reporting_Date", metric]].dropna()
    ts = ts.rename(columns={"Reporting_Date": "ds", metric: "y"})

    # Skip evaluation if dataset is too short (<6 months)
    if len(ts) < 6:
        print(f"[SKIP] Not enough data to evaluate forecast for {metric}")
        return {"Metric": metric, "MAPE": None, "RMSE": None}

    # Train/test split: last 3 months as test set
    train = ts.iloc[:-3]
    test = ts.iloc[-3:]

    # Fit Prophet on training data
    model = Prophet()
    model.fit(train)

    # Forecast next 3 months
    future = model.make_future_dataframe(periods=3, freq="ME")
    forecast = model.predict(future)

    # Merge forecast with test set on 'ds' (safe alignment)
    merged = test.merge(forecast[["ds", "yhat"]], on="ds", how="inner")

    # If no matching dates, skip evaluation
    if merged.empty:
        print(f"[SKIP] No matching forecast dates for {metric}")
        return {"Metric": metric, "MAPE": None, "RMSE": None}

    # Extract actual vs predicted values
    y_true = merged["y"].values
    y_pred = merged["yhat"].values

    # Calculate accuracy metrics
    mape = mean_absolute_percentage_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))

    return {"Metric": metric, "MAPE": mape, "RMSE": rmse}

# -----------------------------
# Function: detect_anomalies
# Purpose: Flag deviations between actuals and forecast
# -----------------------------
def detect_anomalies(df, metric):
    # Prepare dataset
    ts = df[["Reporting_Date", metric]].dropna()
    ts = ts.rename(columns={"Reporting_Date": "ds", metric: "y"})

    # Fit Prophet on full dataset
    model = Prophet()
    model.fit(ts)

    # Forecast values for existing dates
    forecast = model.predict(ts[["ds"]])

    # Merge actuals with forecast
    merged = ts.merge(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]], on="ds")

    # Flag anomalies: actual outside confidence interval
    merged["Anomaly"] = (merged["y"] < merged["yhat_lower"]) | (merged["y"] > merged["yhat_upper"])
    anomalies = merged[merged["Anomaly"]]
    anomalies["Metric"] = metric
    return anomalies

# -----------------------------
# Main Forecasting Process
# -----------------------------
def main():
    # Load enriched monthly dataset
    df = pd.read_csv("data/enriched/enriched_monthly.csv", parse_dates=["Reporting_Date"])

    # Containers for outputs
    results = []           # Forecast results
    quality_results = []   # Forecast accuracy metrics
    anomalies_results = [] # Anomaly detection results

    # Metrics to forecast
    metrics_to_forecast = [
        "Total_Contracted_Racks",
        "Avg_IT_Load_kW",
        "Avg_Total_Load_kW",
        "Remaining_Capacity",
        "PUE_vs_Target",
        "Rack_Utilization_vs_Design_%"
    ]

    # Horizons: short (6m), medium (12m), long (24m)
    horizons = [(6, "6m"), (12, "12m"), (24, "24m")]

    # Loop through each data center
    for dc in df["Data_Center_Name"].unique():
        dc_df = df[df["Data_Center_Name"] == dc]

        # Loop through each metric
        for metric in metrics_to_forecast:
            # Forecast for multiple horizons
            for periods, label in horizons:
                fc = forecast_metric(dc_df, metric, periods=periods, horizon_label=label)
                fc["Data_Center_Name"] = dc
                results.append(fc)

            # Evaluate forecast quality
            quality = evaluate_forecast(dc_df, metric)
            quality["Data_Center_Name"] = dc
            quality_results.append(quality)

            # Detect anomalies
            anomalies = detect_anomalies(dc_df, metric)
            anomalies["Data_Center_Name"] = dc
            anomalies_results.append(anomalies)

    # Save forecasts
    final_fc = pd.concat(results)
    os.makedirs("data/processed", exist_ok=True)  # Ensure output folder exists
    final_fc.to_csv("data/processed/forecast.csv", index=False)

    # Save forecast quality metrics
    quality_df = pd.DataFrame(quality_results)
    quality_df.to_csv("data/processed/forecast_quality.csv", index=False)

    # Save anomalies
    if anomalies_results:
        anomalies_df = pd.concat(anomalies_results)
        anomalies_df.to_csv("data/processed/forecast_anomalies.csv", index=False)

# Entry point: run main() if script is executed directly
if __name__ == "__main__":
    main()
