#!/bin/bash
# Shebang line: tells the system to run this script using Bash

# === Pipeline Sync Script with Timestamps + Error Handling ===
# Script purpose: Automate upload of raw Excel, run ETL + forecast remotely, and download results

# -----------------------------
# Define paths and credentials
# -----------------------------
REMOTE_USER="kenei"                              # VPS username used for SSH/SCP
REMOTE_HOST="102.206.164.134"               # VPS IP or hostname
REMOTE_PROJECT="/home/kenei/projects/colocation-capacity-intelligence"  # Root project folder on VPS
REMOTE_DATA="$REMOTE_PROJECT/data/raw"          # Remote folder where raw Excel is uploaded
REMOTE_ENRICHED="$REMOTE_PROJECT/data/enriched" # Remote folder where enriched CSV is saved
REMOTE_PROCESSED="$REMOTE_PROJECT/data/processed" # Remote folder where forecast outputs are saved

LOCAL_DIR="/d/Data Center Business Intelligence Project Proposal" # Local folder on Drive D

# -----------------------------
# Helper function: timestamped logging
# -----------------------------
log() {
    # Function prints a message with current time in HH:MM:SS format
    echo "[$(date '+%H:%M:%S')] $1"
}

# -----------------------------
# Upload raw Excel to VPS
# -----------------------------
log "=== Starting pipeline sync ==="   # Log start of sync
log "[UPLOAD] Sending Colocation_Capacity_Data.xlsx to VPS..."  # Log upload step
scp "$LOCAL_DIR/Colocation_Capacity_Data.xlsx" $REMOTE_USER@$REMOTE_HOST:$REMOTE_DATA/ || {
    # Secure copy raw Excel file to VPS; if it fails, log error and exit
    log "[ERROR] Upload failed!"
    exit 1
}
log "[UPLOAD COMPLETE] Raw Excel sent."  # Log upload success

# -----------------------------
# Trigger remote ETL + forecast
# -----------------------------
log "[PROCESS] Executing ETL + Forecast on VPS..."  # Log process start
ssh $REMOTE_USER@$REMOTE_HOST "cd $REMOTE_PROJECT && source venv/bin/activate && python3 src/python/run_pipeline.py" || {
    # SSH into VPS, activate virtual environment, run pipeline script; if fails, log error and exit
    log "[ERROR] Remote pipeline execution failed!"
    exit 1
}
log "[PROCESS COMPLETE] Remote ETL + Forecast finished."  # Log process success

# -----------------------------
# Download enriched + forecast files
# -----------------------------
log "[DOWNLOAD] Fetching enriched + forecast CSVs back to Drive D..."  # Log download start

log " -> enriched_monthly.csv"  # Log file name
scp $REMOTE_USER@$REMOTE_HOST:$REMOTE_ENRICHED/enriched_monthly.csv "$LOCAL_DIR/" || {
    # Download enriched_monthly.csv from VPS; if fails, log error and exit
    log "[ERROR] Failed to download enriched_monthly.csv"
    exit 1
}
log "[DOWNLOAD COMPLETE] enriched_monthly.csv"  # Log success

log " -> forecast.csv"  # Log file name
scp $REMOTE_USER@$REMOTE_HOST:$REMOTE_PROCESSED/forecast.csv "$LOCAL_DIR/" || {
    # Download forecast.csv from VPS; if fails, log error and exit
    log "[ERROR] Failed to download forecast.csv"
    exit 1
}
log "[DOWNLOAD COMPLETE] forecast.csv"  # Log success

# -----------------------------
# Optional: Download forecast quality + anomalies
# -----------------------------
log " -> forecast_quality.csv"  # Log file name
scp $REMOTE_USER@$REMOTE_HOST:$REMOTE_PROCESSED/forecast_quality.csv "$LOCAL_DIR/" || {
    # Download forecast_quality.csv from VPS; if fails, log error and exit
    log "[ERROR] Failed to download forecast_quality.csv"
    exit 1
}
log "[DOWNLOAD COMPLETE] forecast_quality.csv"  # Log success

log " -> forecast_anomalies.csv"  # Log file name
scp $REMOTE_USER@$REMOTE_HOST:$REMOTE_PROCESSED/forecast_anomalies.csv "$LOCAL_DIR/" || {
    # Download forecast_anomalies.csv from VPS; if fails, log error and exit
    log "[ERROR] Failed to download forecast_anomalies.csv"
    exit 1
}
log "[DOWNLOAD COMPLETE] forecast_anomalies.csv"  # Log success

log "=== Pipeline sync complete! ==="  # Log end of sync
