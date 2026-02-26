"""Configuration loader for Jupyter server."""

import os

VOLUMES_PATH = "/app/data/"
SOLUTIONS_PATH = "/app/shared_data"
SPREADSHEETBENCH_DATASET_NAME = "all_data_912_v0.1"
SPREADSHEETBENCH_DATASET_PATH = os.path.join(VOLUMES_PATH, SPREADSHEETBENCH_DATASET_NAME)