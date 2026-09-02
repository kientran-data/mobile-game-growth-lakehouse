"""Generator for ad impressions simulating ad revenue."""
import uuid
import random
from datetime import timedelta
from typing import List, Dict, Any
from generator.utils.dates import parse_datetime

def generate_ad_impressions(installs: List[Dict[str, Any]], game_events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate ad impressions tied to active game sessions."""
    impressions = []
    
    player_install_map = {p["player_id"]: p for p in installs}
    
    # We only care about session_start and level_complete/fail events for showing ads
    ad_opportunities = [evt for evt in game_events if evt["event_name"] in ("session_start", "level_complete", "level_fail")]
    
    ad_networks = ["AdMob", "AppLovin", "Unity Ads", "Mintegral", "Meta Audience Network"]
    ad_formats = ["rewarded", "interstitial", "banner"]
    
    for evt in ad_opportunities:
        player_id = evt["player_id"]
        install = player_install_map.get(player_id)
        if not install:
            continue
            
        evt_time = parse_datetime(evt["event_time"])
        
        # Decide if an ad is shown based on event type
        # E.g. high chance of ad after level complete/fail
        prob = 0.0
        if evt["event_name"] == "session_start":
            prob = 0.1 # app open ad
        elif evt["event_name"] in ("level_complete", "level_fail"):
            prob = 0.7 # interstitial or rewarded
            
        if random.random() < prob:
            network = random.choice(ad_networks)
            
            # Format and revenue logic
            if evt["event_name"] == "session_start":
                format_type = "banner"
                revenue = random.uniform(0.001, 0.005)
            else:
                format_type = random.choices(["rewarded", "interstitial"], weights=[0.4, 0.6])[0]
                revenue = random.uniform(0.01, 0.05) if format_type == "rewarded" else random.uniform(0.005, 0.02)
                
            # Ad happens slightly after the event
            ad_time = evt_time + timedelta(seconds=random.randint(1, 10))
            imp_hex = f"{random.getrandbits(32):08x}".upper()
            
            impressions.append({
                "impression_id": f"IMP_{imp_hex}",
                "player_id": player_id,
                "game_id": evt["game_id"],
                "event_time": ad_time.isoformat() + "Z",
                "session_id": evt["session_id"],
                "ad_network": network,
                "ad_format": format_type,
                "country": install["country"],
                "revenue_usd": round(revenue, 4)
            })
            
    # Sort chronologically
    impressions.sort(key=lambda x: x["event_time"])
    return impressions
