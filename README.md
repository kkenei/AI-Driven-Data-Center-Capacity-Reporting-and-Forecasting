# Colocation Capacity Intelligence

Data-driven capacity reporting & forecasting for colocation data centers.

## Current stack
- Source data: Excel
- Processing & forecasting: Python (pandas + prophet)
- Visualization: Power BI (.pbip format)
- Version control: Git

## Quick start (on this server)
1. Activate virtual environment:   `source .venv/bin/activate`
2. Install dependencies:           `pip install -r src/python/requirements.txt`
3. Run ETL:                        `python src/python/01_etl_clean.py`

## Folder structure
- data/raw/          → original Excel files (not committed)
- data/processed/    → cleaned CSVs & forecasts
- src/python/        → ETL & forecasting scripts
- src/powerbi/       → Power BI project files (.pbip)
