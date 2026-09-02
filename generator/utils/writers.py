import os
import json
import csv
from typing import List, Dict, Any
from collections import defaultdict

# The base directory where data will be generated
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "landing")

def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

def write_csv(data: List[Dict[str, Any]], dataset_name: str, filename: str):
    """Write a list of dictionaries to a CSV file."""
    if not data:
        return

    dataset_dir = os.path.join(DATA_DIR, dataset_name)
    ensure_dir(dataset_dir)
    
    filepath = os.path.join(dataset_dir, filename)
    fieldnames = data[0].keys()

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def write_json_batches(data: List[Dict[str, Any]], dataset_name: str, date_field: str = None, batch_size: int = 10000):
    """
    Write data to JSON-line files in batches.
    If date_field is provided, groups records by date and writes files like:
    dataset_YYYY-MM-DD_00.json
    """
    if not data:
        return

    dataset_dir = os.path.join(DATA_DIR, dataset_name)
    ensure_dir(dataset_dir)

    if date_field:
        # Group by date
        grouped_data = defaultdict(list)
        for row in data:
            # Determine grouping date
            if "_file_arrival_date" in row:
                date_str = str(row.pop("_file_arrival_date"))[:10]
            else:
                date_str = str(row[date_field])[:10]
            grouped_data[date_str].append(row)
        
        for date_str, records in grouped_data.items():
            _write_batches(records, dataset_dir, f"{dataset_name}_{date_str}", batch_size)
    else:
        _write_batches(data, dataset_dir, dataset_name, batch_size)

def _write_batches(data: List[Dict[str, Any]], dataset_dir: str, prefix: str, batch_size: int):
    """Helper to split data into batches and write JSON Lines."""
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        batch_idx = i // batch_size
        filename = f"{prefix}_{batch_idx:02d}.json"
        filepath = os.path.join(dataset_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for row in batch:
                f.write(json.dumps(row) + '\n')
