# Mobile Game Growth & Monetization Lakehouse

An end-to-end Databricks Lakehouse project for mobile game analytics,
covering player acquisition, engagement, retention, monetization,
LTV and campaign ROAS.

## Project Goals

The project simulates a mobile game company's data platform integrating:

- Gameplay telemetry
- Attribution data
- User Acquisition spend
- Ad monetization
- In-App Purchase revenue
- Game and campaign metadata

The platform will be implemented using:

- Databricks
- Delta Lake
- Auto Loader
- Lakeflow Pipelines
- Lakeflow Jobs
- Unity Catalog
- Databricks SQL

## Architecture

```text
Source Data
    ↓
Landing
    ↓
Auto Loader
    ↓
Bronze Delta
    ↓
Lakeflow Pipelines
    ↓
Silver
    ↓
Gold
    ↓
Databricks SQL