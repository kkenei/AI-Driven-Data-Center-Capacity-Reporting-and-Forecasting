 Progress Report – TippleK Data Centres

## Date: January 31, 2026

---

## 1. ETL Pipeline
- Fixed `constants.py` syntax error (missing comma).
- Mapped `Facility_Power_kW` to `Avg_Total_Load_kW`.
- Corrected enrichment order: define Facility Power before Cooling Load.
- Pipeline now produces consistent `enriched_monthly.csv`.

---

## 2. KPI Dictionary
- Built a structured KPI suite grouped into Capacity, Space/Load, Efficiency, Forecast/Anomalies.
- Standardized naming conventions (Installed, Used, Available, Utilization).
- Removed duplicate definitions (TanzaniaDC Utilization, PUE).

---

## 3. Power BI Model
- Designed star schema:
  - Fact tables: `enriched_monthly`, `forecast`, `forecast_quality`, `forecast_anomalies`.
  - Dimension tables: `Calendar`, `Data_Center_Metadata`.
- Relationships established via `Date` and `Data_Center_Name`.
- Supports drill-down from portfolio → country → site → rack.

---

## 4. Executive Readiness
- KPI dictionary aligned with Global Adoption Playbook.
- Documentation structured for stakeholder presentation.
- ETL + Power BI integration now demo-ready.



## Date: February 2, 2026

## 1. ETL Pipeline
- Fixed `constants.py` syntax error (missing comma).
- Mapped `Facility_Power_kW` to `Avg_Total_Load_kW`.
- Corrected enrichment order: define Facility Power before Cooling Load.
- Added mapping for `Design_Total_Racks` and `Design_Total_Footprint_m2` into enriched dataset.
- Derived denominators:
  - `Design_Space_m2` from `Gross_White_Space_m2`.
  - `Design_Space_Racks` from `Design_Total_Racks × Rack_Footprint_m2`.
- Introduced new KPIs:
  - `Remaining_vs_Design_%`
  - `Remaining_vs_Design_Racks_%`
- Pipeline now produces consistent `enriched_monthly.csv` with design constants + KPIs.

---

## 2. KPI Dictionary
- Built a structured KPI suite grouped into Capacity, Space/Load, Efficiency, Forecast/Anomalies.
- Standardized naming conventions (Installed, Used, Available, Utilization).
- Removed duplicate definitions (TanzaniaDC Utilization, PUE).
- Extended dictionary to include new denominators (`Design_Space_m2`, `Design_Space_Racks`) for clarity in executive vs technical views.

---

## 3. Power BI Model
- Designed star schema:
  - Fact tables: `enriched_monthly`, `forecast`, `forecast_quality`, `forecast_anomalies`.
  - Dimension tables: `Calendar`, `Data_Center_Metadata`.
- Relationships established via `Date` and `Data_Center_Name`.
- Supports drill-down from portfolio → country → site → rack.
- Measures updated to consume new denominators for realistic % KPIs.

---

## 4. Executive Readiness
- KPI dictionary aligned with Global Adoption Playbook.
- Documentation structured for stakeholder presentation.
- ETL + Power BI integration now demo-ready.
- GitHub workflow cleaned:
  - Minimal safe commit strategy (focus on `etl.py` changes).
  - Processed CSVs and backup scripts identified for `.gitignore`.
  - Repo history kept clean for executive review.
