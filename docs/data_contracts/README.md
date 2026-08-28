# Source Data Contracts

## Source System Overview

There are 7 source groups but practically 8 datasets:

| Domain | Dataset | Simulated Source | Delivery |
| --- | --- | --- | --- |
| Product Analytics | `game_events` | Game SDK | Near-real-time files |
| Attribution | `installs` | AppsFlyer-like | Hourly |
| User Acquisition | `ua_spend` | Meta/Google/TikTok-like | Daily |
| Ad Monetization | `ad_impressions` | Mediation SDK | Near-real-time |
| IAP | `iap_purchases` | App Store / Play Store-like | Incremental |
| Reference | `games` | Internal Game Management | Snapshot |
| Reference | `app_versions` | Release Management | Incremental |
| Marketing Metadata | `campaigns` | Marketing Platform | Mutable |

## Dataset Inventory
- `game_events`
- `installs`
- `ua_spend`
- `ad_impressions`
- `iap_purchases`
- `games`
- `app_versions`
- `campaigns`

## Source Relationships

```text
                        games
                          │
                  ┌───────┼────────┐
                  │       │        │
             app_versions │     campaigns
                  │       │        │
                  │       │        │
                  ▼       ▼        ▼
              game_events installs ua_spend
                  │         │
                  │         │
                  └────┬────┘
                       │
                    player
                       │
             ┌─────────┴──────────┐
             │                    │
             ▼                    ▼
      ad_impressions        iap_purchases
```

## Delivery Patterns

| Dataset        | Format   | Frequency       | Pattern                 |
| -------------- | -------- | --------------- | ----------------------- |
| game_events    | JSON     | 5-15 min        | Incremental             |
| installs       | JSON     | Hourly          | Incremental/Corrections |
| ua_spend       | CSV      | Daily           | Daily report            |
| ad_impressions | JSON     | 5-15 min        | Incremental             |
| iap_purchases  | JSON     | Hourly          | Incremental/updates     |
| games          | CSV      | Daily/On change | Snapshot                |
| app_versions   | CSV/JSON | On release      | Incremental             |
| campaigns      | JSON/CSV | Hourly/Daily    | Mutable snapshot/change |

## Mutability Matrix

| Dataset          | Append-only | Historical Update |  Delete/Cancel |
| ---------------- | ----------: | ----------------: | -------------: |
| `game_events`    |           ✅ |                 ❌ |              ❌ |
| `installs`       |           ❌ |                 ✅ |           Rare |
| `ua_spend`       |           ❌ |                 ✅ |              ❌ |
| `ad_impressions` |           ✅ |                 ❌ |              ❌ |
| `iap_purchases`  |           ❌ |                 ✅ |  Refund/cancel |
| `games`          |           ❌ |                 ✅ |    Soft status |
| `app_versions`   |           ❌ |                 ✅ | Status changes |
| `campaigns`      |           ❌ |                 ✅ |      Pause/end |

## Timestamp Standards

All business timestamps are UTC unless explicitly documented otherwise.

- **event_timestamp**: When the business action actually occurred on the client.
- **source_updated_at**: When the source record was updated.
- **_ingested_at**: When the Data Platform received the data (added at Bronze layer).

## Identifier Strategy

- **player_id**: Used in `game_events`, `installs`, `ad_impressions`, `iap_purchases`.
- **game_id**: Used in almost all datasets.
- **campaign**: Uses `ad_platform` + `campaign_id` across `installs`, `ua_spend`, `campaigns`.
- **app_version**: Uses `game_id` + `platform` + `app_version` across `game_events`, `ad_impressions`, `app_versions`.

## PII Classification

| Field                     | Classification       |
| ------------------------- | -------------------- |
| `player_id`               | Internal Identifier  |
| `device_id`               | Sensitive Identifier |
| `advertising_id`          | Sensitive Identifier |
| `country`                 | General              |
| `campaign_id`             | Business             |
| `revenue`                 | Financial/Commercial |
| `spend`                   | Financial/Commercial |

## Common Enumerations

**Platform:** `android`, `ios`
**Country:** `US`, `GB`, `CA`, `VN`, `TH`, `ID`, `BR`, `MX`
**Ad Platform:** `META_ADS`, `GOOGLE_ADS`, `TIKTOK_ADS`
**Lifecycle:** `SOFT_LAUNCH`, `GROWTH`, `MATURE`
**Campaign Status:** `ACTIVE`, `PAUSED`, `ENDED`

## Known Data Issues
See [known_data_issues.md](known_data_issues.md).

## Downstream KPI Coverage

| Source Dataset | Downstream Business Domain        |
| -------------- | --------------------------------- |
| game_events    | Engagement, Retention, Funnel     |
| installs       | Acquisition, Retention, LTV, ROAS |
| ua_spend       | CPI, ROAS                         |
| ad_impressions | Monetization, LTV                 |
| iap_purchases  | Monetization, LTV                 |
| games          | All                               |
| app_versions   | Version Performance               |
| campaigns      | UA Performance, ROAS              |
