"""Date and time utilities for the generator."""

from datetime import datetime, date, timedelta

def parse_date(date_str: str) -> date:
    return datetime.strptime(date_str, "%Y-%m-%d").date()

def parse_datetime(dt_str: str) -> datetime:
    if "T" in dt_str:
        return datetime.fromisoformat(dt_str.replace("Z", "+00:00")).replace(tzinfo=None)
    return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")

def format_timestamp(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def add_days(base_date: date, days: int) -> date:
    return base_date + timedelta(days=days)
