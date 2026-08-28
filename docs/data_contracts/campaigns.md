# Dataset: campaigns

## Overview
Marketing platform campaign metadata.

## Source System
Marketing Platform

## Business Purpose
Provide campaign context and history for UA analysis.

## Grain
One row represents the current source state/version of one marketing campaign.

## Keys
- Business Key: `ad_platform` + `campaign_id`

## Delivery Pattern
Hourly/Daily JSON/CSV.

## Mutability
Mutable (Changes to budget, status, name, etc.). Supports SCD Type 2 downstream.

## Schema

| Column          | Type      | Nullable | Description |
| --------------- | --------- | -------: | --- |
| `ad_platform`   | STRING    | No | |
| `campaign_id`   | STRING    | No | |
| `campaign_name` | STRING    | No | |
| `game_id`       | STRING    | No | |
| `country_group` | STRING    | Yes | |
| `platform`      | STRING    | No | |
| `objective`     | STRING    | Yes | |
| `daily_budget`  | DECIMAL   | Yes | Mutable |
| `status`        | STRING    | No  | Mutable |
| `start_date`    | DATE      | Yes | |
| `end_date`      | DATE      | Yes | Mutable |
| `updated_at`    | TIMESTAMP | No  | |

## Business Rules
- Campaign IDs can overlap across different ad platforms.
- Mutable fields require SCD Type 2 tracking in the data warehouse.

## Data Quality Expectations
- `ad_platform`, `campaign_id` not null.

## Known Data Issues
None specific.

## PII / Sensitive Data
- `daily_budget` (Financial)

## Example Record
```json
{
  "ad_platform": "META_ADS",
  "campaign_id": "C100",
  "campaign_name": "US Android Scale",
  "game_id": "GAME_ZOMBIE_RUSH",
  "country_group": "US",
  "platform": "android",
  "objective": "INSTALL",
  "daily_budget": 10000.0,
  "status": "ACTIVE",
  "start_date": "2026-01-01",
  "end_date": null,
  "updated_at": "2026-01-01T00:00:00Z"
}
```

## Downstream Usage
UA Performance, ROAS, Campaign Analysis.
