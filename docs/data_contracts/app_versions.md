# Dataset: app_versions

## Overview
Metadata for app version releases.

## Source System
Oracle Operational DB (APP_VERSION)

## Business Purpose
Correlate app updates with engagement/monetization changes.

## Grain
One row per `game + platform + app version`.

## Keys
- Business Key: `game_id` + `platform` + `version`

## Delivery Pattern
JDBC incremental.

## Mutability
Mutable (Status can change).

## Schema

| Column | Type | Nullable | Description |
|---|---|---|---|
| `game_id` | STRING | No | |
| `platform` | STRING | No | |
| `version` | STRING | No | |
| `release_date` | DATE | No | |
| `release_timestamp` | TIMESTAMP | Yes | |
| `minimum_supported_version` | STRING | Yes | |
| `status` | STRING | No | ACTIVE, DEPRECATED, ROLLED_BACK |
| `created_at` | TIMESTAMP | No | |
| `updated_at` | TIMESTAMP | No | |

## Business Rules
- Essential for version performance analysis (e.g. did D1 retention drop after 1.7.0).

## Data Quality Expectations
- `game_id`, `platform`, `version` not null.

## Known Data Issues
None specific.

## PII / Sensitive Data
None.

## Example Record
```text
GAME002, android, 1.7.0, 2026-04-10, 2026-04-10T08:00:00Z, 1.5.0, ACTIVE, 2026-04-09T00:00:00Z, 2026-04-09T00:00:00Z
```

## Downstream Usage
Version Performance Analysis.
