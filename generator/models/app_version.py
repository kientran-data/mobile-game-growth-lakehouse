"""Data models for AppVersion master data."""

from dataclasses import dataclass

@dataclass
class AppVersion:
    game_id: str
    platform: str
    version: str
    release_date: str
    release_timestamp: str
    minimum_supported_version: str
    status: str
    created_at: str
    updated_at: str
    is_bad_release: bool = False  # Internal flag to drive poor behavior downstream

    def to_dict(self):
        """Serialize to dictionary for CSV/JSON writing."""
        return {
            "game_id": self.game_id,
            "platform": self.platform,
            "version": self.version,
            "release_date": self.release_date,
            "release_timestamp": self.release_timestamp,
            "minimum_supported_version": self.minimum_supported_version,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
