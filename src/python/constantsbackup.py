"""
Centralized constants for AI-Driven Data Center Capacity Reporting & Forecasting
Applicable to multiple colocation sites (KenyaDC, UgandaDC, TanzaniaDC).
"""

# Facility-level constants per data center
DATA_CENTERS = {
    "KenyaDC": {
        "Design_Total_Racks": 186,              # Total racks available for sale (design capacity)
        "Design_Total_Footpint_m2":500,          # Total Racks theoretical footprint
        "Gross_White_Space_m2": 800,             # Total data center space in m2
        "Contract_Density_kW_per_Rack": 5,      # Planned IT load per rack (kW)
        "Design_IT_Capacity_kW": 640,           # Design IT load capacity (kW)        
        "Design_Total_Load_kW": 900,            # Total facility load capacity (kW)
        "PUE_Target": 1.5                       # Design Power Usage Effectiveness
    },
    "UgandaDC": {
        "Design_Total_Racks": 200,
        "Design_Total_Footpint_m2":540,          # Total Racks theoretical footprint
        "Gross_White_Space_m2": 850,             # Total data center space in m2
        "Contract_Density_kW_per_Rack": 5,
        "Design_IT_Capacity_kW": 800,
        "Design_Total_Load_kW": 1200,
        "PUE_Target": 1.4
    },
    "TanzaniaDC": {
        "Design_Total_Racks": 150,
        "Design_Total_Footpint_m2":405,          # Total Racks theoretical footprint
        "Gross_White_Space_m2": 600,             # Total data center space in m2
        "Contract_Density_kW_per_Rack": 5,
        "Design_IT_Capacity_kW": 500,
        "Design_Total_Load_kW": 750,
        "PUE_Target": 1.6
    }
}
