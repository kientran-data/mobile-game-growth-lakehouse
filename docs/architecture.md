# Architecture

## Logical Architecture (Phase 1)

```text
                         SOURCE SYSTEMS

                ┌───────────────────────────┐
                │                           │
                │      Oracle OLTP          │
                │                           │
                │  GAME_MASTER              │
                │  APP_VERSION              │
                │  IAP_TRANSACTION          │
                │                           │
                └─────────────┬─────────────┘
                              │
                              │ JDBC
                              │ incremental
                              ▼

Game SDK ───────── JSON ─────────────┐
Attribution ────── JSON ─────────────┤
UA Platforms ───── CSV ──────────────┤
Ad Monetization ── JSON ─────────────┤
Campaign Export ── JSON/CSV ─────────┤
                                     │
                                     ▼
                               DATABRICKS
                                     │
                      ┌──────────────┴─────────────┐
                      │                            │
                Auto Loader                  JDBC Ingestion
                      │                            │
                      └──────────────┬─────────────┘
                                     ▼
                               BRONZE DELTA
                                     │
                                     ▼
                             LAKEFLOW PIPELINES
                                     │
                                     ▼
                                  SILVER
                                     │
                  ┌──────────────────┼───────────────────┐
                  │                  │                   │
             Engagement        Acquisition        Monetization
                  │                  │                   │
                  └──────────────────┼───────────────────┘
                                     ▼
                                   GOLD
                                     │
                  ┌──────────────────┼──────────────────┐
                  ▼                  ▼                  ▼
              Retention             LTV               ROAS
              ARPDAU              Funnel         Version Analysis
                                     │
                                     ▼
                              Databricks SQL
```
