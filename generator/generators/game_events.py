"""Generator for game events simulating player engagement."""
import uuid
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

from generator.models.app_version import AppVersion
from generator.utils.dates import parse_datetime

def generate_game_events(installs: List[Dict[str, Any]], app_versions: List[AppVersion]) -> List[Dict[str, Any]]:
    """Generate game events based on player installs and retention curves."""
    events = []
    
    # Simple retention curve probabilities (D0 is 1.0, D1 is 0.4, D3 is 0.25, D7 is 0.15, D30 is 0.05)
    retention_curve = {
        1: 0.40,
        2: 0.30,
        3: 0.25,
        4: 0.22,
        5: 0.20,
        6: 0.18,
        7: 0.15,
        14: 0.08,
        30: 0.05
    }
    
    # To quickly find version info for a game and platform
    versions_by_game_platform = {}
    for v in app_versions:
        key = (v.game_id, v.platform)
        if key not in versions_by_game_platform:
            versions_by_game_platform[key] = []
        versions_by_game_platform[key].append(v)
        
    for k in versions_by_game_platform:
        versions_by_game_platform[k].sort(key=lambda x: x.release_date, reverse=True)

    def get_version_at_time(game_id, platform, event_time):
        valid = [v for v in versions_by_game_platform.get((game_id, platform), []) 
                 if parse_datetime(v.release_timestamp) <= event_time]
        return valid[0].version if valid else "1.0.0"

    for install in installs:
        player_id = install["player_id"]
        game_id = install["game_id"]
        platform = install["platform"]
        country = install["country"]
        
        install_dt = parse_datetime(install["install_time"])
        max_level = 1
        
        # Determine how many days this player will be active in the next 30 days
        active_days = [0] # Always active on D0
        for day in range(1, 31):
            prob = retention_curve.get(day)
            if prob is None:
                # Interpolate roughly
                if day < 14:
                    prob = 0.15 - ((day - 7) * 0.01)
                else:
                    prob = 0.08 - ((day - 14) * 0.002)
            
            # Boost retention slightly for paid users
            if not install["is_organic"]:
                prob *= 1.1
                
            if random.random() < prob:
                active_days.append(day)
                
        # Generate sessions for each active day
        for day_offset in active_days:
            active_dt = install_dt + timedelta(days=day_offset)
            # Ensure we don't go beyond our project end date (approx July 2026)
            if active_dt.year > 2026 or (active_dt.year == 2026 and active_dt.month > 6):
                continue
                
            # 1 to 3 sessions per active day
            num_sessions = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1])[0]
            
            for _ in range(num_sessions):
                session_hex = f"{random.getrandbits(32):08x}".upper()
                session_id = f"S_{session_hex}"
                
                # Randomize session start time on that day
                # If it's D0, session must start after install_time
                if day_offset == 0:
                    start_time = install_dt + timedelta(seconds=random.randint(5, 3600))
                else:
                    start_time = active_dt.replace(hour=random.randint(7, 22), minute=random.randint(0, 59))
                
                app_ver = get_version_at_time(game_id, platform, start_time)
                
                # Base event payload template
                base_event = {
                    "player_id": player_id,
                    "game_id": game_id,
                    "session_id": session_id,
                    "app_version": app_ver,
                    "platform": platform,
                    "country": country
                }
                
                current_time = start_time
                
                def create_event(name: str, props: Dict[str, Any], seconds_add: int) -> Dict[str, Any]:
                    nonlocal current_time
                    current_time += timedelta(seconds=seconds_add)
                    evt = base_event.copy()
                    evt_hex = f"{random.getrandbits(32):08x}".upper()
                    evt["event_id"] = f"EVT_{evt_hex}"
                    evt["event_name"] = name
                    evt["event_time"] = current_time.isoformat() + "Z"
                    evt["event_properties"] = props
                    return evt
                
                # Start Session
                events.append(create_event("session_start", {}, 0))
                events.append(create_event("app_open", {}, random.randint(1, 5)))
                
                # Gameplay loop (1 to 5 levels played per session)
                levels_to_play = random.randint(1, 5)
                for _ in range(levels_to_play):
                    start_props = {"level_id": max_level}
                    if current_time >= parse_datetime("2026-03-01 00:00:00") and random.random() < 0.01:
                        start_props["level_id"] = str(max_level)
                    events.append(create_event("level_start", start_props, random.randint(5, 30)))
                    
                    # Pass or fail?
                    # Harder levels have lower pass rate
                    pass_rate = max(0.2, 0.9 - (max_level * 0.02))
                    passed = random.random() < pass_rate
                    
                    duration = random.randint(30, 180)
                    
                    props = {"level_id": max_level, "duration": duration}
                    
                    # Additive Schema Evolution starting 2026-02-01
                    if current_time >= parse_datetime("2026-02-01 00:00:00"):
                        props["difficulty"] = random.choice(["easy", "normal", "hard"])
                        props["game_mode"] = random.choice(["casual", "ranked", "tournament"])
                        
                    # Type drift starting 2026-03-01: level_id occasionally becomes string
                    if current_time >= parse_datetime("2026-03-01 00:00:00"):
                        if random.random() < 0.01: # 1% type drift
                            props["level_id"] = str(props["level_id"])
                            
                    if passed:
                        events.append(create_event("level_complete", props, duration))
                        if isinstance(props["level_id"], int):
                            max_level += 1
                        else:
                            max_level += 1 # it's string, but logic wise player still advanced
                    else:
                        events.append(create_event("level_fail", props, duration))
                        
                events.append(create_event("session_end", {}, random.randint(5, 15)))

    # Sort chronologically
    events.sort(key=lambda x: x["event_time"])
    return events
