# Architecture

## Logical Architecture (Phase 1)

```text
                         MOBILE GAME SOURCES

     Gameplay     Attribution     UA Spend
        │              │             │
        │              │             │
     Ad Revenue       IAP        Metadata
        │              │             │
        └──────────────┼─────────────┘
                       ▼
                  Landing Zone
                       │
                       ▼
                    Auto Loader
                       │
                       ▼
                    BRONZE
                       │
                       ▼
               Lakeflow Pipelines
                       │
                       ▼
                    SILVER
                       │
           ┌───────────┼───────────┐
           │           │           │
      Acquisition   Player     Monetization
           │           │           │
           └───────────┼───────────┘
                       ▼
                     GOLD
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
    Retention         LTV            ROAS
      Funnel        ARPDAU       UA Performance
        │              │              │
        └──────────────┼──────────────┘
                       ▼
                 Databricks SQL
```
