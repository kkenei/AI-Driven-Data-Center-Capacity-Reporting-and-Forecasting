# KPI Dictionary – TippleK Data Centres

This dictionary defines the standardized KPIs used across Power BI dashboards and executive reporting.

---

## 1. Capacity KPIs
- **IT Capacity Installed (kW)** = SUM('enriched_monthly'[Design_IT_Capacity_kW])
- **IT Capacity Used (kW)** = SUM('enriched_monthly'[Avg_IT_Load_kW])
- **IT Capacity Available (kW)** = Installed – Used
- **Utilization (%)** = Used ÷ Installed
- **Growth Rate (MoM %)** = Month-over-month change in Available capacity

---

## 2. Space & Load KPIs
- **Space Contracted (m² / Racks)** = SUM('enriched_monthly'[Contracted_Space_m2]) / SUM('enriched_monthly'[Total_Contracted_Racks])
- **Load Contracted (kW)** = SUM('enriched_monthly'[Contracted_Load_kW])
- **Load Fill Ratio (%)** = Used ÷ Contracted
- **Sellable Remaining (kW / m² / Racks)** = SUM of remaining capacity
- **Sellable Remaining (%)** = Remaining ÷ Contracted

---

## 3. Efficiency KPIs
- **Facility Power (kW)** = SUM('enriched_monthly'[Facility_Power_kW])
- **PUE** = Facility Power ÷ IT Load
- **PUE Compliance (%)** = % of records with PUE ≤ 1.5
- **Energy Consumption (kWh)** = SUM('enriched_monthly'[Energy_Consumption_kWh])
- **Cooling Load (kW)** = Facility Power – IT Load
- **Cooling Efficiency (%)** = Cooling Load ÷ Facility Power

---

## 4. Forecast & Anomaly KPIs
- **Forecasted IT Capacity (kW)** = SUM('forecast'[Forecast_kW])
- **Forecast Variance (kW)** = Forecast – Actual
- **Forecast Accuracy (%)** = 1 – (|Variance| ÷ Actual)
- **Forecast Error MAPE (%)** = AVERAGE('forecast_quality'[MAPE])
- **Forecast Error RMSE** = AVERAGE('forecast_quality'[RMSE])
- **Anomaly Count** = COUNTROWS('forecast_anomalies')
- **Anomaly Severity Index** = AVERAGE('forecast_anomalies'[Severity])
