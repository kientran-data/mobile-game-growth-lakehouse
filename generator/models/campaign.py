"""Data models for Campaign master data (SCD Type 2)."""

from dataclasses import dataclass
from typing import Optional

@dataclass
class Campaign:
    ad_platform: str
    campaign_id: str
    campaign_name: str
    game_id: str
    country_group: str
    platform: str
    objective: str
    daily_budget: float
    status: str
    start_date: str
    end_date: Optional[str]
    updated_at: str

    def to_dict(self):
        """Serialize to dictionary for CSV/JSON writing."""
        return {
            "ad_platform": self.ad_platform,
            "campaign_id": self.campaign_id,
            "campaign_name": self.campaign_name,
            "game_id": self.game_id,
            "country_group": self.country_group,
            "platform": self.platform,
            "objective": self.objective,
            "daily_budget": round(self.daily_budget, 2),
            "status": self.status,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "updated_at": self.updated_at
        }
