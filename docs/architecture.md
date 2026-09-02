# Architecture

## Logical Architecture

```text
Synthetic Data Sources
        ↓
CSV / JSON / Parquet
        ↓
Landing Zone
        ↓
Auto Loader
        ↓
Bronze Delta
        ↓
Silver
Clean / Normalize / Dedup / DQ
        ↓
Gold
Fact / Dimension / Marts
        ↓
DAU / Retention / ARPDAU / LTV / ROAS
```
