Global Adoption Playbook for Colocation Reporting

This playbook outlines the strategy for transitioning from Excel-based colocation reporting to a globally adopted, automated, and AI-enhanced reporting pipeline. It builds on the Colocation Metrics Dictionary to ensure clarity, consistency, and scalability.

1. Vision & Objectives

Eliminate manual Excel tasks: Excel remains only as a raw data capture tool, not a calculation engine.

Establish a single source of truth: Python ETL enriches raw data into standardized metrics.

Enable executive-ready dashboards: Power BI visualizes metrics with drill-downs from global to rack-level.

Integrate AI intelligence: Forecasting, anomaly detection, and narrative insights enhance decision-making.

Ensure global scalability: Framework supports multiple data centres, regions, and future expansion.

2. Workflow Architecture

Data Capture Layer (Excel)

Operators input daily, monthly, and validated metrics.

Standardized column names across all sheets.

No formulas or calculations in Excel.

ETL Layer (Python)

Normalize column names to avoid ambiguity.

Apply enrichments (capacity, space, load, ratios, compliance).

Export enriched CSV (enriched_monthly.csv) with consistent schema.

Presentation Layer (Power BI)

Connect to enriched CSV.

Build dashboards:

Executive Summary: Global contracted load, space fill %, PUE compliance.

Regional Drill-Downs: Country-level capacity and utilization.

Rack-Level Detail: Contracted vs available metrics.

Auto-refresh tied to ETL outputs.

AI Layer

Forecasting: Predict contracted growth, IT load, cooling demand.

Anomaly Detection: Flag unusual PUE spikes or load ratios.

Narrative Insights: Auto-generate executive summaries.

Scenario Simulation: Model impact of density changes or new capacity.

3. Governance & Standards

Metrics Dictionary: Defines every measure, formula, and unit.

Naming Conventions: _kW, _m2, _Racks, _% suffixes for clarity.

Constants Management: All design values stored in DATA_CENTERS configuration.

Auditability: ETL logs transformations and schema changes.

Compliance: PUE and efficiency metrics aligned with industry standards.

4. Implementation Roadmap

Phase 1: Foundation

Standardize Excel schema.

Build ETL pipeline with enrichments.

Validate enriched CSV outputs.

Phase 2: Visualization

Develop Power BI dashboards.

Align visuals with executive reporting needs.

Phase 3: Intelligence

Integrate AI forecasting and anomaly detection.

Add narrative insights for executive summaries.

Phase 4: Global Rollout

Extend to all data centres.

Train operators and executives on new workflow.

Establish governance and continuous improvement.

5. Key Benefits

Clarity: Every metric defined and standardized.

Efficiency: Elimination of manual Excel calculations.

Scalability: Easy to add new data centres.

Trust: Executives rely on consistent, auditable data.

Innovation: AI enhances forecasting and decision-making.

This playbook provides the framework for global adoption of automated colocation reporting, ensuring clarity, scalability, and intelligence across all data centres.





