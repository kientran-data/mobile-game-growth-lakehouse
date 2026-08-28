"""Generator for AppVersion master data."""

from generator.models.app_version import AppVersion
from generator.models.game import Game
from generator.config import PROJECT_CONFIG
from generator.utils.dates import parse_date, add_days

def generate_app_versions(games: list[Game]) -> list[AppVersion]:
    """Generate app versions for all games and platforms."""
    app_versions = []
    
    start_date = parse_date(PROJECT_CONFIG["start_date"])
    platforms = PROJECT_CONFIG["platforms"]
    
    for game in games:
        for platform in platforms:
            current_date = max(start_date, game.release_date)
            major, minor, patch = 1, 0, 0
            
            while current_date <= parse_date(PROJECT_CONFIG["end_date"]):
                version_str = f"{major}.{minor}.{patch}"
                
                # Check for our intentional bad release scenario (Section 3.7 & 3.21)
                is_bad = False
                if game.game_id == "GAME_ZOMBIE_RUSH" and version_str == "1.4.0":
                    is_bad = True
                
                app_version = AppVersion(
                    game_id=game.game_id,
                    platform=platform,
                    version=version_str,
                    release_date=current_date.isoformat(),
                    release_timestamp=current_date.strftime("%Y-%m-%dT08:00:00Z"),
                    minimum_supported_version=f"{major}.{max(0, minor-2)}.0",
                    status="ACTIVE",
                    created_at=current_date.isoformat() + "T00:00:00Z",
                    updated_at=current_date.isoformat() + "T00:00:00Z",
                    is_bad_release=is_bad
                )
                app_versions.append(app_version)
                
                # Advance version and time deterministically
                minor += 1
                current_date = add_days(current_date, 21)
                
    return app_versions
