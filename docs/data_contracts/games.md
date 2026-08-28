# Dataset: games

## Overview
Internal reference data for the game portfolio.

## Source System
Oracle Operational DB (GAME_MASTER)

## Business Purpose
Provide metadata for games.

## Grain
One row per game.

## Keys
- Primary Key: `game_id`

## Delivery Pattern
JDBC snapshot/incremental.

## Mutability
Mutable (low frequency, e.g. status changes).

## Schema

| Column | Type | Nullable | Description |
|---|---|---|---|
| `game_id` | STRING | No | |
| `game_name` | STRING | No | |
| `genre` | STRING | No | |
| `publisher` | STRING | No | |
| `monetization_model` | STRING | No | |
| `release_date` | DATE | No | |
| `lifecycle_stage` | STRING | No | GROWTH, MATURE, SOFT_LAUNCH |
| `status` | STRING | No | ACTIVE, DEPRECATED |
| `created_at` | TIMESTAMP | No | |
| `updated_at` | TIMESTAMP | No | |

## Business Rules
- Used as dimension table.

## Data Quality Expectations
- `game_id`, `game_name` not null.

## Known Data Issues
None specific.

## PII / Sensitive Data
None.

## Example Record
```text
GAME001, Merge Kingdom, Casual Merge, NovaPlay Games, HYBRID, 2024-03-01, MATURE, ACTIVE, 2024-02-01T00:00:00Z, 2024-02-01T00:00:00Z
```

## Downstream Usage
All domains (filtering/grouping by game attributes).
