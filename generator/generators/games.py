"""Generator for master games data."""

from datetime import date
from generator.models.game import Game

def generate_games() -> list[Game]:
    """Return the predefined list of master games."""
    return [
        Game(
            game_id="GAME_MERGE_KINGDOM",
            game_name="Merge Kingdom",
            genre="CASUAL_MERGE",
            monetization_model="HYBRID",
            lifecycle_stage="MATURE",
            release_date=date(2024, 3, 1),
            publisher="NovaPlay Games",
            status="ACTIVE",
            created_at="2024-02-01T00:00:00Z",
            updated_at="2024-02-01T00:00:00Z"
        ),
        Game(
            game_id="GAME_ZOMBIE_RUSH",
            game_name="Zombie Rush",
            genre="HYBRID_CASUAL",
            monetization_model="ADS_HEAVY_IAP",
            lifecycle_stage="GROWTH",
            release_date=date(2025, 6, 15),
            publisher="NovaPlay Games",
            status="ACTIVE",
            created_at="2025-05-15T00:00:00Z",
            updated_at="2025-05-15T00:00:00Z"
        ),
        Game(
            game_id="GAME_PUZZLE_QUEST",
            game_name="Puzzle Quest",
            genre="PUZZLE",
            monetization_model="ADS_HEAVY",
            lifecycle_stage="SOFT_LAUNCH",
            release_date=date(2025, 11, 20),
            publisher="NovaPlay Games",
            status="ACTIVE",
            created_at="2025-10-20T00:00:00Z",
            updated_at="2025-10-20T00:00:00Z"
        )
    ]
