"""
Centralized constants for AI-Driven Data Center Capacity Reporting & Forecasting
Applicable to multiple colocation sites (DC1, DC2, DC3).
"""

# Facility-level constants per data center
DATA_CENTERS = {
    "KenyaDC": {
        "SELLABLE_RACKS": 186,              # Total racks available for sale
        "CONTRACT_DENSITY_KW_PER_RACK": 5,  # Planned IT load per rack (kW)
        "DESIGN_IT_CAPACITY_KW": 640,       # Design IT load capacity (kW)
        "SELLABLE_LOAD_KW": 900,            # Total facility load capacity (kW)
        "DESIGN_PUE": 1.5                   # Design Power Usage Effectiveness
    },
    "UgandaDC": {
        "SELLABLE_RACKS": 200,
        "CONTRACT_DENSITY_KW_PER_RACK": 5,
        "DESIGN_IT_CAPACITY_KW": 800,
        "SELLABLE_LOAD_KW": 1200,
        "DESIGN_PUE": 1.4
    },
    "TanzaniaDC": {
        "SELLABLE_RACKS": 150,
        "CONTRACT_DENSITY_KW_PER_RACK": 5,
        "DESIGN_IT_CAPACITY_KW": 500,
        "SELLABLE_LOAD_KW": 750,
        "DESIGN_PUE": 1.6
    }
}

# Global thresholds for alerts
ALERT_THRESHOLDS = {
    "SPACE_FILL_ALERT": 0.75,   # Trigger alert if > 75% racks filled
    "POWER_FILL_ALERT": 0.80,   # Trigger alert if > 80% power filled
    "DESIGN_UTIL_ALERT": 0.80   # Trigger alert if > 80% IT design capacity used
}
