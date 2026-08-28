"""ID generation utilities."""

def generate_campaign_id(ad_platform: str, game_id: str, country_group: str, platform: str, seq: int) -> str:
    """Format: CMP_{PLATFORM}_{GAME_SHORT}_{COUNTRY}_{OS}_{SEQ}"""
    platform_short = ad_platform.split('_')[0]
    game_short = "".join(word[0] for word in game_id.replace("GAME_", "").split("_"))
    return f"CMP_{platform_short}_{game_short}_{country_group}_{platform.upper()}_{seq:03d}"
