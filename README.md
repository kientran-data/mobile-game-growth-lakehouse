# Mobile Game Growth & Monetization Lakehouse

An end-to-end Databricks Lakehouse project for mobile game analytics,
covering player acquisition, engagement, retention, monetization,
LTV and campaign ROAS.

## Project Goals

Integrated gameplay telemetry, attribution, UA spend, ad monetization, IAP, and master data from multiple file-based and simulated source systems into the Databricks Lakehouse.

Implemented incremental ingestion for continuously arriving file-based datasets using Databricks Auto Loader.

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
CSV / JSON / Parquet
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