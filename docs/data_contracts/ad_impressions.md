# Dataset: ad_impressions

## Overview
Monetization events for ads shown to players.

## Source System
Mediation SDK (Mediation / Monetization SDK)

## Business Purpose
Track ad revenue and ARPDAU.

## Grain
One row represents one monetized ad impression shown to one player.

## Keys
- Primary Key: `ad_impression_id`

## Delivery Pattern
Frequent incremental JSON files (5-15 min).

## Mutability
Append-only.

## Schema

| Column               | Type      | Nullable | Description |
| -------------------- | --------- | -------: | --- |
| `ad_impression_id`   | STRING    |       No | |
| `player_id`          | STRING    |       No | |
| `game_id`            | STRING    |       No | |
| `event_time`         | TIMESTAMP |       No | |
| `ad_source`          | STRING    |       No | AdMob, AppLovin, Unity Ads, etc. |
| `ad_unit_id`         | STRING    |       No | |
| `ad_format`          | STRING    |       No | rewarded, interstitial, banner, app_open |
| `country`            | STRING    |      Yes | |
| `platform`           | STRING    |       No | |
| `app_version`        | STRING    |       No | |
| `revenue_usd`        | DECIMAL   |       No | |
| `mediation_platform` | STRING    |       No | Note: mediation_platform != ad_source |

## Business Rules
- `mediation_platform` is the aggregator (e.g., AppLovin MAX), `ad_source` is the actual ad provider (e.g., Mintegral).

## Data Quality Expectations
- `ad_impression_id` not null
- `player_id` not null
- `revenue_usd >= 0` (can be very small like 0.000034)
- `valid ad_format`
- `event_time` not null

## Known Data Issues
DQ009

## PII / Sensitive Data
- `revenue_usd` (Financial)
- `player_id` (Internal)

## Example Record
```json
{
  "ad_impression_id": "IMP_998877",
  "player_id": "PLY_000042",
  "game_id": "GAME_ZOMBIE_RUSH",
  "event_time": "2026-03-18T09:25:00Z",
  "ad_source": "AdMob",
  "ad_unit_id": "UNIT_REW_01",
  "ad_format": "rewarded",
  "country": "US",
  "platform": "android",
  "app_version": "1.4.2",
  "revenue_usd": 0.015,
  "mediation_platform": "AppLovin MAX"
}
```

## Downstream Usage
Monetization, LTV, ROAS
