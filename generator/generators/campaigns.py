"""Generator for Campaign master data with SCD Type 2 history."""

import random
from generator.models.campaign import Campaign
from generator.models.game import Game
from generator.config import PROJECT_CONFIG
from generator.utils.dates import parse_date, add_days
from generator.utils.ids import generate_campaign_id

def generate_campaigns(games: list[Game]) -> list[Campaign]:
    """Generate campaigns and their historical changes."""
    campaigns = []
    
    start_date = parse_date(PROJECT_CONFIG["start_date"])
    end_date = parse_date(PROJECT_CONFIG["end_date"])
    countries = PROJECT_CONFIG["countries"]
    platforms = PROJECT_CONFIG["platforms"]
    
    ad_platforms = ["META_ADS", "GOOGLE_ADS", "TIKTOK_ADS"]
    
    seq = 1
    for game in games:
        for country in countries:
            for platform in platforms:
                for ad_platform in ad_platforms:
                    camp_id = generate_campaign_id(ad_platform, game.game_id, country, platform, seq)
                    seq += 1
                    
                    camp_start = max(start_date, game.release_date)
                    
                    if camp_start > end_date:
                        continue
                        
                    # Initial state
                    daily_budget = float(random.choice([100, 500, 1000, 5000]))
                    
                    campaigns.append(Campaign(
                        ad_platform=ad_platform,
                        campaign_id=camp_id,
                        campaign_name=f"{country} {platform.capitalize()} Scale",
                        game_id=game.game_id,
                        country_group=country,
                        platform=platform,
                        objective="INSTALL",
                        daily_budget=daily_budget,
                        status="ACTIVE",
                        start_date=camp_start.isoformat(),
                        end_date=None,
                        updated_at=camp_start.isoformat() + "T00:00:00Z"
                    ))
                    
                    # Simulate SCD2 changes over time
                    current_date = add_days(camp_start, random.randint(15, 45))
                    
                    while current_date < end_date:
                        # Close the previous record
                        campaigns[-1].end_date = current_date.isoformat()
                        
                        # Change budget or status
                        if random.random() < 0.2:
                            status = "PAUSED"
                        else:
                            status = "ACTIVE"
                            daily_budget = daily_budget * random.choice([0.8, 1.2, 1.5])
                            
                        campaigns.append(Campaign(
                            ad_platform=ad_platform,
                            campaign_id=camp_id,
                            campaign_name=f"{country} {platform.capitalize()} Scale",
                            game_id=game.game_id,
                            country_group=country,
                            platform=platform,
                            objective="INSTALL",
                            daily_budget=daily_budget,
                            status=status,
                            start_date=current_date.isoformat(),
                            end_date=None,
                            updated_at=current_date.isoformat() + "T00:00:00Z"
                        ))
                        
                        if status == "PAUSED":
                            break
                            
                        current_date = add_days(current_date, random.randint(15, 45))
                        
    return campaigns
