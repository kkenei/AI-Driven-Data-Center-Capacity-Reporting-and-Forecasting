Colocation


 Metrics Dictionary

This document defines the key measures used in global colocation capacity reporting. Each metric includes its formula, unit, and source, ensuring clarity and consistency across ETL, Power BI, and executive dashboards.

Capacity Metrics

Available IT Capacity (kW)Formula: Design_IT_Capacity_kW - Avg_IT_Load_kWUnit: kWSource: Constants + Monthly Validated

Average IT Capacity (kW)Formula: Avg_IT_Load_kW (direct from raw data)Unit: kWSource: Monthly Validated

Contracted Load (kW)Formula: Total_Contracted_Racks * Contract_Density_kW_per_RackUnit: kWSource: Constants + Monthly Validated

Space Metrics

Contracted Space (m²)Formula: Total_Contracted_Racks * Rack_Footprint_m2Unit: m²Source: Constants + Monthly Validated

Contracted Space (Racks)Formula: Total_Contracted_RacksUnit: RacksSource: Monthly Validated

Remaining Sellable Space (m²)Formula: (Design_Total_Racks - Total_Contracted_Racks) * Rack_Footprint_m2Unit: m²Source: Constants + Monthly Validated

Remaining Sellable Space (Racks)Formula: Design_Total_Racks - Total_Contracted_RacksUnit: RacksSource: Constants + Monthly Validated

Load Metrics

Remaining Sellable Load (kW)Formula: Design_Total_Load_kW - Avg_Total_Load_kWUnit: kWSource: Constants + Monthly Validated

Load Fill Ratio (%)Formula: (Avg_Total_Load_kW / Design_Total_Load_kW) * 100Unit: %Source: Constants + Monthly Validated

Utilization & Efficiency Metrics

Space Fill Ratio (%)Formula: (Total_Contracted_Racks / Design_Total_Racks) * 100Unit: %Source: Constants + Monthly Validated

PUE (Power Usage Effectiveness)Formula: Avg_Total_Load_kW / Avg_IT_Load_kWUnit: RatioSource: Monthly Validated

PUE ComplianceFormula: PUE <= Design_PUEUnit: Boolean (True/False)Source: Constants + Monthly Validated

Notes

Constants (Design capacity, rack density, rack footprint, PUE target) are stored in DATA_CENTERS configuration.

Raw Data comes from Excel capture sheets (Operational_Daily, Monthly_Raw, Monthly_Validated).

ETL Layer enriches raw data into calculated fields before export to Power BI.

Power BI Layer aggregates and visualizes only — no hard-coded formulas.

This dictionary ensures global data centre management has a clear, consistent understanding of colocation metrics, enabling adoption of automated reporting and AI-driven insights.
