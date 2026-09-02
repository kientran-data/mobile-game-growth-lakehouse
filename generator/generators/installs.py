"""Generator for player installs."""
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

from generator.models.game import Game
from generator.models.app_version import AppVersion
from generator.models.campaign import Campaign
from generator.config import PROJECT_CONFIG, SCALE_CONFIGS
from generator.utils.dates import parse_date

def generate_installs(games: List[Game], app_versions: List[AppVersion], campaigns: List[Campaign], scale: str = "small") -> List[Dict[str, Any]]:
    """Generate player installs maintaining causal consistency with games, versions, and campaigns."""
    installs = []
    num_players = SCALE_CONFIGS[scale]["players"]
    
    start_date = parse_date(PROJECT_CONFIG["start_date"])
    end_date = parse_date(PROJECT_CONFIG["end_date"])
    
    # Organic vs Paid split
    organic_ratio = 0.4
    
    for _ in range(num_players):
        # 1. Pick a random game
        game = random.choice(games)
        
        # 2. Pick a valid install date
        game_start = max(start_date, game.release_date)
        if game_start > end_date:
            continue
            
        game_active_days = (end_date - game_start).days
        install_date = game_start + timedelta(days=random.randint(0, game_active_days))
        
        # Random hour/min/sec
        install_time = datetime.combine(install_date, datetime.min.time()) + timedelta(seconds=random.randint(0, 86399))
        install_timestamp = install_time.isoformat() + "Z"
        
        # 3. Pick platform and country
        platform = random.choice(PROJECT_CONFIG["platforms"])
        country = random.choice(PROJECT_CONFIG["countries"])
        
        # 4. Marketing attribution (Organic vs Paid)
        is_organic = random.random() < organic_ratio
        campaign_id = None
        media_source = "organic"
        
        if not is_organic:
            # Find active campaigns for this game/platform/country during install date
            valid_campaigns = [
                c for c in campaigns 
                if c.game_id == game.game_id 
                and c.platform == platform 
                and c.country_group == country 
                and parse_date(c.start_date.split('T')[0]) <= install_date
                and (c.end_date is None or parse_date(c.end_date.split('T')[0]) >= install_date)
                and c.status == "ACTIVE"
            ]
            
            if valid_campaigns:
                camp = random.choice(valid_campaigns)
                campaign_id = camp.campaign_id
                media_source = camp.ad_platform.lower()
            else:
                is_organic = True # Fallback to organic if no active campaign exists
                
        # 5. App Version assignment (must be released before install)
        valid_versions = [
            v for v in app_versions
            if v.game_id == game.game_id
            and v.platform == platform
            and parse_date(v.release_date.split('T')[0]) <= install_date
        ]
        
        # Pick the latest valid version
        valid_versions.sort(key=lambda x: parse_date(x.release_date.split('T')[0]), reverse=True)
        app_version = valid_versions[0].version if valid_versions else "1.0.0"
        
        # Deterministic UUID generation using random.getrandbits
        player_hex = f"{random.getrandbits(32):08x}".upper()
        install_hex = f"{random.getrandbits(32):08x}".upper()
        device_hex = f"{random.getrandbits(128):032x}"
        
        player_id = f"PLY_{player_hex}"
        install_id = f"INS_{install_hex}"
        device_id = f"{device_hex[:8]}-{device_hex[8:12]}-{device_hex[12:16]}-{device_hex[16:20]}-{device_hex[20:]}"
        
        installs.append({
            "install_id": install_id,
            "player_id": player_id,
            "game_id": game.game_id,
            "install_time": install_timestamp,
            "platform": platform,
            "country": country,
            "app_version": app_version,
            "media_source": media_source,
            "campaign_id": campaign_id,
            "device_id": device_id,
            "is_organic": is_organic
        })
        
    # Sort chronologically
    installs.sort(key=lambda x: x["install_time"])
    return installs
