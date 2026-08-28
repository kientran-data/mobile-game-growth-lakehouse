# Dataset: ua_spend

## Overview
Aggregated advertising spend from UA platforms.

## Source System
Meta/Google/TikTok-like (Ad Platforms)

## Business Purpose
Measure acquisition cost (CPI, ROAS).

## Grain
One row per `date + source + game + campaign + country + platform`.

## Keys
- Business Key: `report_date` + `ad_platform` + `game_id` + `campaign_id` + `country` + `platform`

## Delivery Pattern
Daily CSV reports.

## Mutability
Mutable (Daily advertising reports can change after the first day due to reporting finalization/correction).

## Schema

| Column              | Type      | Nullable | Description |
| ------------------- | --------- | -------: | --- |
| `report_date`       | DATE      |       No | |
| `ad_platform`       | STRING    |       No | |
| `game_id`           | STRING    |       No | |
| `campaign_id`       | STRING    |       No | |
| `campaign_name`     | STRING    |       No | |
| `country`           | STRING    |       No | |
| `platform`          | STRING    |       No | |
| `currency`          | STRING    |       No | |
| `spend`             | DECIMAL   |       No | |
| `impressions`       | BIGINT    |       No | |
| `clicks`            | BIGINT    |       No | |
| `reported_installs` | BIGINT    |      Yes | Platform-reported installs (may differ from attribution) |
| `source_updated_at` | TIMESTAMP |       No | |

## Business Rules
- `reported_installs` is specific to the marketing platform, may not match attribution platform.

## Data Quality Expectations
- `spend >= 0`
- `impressions >= 0`
- `clicks >= 0`
- `clicks <= impressions`
- `ad_platform IN ('META_ADS', 'GOOGLE_ADS', 'TIKTOK_ADS')`

## Known Data Issues
DQ007, DQ010

## PII / Sensitive Data
- `spend` (Financial)

## Example Record
```text
report_date:      2026-03-15
ad_platform:      META_ADS
game_id:          GAME_ZOMBIE_RUSH
campaign_id:      CMP_META_001
country:          US
platform:         android
spend:            1240.50
impressions:      125000
clicks:           4800
reported_installs: 920
```

## Downstream Usage
CPI, ROAS
