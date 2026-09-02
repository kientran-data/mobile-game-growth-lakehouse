"""Utilities for injecting intentional Data Quality issues."""
import random
import copy
from typing import List, Dict, Any, Tuple
from datetime import timedelta
from generator.utils.dates import parse_datetime

DQ_CONFIG = {
    "duplicate_event_rate": 0.002,
    "late_event_rate": 0.01,
    "invalid_country_rate": 0.001,
    "missing_player_id_rate": 0.0005,
}

def inject_dq_issues(datasets: Dict[str, List[Dict[str, Any]]]) -> Tuple[Dict[str, List[Dict[str, Any]]], Dict[str, int]]:
    """Inject intentional data quality issues into the generated datasets."""
    
    dq_stats = {
        "duplicate_events": 0,
        "late_events": 0,
        "invalid_country": 0,
        "missing_player_id": 0
    }
    
    # Process game_events
    if "game_events" in datasets:
        game_events = datasets["game_events"]
        new_game_events = []
        
        for evt in game_events:
            # 1. Invalid country
            if random.random() < DQ_CONFIG["invalid_country_rate"]:
                evt["country"] = "ZZ"
                dq_stats["invalid_country"] += 1
                
            # 2. Missing player_id
            if random.random() < DQ_CONFIG["missing_player_id_rate"]:
                evt["player_id"] = None
                dq_stats["missing_player_id"] += 1
            
            # 3. Late arriving simulation
            # By default file_date = event_time
            file_dt = parse_datetime(evt["event_time"].replace("Z", ""))
            
            if random.random() < DQ_CONFIG["late_event_rate"]:
                # Delay by 1 to 5 days
                delay_days = random.randint(1, 5)
                file_dt += timedelta(days=delay_days)
                dq_stats["late_events"] += 1
                
            evt["_file_arrival_date"] = file_dt.isoformat()[:10]
            
            # Add normal event
            new_game_events.append(evt)
            
            # 4. Duplicates (clone exactly)
            if random.random() < DQ_CONFIG["duplicate_event_rate"]:
                dup = copy.deepcopy(evt)
                # Keep same file arrival for duplicates
                new_game_events.append(dup)
                dq_stats["duplicate_events"] += 1
                
        datasets["game_events"] = new_game_events
        
    return datasets, dq_stats
