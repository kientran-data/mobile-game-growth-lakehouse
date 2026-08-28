"""Configuration settings for the synthetic data generator."""

SCALE_CONFIGS = {
    "small": {
        "players": 1_000,
    },
    "medium": {
        "players": 10_000,
    },
    "portfolio": {
        "players": 100_000,
    },
}

PROJECT_CONFIG = {
    "seed": 42,
    "start_date": "2026-01-01",
    "end_date": "2026-06-30",
    "countries": [
        "US", "GB", "CA",
        "VN", "TH", "ID",
        "BR", "MX",
    ],
    "platforms": [
        "android",
        "ios",
    ],
}
