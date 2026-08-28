# Dataset: installs

## Overview
Attribution data for player installs.

## Source System
AppsFlyer-like Attribution Platform

## Business Purpose
Determine acquisition channel and campaign for ROI/ROAS calculation.

## Grain
One row represents the latest known attribution state of one install.

## Keys
- Primary Key: `install_id`
- Relation: `install_id` -> `player_id` (1:1 in V1)

## Delivery Pattern
Hourly incremental JSON files.

## Mutability
Mutable (Attribution corrections happen).

## Schema

| Column                   | Type      | Nullable | Description |
| ------------------------ | --------- | -------: | --- |
| `install_id`             | STRING    |       No | |
| `player_id`              | STRING    |       No | |
| `game_id`                | STRING    |       No | |
| `install_time`           | TIMESTAMP |       No | |
| `media_source`           | STRING    |      Yes | |
| `campaign_id`            | STRING    |      Yes | |
| `campaign_name`          | STRING    |      Yes | |
| `adset_id`               | STRING    |      Yes | |
| `adset_name`             | STRING    |      Yes | |
| `creative_id`            | STRING    |      Yes | |
| `creative_name`          | STRING    |      Yes | |
| `country`                | STRING    |      Yes | |
| `platform`               | STRING    |       No | |
| `is_organic`             | BOOLEAN   |       No | |
| `attribution_updated_at` | TIMESTAMP |       No | |

## Business Rules
- Organic rule: If `is_organic = true`, then `media_source`, `campaign`, `adset`, `creative` can be NULL (valid null).
- Paid install: If `is_organic = false`, should ideally have `media_source` and `campaign_id`.

## Data Quality Expectations
- `install_id`, `player_id`, `game_id`, `install_time`, `platform`, `is_organic`, `attribution_updated_at` NOT NULL

## Known Data Issues
DQ006 (Attribution correction)

## PII / Sensitive Data
- `player_id` (Internal)

## Example Record
```json
{
  "install_id": "INS_000042",
  "player_id": "PLY_000042",
  "game_id": "GAME_ZOMBIE_RUSH",
  "install_time": "2026-03-15T12:10:44Z",
  "media_source": "META_ADS",
  "campaign_id": "CMP_META_001",
  "campaign_name": "US_ANDROID_SCALE_01",
  "adset_id": "ADSET_010",
  "creative_id": "CREATIVE_042",
  "country": "US",
  "platform": "android",
  "is_organic": false,
  "attribution_updated_at": "2026-03-15T12:15:00Z"
}
```

## Downstream Usage
Acquisition, Retention, LTV, ROAS
