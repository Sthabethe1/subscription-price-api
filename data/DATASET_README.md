# Subscription Price Gaps by Country

**How much does the same subscription cost in 18 countries?** This dataset summarises the price gaps of 146 digital subscriptions (streaming, music, AI assistants, productivity, education, social & dating, mobile games) across 18 countries, compared with the United States.

It is built for quick analysis: one row per service with the cheapest and most expensive country, a country-level price index vs the US, and a category × country matrix.

**Data snapshot:** 30 September 2026 (source version v2026.09.30). New versions of this dataset are added when the source publishes new prices.

## Highlights

- 🎵 **Spotify Individual**: $12.99 in the US vs $1.20 in Nigeria (−91%); the most expensive country (Switzerland, $19.18) costs 16× the cheapest.
- 🤖 **AI assistants barely do regional pricing**: ChatGPT Plus is only 12% cheaper in the cheapest country (Canada) than in the US, and AI subscriptions are *more* expensive than the US in several countries.
- 🌍 **Cheapest countries overall** (median price vs US across all services): Egypt (−56%), Turkey (−49%), Nigeria (−48%).

## Files

### `service_price_gaps.csv` (one row per service)
| Column | Description |
|---|---|
| `service`, `service_name` | Service identifier and name |
| `category` | ai, streaming, productivity, photo-video, education, social, mobile-game |
| `plan`, `store`, `billing_period` | The plan compared (the variant listed in the most countries), its store and billing period |
| `countries` | Number of countries with a price for this plan |
| `us_price_usd` | Price in the United States (USD) |
| `cheapest_country`, `cheapest_price_usd`, `cheapest_local_price` | Cheapest country (ISO code), price in USD and in local currency |
| `most_expensive_country`, `most_expensive_price_usd` | Most expensive country and price in USD |
| `max_min_ratio` | Most expensive price ÷ cheapest price |
| `cheapest_vs_us_pct` | Cheapest price compared with the US price, in % |
| `yearly_saving_vs_us_usd` | Yearly difference between the US price and the cheapest price (monthly and weekly plans) |
| `last_verified` | Most recent verification date of the prices used |
| `page` | Page with the full country-by-country table |

### `country_price_index.csv` (one row per country, US excluded)
| Column | Description |
|---|---|
| `country`, `country_name`, `region`, `currency` | Country information |
| `services_compared` | Services with a price both in this country and in the US |
| `median_price_vs_us_pct` | Median of (country price ÷ US price − 1), in % |
| `share_cheaper_than_us_pct` | Share of services cheaper than in the US, in % |
| `page` | Country page |

### `category_country_matrix.csv`
Median price vs the US (in %) for each category (rows) and country (columns). Negative = cheaper than the US.

## Methodology

- Prices are store prices (mostly Apple App Store, some official websites) converted to USD with the exchange rates of the source snapshot.
- For each service, the comparison uses a single plan, store and billing period: the variant available in the most countries.
- Demo values and prices excluded from the index by the source are removed.
- Prices may include or exclude local taxes depending on the country; availability and payment requirements vary. This dataset describes listed prices only: it is not a guide to buying subscriptions in another country, which many services do not allow.

## Source and license

This dataset is **derived from the [Global App Store Price Index](https://opentherank.com/open-data/app-price-index/) by OpenTheRank (version v2026.09.30), licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)**.

Changes made: selection of one comparable plan per service, calculation of price gaps, ratios, yearly savings, a country price index and a category × country matrix.

This derived dataset is shared under the same license, **CC BY 4.0**. Please credit both the original source and **SubPriced (subpriced.com)**.

## Updates

Interactive tables, a monthly price report and the latest prices: **[subpriced.com](https://subpriced.com)**.
