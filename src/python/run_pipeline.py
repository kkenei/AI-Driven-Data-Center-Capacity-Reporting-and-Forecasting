#!/usr/bin/env python3
# Shebang line: tells the system to run this script using Python 3 interpreter

"""
run_pipeline.py
Purpose: Orchestrates the full pipeline — ETL + Forecast — so sync_pipeline.sh
can call a single entry point.
"""

import subprocess   # Import subprocess module to run external commands (like calling other Python scripts)
import sys          # Import sys module to allow exiting the program with error codes

def run_step(step_name, command):
    """
    Helper function to run a pipeline step with logging and error handling.
    Arguments:
      step_name: A string describing the step (e.g., 'ETL pipeline')
      command: A list containing the command to run (e.g., ['python3', 'src/python/etl.py'])
    """
    print(f"=== Starting {step_name} ===")   # Log the start of the step
    try:
        subprocess.run(command, check=True) # Run the command; check=True means raise error if it fails
        print(f"=== {step_name} complete ✅ ===")  # Log success if command runs without error
    except subprocess.CalledProcessError as e:
        # If the command fails, catch the error and log it
        print(f"[ERROR] {step_name} failed with exit code {e.returncode}")
        sys.exit(1)  # Exit the script with error code 1 to signal failure

def main():
    """
    Main function that orchestrates the pipeline steps.
    """
    # Step 1: Run ETL pipeline
    run_step("ETL pipeline", ["python3", "src/python/etl.py"])

    # Step 2: Run Forecast pipeline
    run_step("Forecast pipeline", ["python3", "src/python/forecast.py"])

    # Final log message after both steps succeed
    print("=== Full pipeline complete ✅ ===")

# Entry point: ensures main() runs only if this script is executed directly
if __name__ == "__main__":
    main()
