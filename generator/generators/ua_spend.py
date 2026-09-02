"""Generator for User Acquisition (UA) spend data."""
import random
from collections import defaultdict
from typing import List, Dict, Any
from datetime import timedelta
from generator.models.campaign import Campaign
from generator.utils.dates import parse_date, parse_datetime

def generate_ua_spend(campaigns: List[Campaign], installs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate daily UA spend aggregated per campaign, based roughly on generated installs."""
    ua_spend = []
    
    # Count installs per campaign per day
    installs_by_camp_date = defaultdict(int)
    for ins in installs:
        if not ins["is_organic"] and ins["campaign_id"]:
            date_str = ins["install_time"][:10]
            key = (ins["campaign_id"], date_str)
            installs_by_camp_date[key] += 1
            
    # Group campaigns by ID to handle SCD2 historical states properly
    # We want to iterate day by day for each unique campaign_id
    camp_history = defaultdict(list)
    for c in campaigns:
        camp_history[c.campaign_id].append(c)
        
    for camp_id, states in camp_history.items():
        # Sort states by start_date
        states.sort(key=lambda x: parse_date(x.start_date.split('T')[0]))
        
        # Iterate over all dates this campaign was active
        for state in states:
            if state.status != "ACTIVE":
                continue
                
            start_date = parse_date(state.start_date.split('T')[0])
            # If end_date is None, assume the campaign is active until project end date (e.g. 2026-06-30)
            end_date = parse_date(state.end_date.split('T')[0]) if state.end_date else parse_date("2026-06-30")
            
            # CPI assumption: between $0.50 and $5.00 depending on platform and country
            base_cpi = 1.0
            if state.platform == "ios":
                base_cpi *= 2.5
            if state.country_group in ["US", "GB", "CA"]:
                base_cpi *= 3.0
            
            current_date = start_date
            while current_date <= end_date:
                date_str = current_date.isoformat()
                daily_installs = installs_by_camp_date.get((camp_id, date_str), 0)
                
                # Even if 0 installs, there might be some impressions/clicks and a tiny bit of spend
                impressions = daily_installs * random.randint(100, 300) + random.randint(100, 1000)
                clicks = int(impressions * random.uniform(0.01, 0.05))
                
                if daily_installs > 0:
                    spend = daily_installs * base_cpi * random.uniform(0.8, 1.2)
                else:
                    spend = clicks * random.uniform(0.1, 0.5)
                    
                # Capped by daily budget roughly
                spend = min(spend, state.daily_budget * random.uniform(0.9, 1.1))
                
                ua_spend.append({
                    "date": date_str,
                    "campaign_id": camp_id,
                    "game_id": state.game_id,
                    "media_source": state.ad_platform.lower(),
                    "country": state.country_group,
                    "platform": state.platform,
                    "impressions": impressions,
                    "clicks": clicks,
                    "spend_usd": round(spend, 2)
                })
                
                current_date += timedelta(days=1)
                
    # Sort by date
    ua_spend.sort(key=lambda x: x["date"])
    return ua_spend