TippleK Data Centres KPI Dictionary
1. Capacity KPIs
KPI	Formula	Notes
IT Capacity Installed (kW)	SUM('enriched_monthly'[Design_IT_Capacity_kW])	Total design IT capacity
IT Capacity Installed (per DC)	CALCULATE(SUM('enriched_monthly'[Design_IT_Capacity_kW]), 'enriched_monthly'[Data_Center_Name] = "KenyaDC"/"UgandaDC"/"TanzaniaDC")	Installed capacity by site
IT Capacity Used (kW)	SUM('enriched_monthly'[Avg_IT_Load_kW])	Total average IT load
IT Capacity Used (per DC)	CALCULATE(AVERAGE('enriched_monthly'[Avg_IT_Load_kW]), 'enriched_monthly'[Data_Center_Name] = "KenyaDC"/"UgandaDC"/"TanzaniaDC")	Used capacity by site
IT Capacity Available (kW)	SUM('enriched_monthly'[Design_IT_Capacity_kW]) - SUM('enriched_monthly'[Avg_IT_Load_kW])	Remaining IT capacity
IT Capacity Available (per DC)	CALCULATE([Total IT Capacity Available (kW)], 'enriched_monthly'[Data_Center_Name] = "KenyaDC"/"UgandaDC"/"TanzaniaDC")	Available capacity by site
IT Capacity Utilization (%)	DIVIDE([IT Capacity Used (kW)], [IT Capacity Installed (kW)], 0)	Portfolio utilization
IT Capacity Utilization (per DC)	DIVIDE([IT Capacity Used DC (kW)], [IT Capacity Installed DC (kW)], 0)	Utilization by site
IT Capacity Growth Rate (MoM %)	DIVIDE([IT Capacity Available (kW)] - CALCULATE([IT Capacity Available (kW)], DATEADD('Calendar'[Date], -1, MONTH)), CALCULATE([IT Capacity Available (kW)], DATEADD('Calendar'[Date], -1, MONTH)), 0)	Month‑over‑month growth
2. Space & Load KPIs
KPI	Formula	Notes
Space Contracted (m²)	SUM('enriched_monthly'[Contracted_Space_m2])	Total contracted space
Space Contracted (Racks)	SUM('enriched_monthly'[Total_Contracted_Racks])	Total contracted racks
Load Contracted (kW)	SUM('enriched_monthly'[Contracted_Load_kW])	Total contracted IT load
Load Fill Ratio (%)	DIVIDE([IT Capacity Used (kW)], [Load Contracted (kW)], 0)	Used vs contracted load
Load Sellable Remaining (kW)	SUM('enriched_monthly'[Remaining_Load_kW])	Remaining sellable load
Load Sellable Remaining (%)	DIVIDE([Load Sellable Remaining (kW)], [Load Contracted (kW)], 0)	Remaining load %
Space Sellable Remaining (m²)	SUM('enriched_monthly'[Remaining_Space_m2])	Remaining sellable space
Space Sellable Remaining (Racks)	SUM('enriched_monthly'[Remaining_Racks])	Remaining sellable racks
Space Sellable Remaining (%)	DIVIDE([Space Sellable Remaining (m²)], [Space Contracted (m²)], 0)	Remaining space %
3. Efficiency KPIs
KPI	Formula	Notes
Facility Power (kW)	SUM('enriched_monthly'[Facility_Power_kW])	Total facility power
PUE	DIVIDE(SUM('enriched_monthly'[Facility_Power_kW]), [IT Capacity Used (kW)], 0)	Power Usage Effectiveness
PUE Compliance (%)	DIVIDE(CALCULATE(COUNTROWS('enriched_monthly'), 'enriched_monthly'[PUE] <= 1.5), COUNTROWS('enriched_monthly), 0)	% of records compliant
Energy Consumption (kWh)	SUM('enriched_monthly'[Energy_Consumption_kWh])	Total energy consumption
Cooling Load (kW)	SUM('enriched_monthly'[Cooling_Load_kW])	Cooling load
Cooling Efficiency (%)	DIVIDE([Cooling Load (kW)], SUM('enriched_monthly'[Facility_Power_kW]), 0)	Cooling load vs facility power
4. Forecast & Anomaly KPIs
KPI	Formula	Notes
IT Capacity Forecasted (kW)	SUM('forecast'[Forecast_kW])	Forecasted IT capacity
Forecast Variance (kW)	[IT Capacity Forecasted (kW)] - [IT Capacity Used (kW)]	Difference forecast vs actual
Forecast Accuracy (%)	1 - DIVIDE(ABS([Forecast Variance (kW)]), [IT Capacity Used (kW)], 0)	Forecast accuracy
Forecast Error MAPE (%)	AVERAGE('forecast_quality'[MAPE])	Mean Absolute Percentage Error
Forecast Error RMSE	AVERAGE('forecast_quality'[RMSE])	Root Mean Square Error
Anomaly Count	COUNTROWS('forecast_anomalies')	Number of anomalies detected
Anomaly Severity Index	AVERAGE('forecast_anomalies'[Severity])	Average anomaly severity
