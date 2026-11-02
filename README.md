# Subscription Price Gaps – API + Dashboard

PostgreSQL + FastAPI + a Chart.js dashboard, built on the Kaggle dataset
*Subscription Price Gaps by Country* (CC BY 4.0, derived from OpenTheRank / SubPriced).

## Run
    docker compose up --build
- Dashboard: http://localhost:8000
- Interactive API docs: http://localhost:8000/docs

On first start the API creates the tables and loads the CSVs in `data/`.

## Schema
- `countries(iso PK, name, region, currency, services_compared, median_price_vs_us_pct, share_cheaper_than_us_pct, page)`
- `services(slug PK, name, category, plan, store, billing_period, ..., cheapest_country FK, most_expensive_country FK, max_min_ratio, ...)`
- `category_country_medians(category, country) PK, median_price_vs_us_pct)`  (matrix CSV unpivoted)

## Endpoints
| Method | Path | Notes |
|---|---|---|
| GET | /api/services | `q`, `category`, `sort`, `order`, `limit`, `offset` |
| GET/PATCH/DELETE | /api/services/{slug} | |
| POST | /api/services | create |
| GET | /api/countries, /api/countries/{iso} | |
| GET | /api/categories/matrix | category × country medians |
| GET | /api/stats/summary, /by-category, /extremes | dashboard data |

## Attribution
Data: Global App Store Price Index by OpenTheRank (CC BY 4.0), derived dataset by SubPriced (subpriced.com).
