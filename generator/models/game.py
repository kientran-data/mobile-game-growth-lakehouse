"""Data models for Game master data."""

from dataclasses import dataclass
from datetime import date

@dataclass
class Game:
    game_id: str
    game_name: str
    genre: str
    monetization_model: str
    lifecycle_stage: str
    release_date: date
    publisher: str
    status: str
    created_at: str
    updated_at: str

    def to_dict(self):
        """Serialize to dictionary for CSV/JSON writing."""
        return {
            "game_id": self.game_id,
            "game_name": self.game_name,
            "genre": self.genre,
            "publisher": self.publisher,
            "monetization_model": self.monetization_model,
            "release_date": self.release_date.isoformat(),
            "lifecycle_stage": self.lifecycle_stage,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
