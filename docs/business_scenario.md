# Business Scenario

## Company

NovaPlay Games is a fictional mobile game studio that develops and
operates free-to-play mobile games across Android and iOS.

The company generates revenue through advertising and in-app purchases
while acquiring players through both organic traffic and paid User
Acquisition channels.

The purpose of this project is to simulate the data platform of a
mobile game company and build an end-to-end Databricks Lakehouse for
growth, player engagement, retention, monetization and profitability
analytics.

## Game Portfolio

| Game | Genre | Monetization | Platforms | Lifecycle |
|---|---|---|---|---|
| Merge Kingdom | Casual Merge | Ads + IAP | Android / iOS | Mature |
| Zombie Rush | Hybrid Casual | Ads-heavy + IAP | Android / iOS | Growth |
| Puzzle Quest | Puzzle | Ads-heavy | Android / iOS | Soft Launch |

## Markets

The games operate across multiple markets with different acquisition
cost and monetization characteristics.

Initial markets include:

- United States
- United Kingdom
- Canada
- Vietnam
- Thailand
- Indonesia
- Brazil
- Mexico

## User Acquisition

Paid acquisition is simulated across:

- Meta Ads
- Google Ads
- TikTok Ads

Organic installs are also included.

The acquisition hierarchy is:

Channel → Campaign → Ad Set → Creative

## Monetization

The games use two primary monetization models:

1. Advertising revenue
2. In-App Purchase revenue

Advertising formats include:

- Rewarded
- Interstitial
- Banner
- App Open

Simulated advertising sources include:

- AdMob
- AppLovin
- Unity Ads
- Mintegral
- Meta Audience Network

## Business Problem

Operational and analytical data is produced by multiple independent
systems, including game telemetry, mobile attribution, advertising
platforms, ad monetization networks and in-app purchase systems.

These datasets have different grains, schemas, delivery frequencies
and identifiers.

As a result, business teams cannot consistently connect acquisition
cost with player engagement, retention and downstream revenue.

The Data Team needs a governed Lakehouse that provides trusted datasets
for acquisition, player behavior, monetization and profitability
analysis.

## Stakeholders

| Stakeholder | Primary Questions |
|---|---|
| Executive Management | Growth, revenue and profitability |
| User Acquisition | Spend, CPI, player quality, LTV and ROAS |
| Monetization | Ad revenue, IAP revenue and ARPDAU |
| Product | DAU, retention, sessions and version performance |
| Game Design | Progression, level funnel and failure rate |
| Finance | Spend and revenue reconciliation |
| Data Team | Data quality, freshness, lineage and reliability |

## Core Analytical Domains

The platform supports five primary analytical domains:

- Acquisition
- Player Engagement
- Retention
- Monetization
- Profitability

Additional product analytics include gameplay progression, level funnel
and app-version performance.

## Player Lifecycle

Paid / Organic Acquisition
        ↓
      Install
        ↓
    First Open
        ↓
     Tutorial
        ↓
      Player
        ↓
   Engagement
        ↓
 Ads + IAP Revenue
        ↓
    Retention
        ↓
       LTV
        ↓
 Campaign ROAS

## Data Characteristics

The project intentionally includes realistic Data Engineering
challenges such as:

- Incremental file arrival
- Duplicate events
- Late-arriving events
- Schema evolution
- Malformed records
- Attribution corrections
- Mutable campaign metadata
- Data quality violations
- Different source delivery frequencies

## Dataset Period

The initial historical simulation covers:

2026-01-01 → 2026-06-30

Additional incremental data will be generated after the historical
baseline to simulate ongoing production ingestion.

## Scope

The project focuses on the Data Engineering platform rather than
implementing actual mobile game backend systems or external advertising
APIs.

External systems such as AppsFlyer, Meta Ads, Google Ads, TikTok Ads,
AdMob and AppLovin are represented by synthetic source datasets with
realistic business behavior.
