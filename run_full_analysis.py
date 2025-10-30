#!/usr/bin/env python3
"""
Full Analysis Pipeline for Salifort Motors Employee Retention Project
This script runs the complete analysis pipeline in sequence:
1. Data preprocessing and exploratory analysis
2. Model training
3. Model evaluation
4. Dashboard creation
"""

import logging
import os
import subprocess
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path


logger = logging.getLogger("pipeline")

def print_section(title):
    """Print a section title with formatting."""
    border = "=" * (len(title) + 10)
    print(f"\n{border}")
    print(f"===  {title}  ===")
    print(f"{border}\n")

def setup_logging():
    """Configure application logging for the analysis pipeline."""
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    log_file = logs_dir / "pipeline.log"

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info("Logging initialized. Writing to %s", log_file)


def run_script(script_name, description):
    """Run a Python script and capture its output."""
    print_section(description)
    try:
        logger.info("Starting %s", script_name)
        result = subprocess.run(['python', script_name],
                              capture_output=True,
                              text=True,
                              check=True)
        print(result.stdout)
        if result.stderr:
            logger.warning("Warnings/Errors from %s:\n%s", script_name, result.stderr)
        logger.info("%s completed successfully.", script_name)
        print(f"{script_name} completed successfully.\n")
        return True
    except subprocess.CalledProcessError as e:
        logger.error("Error running %s: %s", script_name, e.stderr or e)
        print(f"Error running {script_name}:")
        print(e.stderr)
        return False

def create_directory_structure():
    """Create the project directory structure if it doesn't exist."""
    directories = [
        "../data/raw",
        "../data/processed",
        "../results/analyzed_data",
        "../results/model_comparison",
        "../models",
        "../documentation"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")

def main():
    """Run the full analysis pipeline."""
    setup_logging()
    start_time = time.time()

    print_section("SALIFORT MOTORS EMPLOYEE RETENTION ANALYSIS")
    logger.info("Starting full analysis pipeline.")
    print("Starting full analysis pipeline...")
    
    # Create directory structure
    print_section("CREATING DIRECTORY STRUCTURE")
    create_directory_structure()
    
    # Check if input data exists
    data_path = "./data/raw/HR_capstone_dataset.csv"
    if not os.path.exists(data_path):
        logger.error("Input dataset not found at %s", data_path)
        print("Error: Input dataset not found.")
        print(f"Please ensure the dataset HR_capstone_dataset.csv exists at {data_path} before running this script.")
        return

    # Run exploratory analysis
    if not run_script("exploratory_analysis.py", "EXPLORATORY DATA ANALYSIS"):
        logger.error("Exploratory analysis failed. Stopping pipeline.")
        print("Exploratory analysis failed. Stopping pipeline.")
        return

    # Run model training
    if not run_script("model_training.py", "MODEL TRAINING"):
        logger.error("Model training failed. Stopping pipeline.")
        print("Model training failed. Stopping pipeline.")
        return

    # Run model evaluation
    if not run_script("model_evaluation.py", "MODEL EVALUATION"):
        logger.error("Model evaluation failed. Stopping pipeline.")
        print("Model evaluation failed. Stopping pipeline.")
        return

    # Create interactive dashboard
    if not run_script("interactive_dashboard.py", "INTERACTIVE DASHBOARD CREATION"):
        logger.warning("Dashboard creation encountered errors. Pipeline completed with warnings.")
        print("Dashboard creation failed. Pipeline completed with warnings.")

    # Calculate and print total execution time
    end_time = time.time()
    execution_time = end_time - start_time
    minutes, seconds = divmod(execution_time, 60)
    hours, minutes = divmod(minutes, 60)
    
    print_section("ANALYSIS PIPELINE COMPLETED")
    execution_summary = f"Total execution time: {int(hours)}h {int(minutes)}m {int(seconds)}s"
    logger.info(execution_summary)
    print(execution_summary)
    print("\nResults available in:")
    print("- Exploratory analysis: ../results/analyzed_data/")
    print("- Model evaluation: ../results/model_comparison/")
    print("- Executive summary: ../documentation/executive_summary.md")
    print("- Interactive dashboard: interactive_dashboard.html")
    print("\nTo view the dashboard, open the interactive_dashboard.html file in your web browser.")

if __name__ == "__main__":
    main()
