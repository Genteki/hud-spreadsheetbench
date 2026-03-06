"""Split dataset.json into individual task JSON files."""

import json
import os
from pathlib import Path

# Paths
DATA_DIR = Path(__file__).parent
DATASET_FILE = DATA_DIR / "dataset.json"
TASKS_DIR = DATA_DIR / "tasks"

def split_dataset():
    """Split the dataset.json into individual task JSON files."""
    # Create tasks directory if it doesn't exist
    TASKS_DIR.mkdir(exist_ok=True)

    # Read the dataset
    with open(DATASET_FILE, 'r') as f:
        tasks = json.load(f)

    # Write each task to its own file
    for task in tasks:
        task_id = task["id"]
        task_file = TASKS_DIR / f"{task_id}.json"

        with open(task_file, 'w') as f:
            json.dump(task, f, indent=2)

        print(f"Created: {task_file}")

    print(f"\nTotal tasks: {len(tasks)}")
    print(f"Saved to: {TASKS_DIR}")

if __name__ == "__main__":
    split_dataset()
