📘 Metrics Dictionary
Core Identifiers
Reporting_Date  
Definition: The month‑end reporting date for the dataset.
Type: Date (parsed as datetime).
Purpose: Primary time dimension for trend analysis and forecasting.

Data_Center_Name  
Definition: Name of the data center (e.g., KenyaDC, UgandaDC, TanzaniaDC).
Type: Text.
Purpose: Dimension for filtering, grouping, and comparisons across sites.

Raw Monthly Metrics
Total_Contracted_Racks  
Definition: Number of racks contracted by customers in the reporting month.
Purpose: Base measure of customer demand.

Reserved_Racks  
Definition: Racks reserved but not yet active.
Purpose: Pipeline indicator of upcoming utilization.

Decommissioned_Racks  
Definition: Racks removed from service.
Purpose: Tracks churn and capacity recovery.

Avg_IT_Load_kW  
Definition: Average IT load (kW) measured across the month.
Purpose: Indicator of actual compute demand.

Avg_Total_Load_kW  
Definition: Average total facility load (kW) across the month.
Purpose: Includes IT + overhead (cooling, power distribution).

Enrichment Metrics
Rack_Utilization_%  
Definition: (Reserved + Decommissioned) ÷ Total Contracted × 100.
Purpose: Shows how much of contracted capacity is actively used.

IT_Load_%  
Definition: Avg IT Load ÷ Avg Total Load × 100.
Purpose: Efficiency measure of IT vs facility load.

Remaining_Capacity  
Definition: Total Contracted Racks − (Reserved + Decommissioned).
Purpose: Available rack slots for new customers.

PUE (Power Usage Effectiveness)  
Definition: Avg Total Load ÷ Avg IT Load.
Purpose: Industry standard efficiency metric.

Design Constants (from constants.py)
Design_Total_Racks  
Definition: Maximum racks available for sale (design capacity).
Purpose: Benchmark for utilization vs design.

Design_IT_Capacity_kW  
Definition: Planned IT load capacity (kW).
Purpose: Benchmark for IT load vs design.

Design_Total_Load_kW  
Definition: Total facility load capacity (kW).
Purpose: Benchmark for facility load vs design.

PUE_Target  
Definition: Design target for Power Usage Effectiveness.
Purpose: Benchmark for efficiency vs target.

Comparisons (Actual vs Design)
Rack_Utilization_vs_Design_%  
Definition: Total Contracted Racks ÷ Design Total Racks × 100.
Purpose: Shows contracted demand relative to design capacity.

IT_Load_vs_Design_%  
Definition: Avg IT Load ÷ Design IT Capacity × 100.
Purpose: Tracks IT demand against planned design.

Total_Load_vs_Design_%  
Definition: Avg Total Load ÷ Design Total Load × 100.
Purpose: Tracks facility load against design capacity.

PUE_vs_Target  
Definition: Actual PUE ÷ PUE Target.
Purpose: Efficiency comparison against design expectations.

Forecast Outputs
ds  
Definition: Forecasted date (month‑end).
Purpose: Time dimension for forecast results.

yhat  
Definition: Forecasted value of the metric.
Purpose: Central prediction from Prophet model.

yhat_lower / yhat_upper  
Definition: Lower and upper bounds of forecast confidence interval.
Purpose: Range of possible outcomes.

Metric  
Definition: The metric being forecasted (e.g., Total_Contracted_Racks, Avg_IT_Load_kW, Avg_Total_Load_kW).
Purpose: Identifies which measure the forecast applies to.

Data_Center_Name  
Definition: Data center associated with forecast.
Purpose: Dimension for site‑specific forecasting.
