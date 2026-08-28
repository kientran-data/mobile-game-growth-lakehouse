# Dataset: iap_purchases

## Overview
In-App Purchase transactions.

## Source System
App Store / Google Play transaction feed

## Business Purpose
Track IAP revenue and payer conversion.

## Grain
One row per purchase transaction.

## Keys
- Primary Key: `transaction_id`

## Delivery Pattern
Hourly incremental JSON files.

## Mutability
Mutable (Transactions can transition from `completed` to `refunded`/`cancelled`).

## Schema

| Column               | Type      | Nullable | Description |
| -------------------- | --------- | -------: | --- |
| `transaction_id`     | STRING    |       No | |
| `player_id`          | STRING    |       No | |
| `game_id`            | STRING    |       No | |
| `product_id`         | STRING    |       No | |
| `purchase_time`      | TIMESTAMP |       No | |
| `platform`           | STRING    |       No | |
| `country`            | STRING    |      Yes | |
| `currency`           | STRING    |       No | |
| `gross_price`        | DECIMAL   |       No | |
| `price_usd`          | DECIMAL   |      Yes | |
| `transaction_status` | STRING    |       No | completed, refunded, cancelled |

## Business Rules
- Refunds are kept in the dataset to calculate gross vs net recognized revenue later.

## Data Quality Expectations
- `transaction_id` not null
- `gross_price >= 0`
- `currency` valid
- `transaction_status` valid

## Known Data Issues
DQ011, DQ012

## PII / Sensitive Data
- `gross_price`, `price_usd` (Financial)
- `player_id` (Internal)

## Example Record
```json
{
  "transaction_id": "TXN_554433",
  "player_id": "PLY_000042",
  "game_id": "GAME_ZOMBIE_RUSH",
  "product_id": "remove_ads_pack",
  "purchase_time": "2026-03-18T10:00:00Z",
  "platform": "android",
  "country": "US",
  "currency": "USD",
  "gross_price": 2.99,
  "price_usd": 2.99,
  "transaction_status": "completed"
}
```

## Downstream Usage
Monetization, LTV, ROAS
