"""Manifest generation for the synthetic data."""
import os
import json
from datetime import datetime
from typing import Dict, Any
from generator.config import PROJECT_CONFIG

def create_manifest(
    generation_id: str,
    seed: int,
    scale: str,
    dataset_counts: Dict[str, int],
    dq_stats: Dict[str, int],
    base_dir: str
):
    """Write the generation_manifest.json file."""
    manifest = {
        "generation_id": generation_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "seed": seed,
        "scale": scale,
        "date_range": {
            "start": PROJECT_CONFIG["start_date"],
            "end": PROJECT_CONFIG["end_date"]
        },
        "datasets": {k: {"rows": v} for k, v in dataset_counts.items()},
        "dq_injections": dq_stats
    }
    
    metadata_dir = os.path.join(base_dir, "data", "generated_metadata")
    if not os.path.exists(metadata_dir):
        os.makedirs(metadata_dir)
        
    manifest_path = os.path.join(metadata_dir, "generation_manifest.json")
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
        
    return manifest
