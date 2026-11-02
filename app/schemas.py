from datetime import date
from pydantic import BaseModel, ConfigDict


class ServiceBase(BaseModel):
    name: str
    category: str
    plan: str | None = None
    store: str | None = None
    billing_period: str | None = None
    countries_count: int | None = None
    us_price_usd: float | None = None
    cheapest_country: str | None = None
    cheapest_price_usd: float | None = None
    cheapest_local_price: str | None = None
    most_expensive_country: str | None = None
    most_expensive_price_usd: float | None = None
    max_min_ratio: float | None = None
    cheapest_vs_us_pct: float | None = None
    yearly_saving_vs_us_usd: float | None = None
    last_verified: date | None = None
    page: str | None = None


class ServiceCreate(ServiceBase):
    slug: str


class ServiceUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    plan: str | None = None
    us_price_usd: float | None = None
    cheapest_country: str | None = None
    cheapest_price_usd: float | None = None
    most_expensive_country: str | None = None
    most_expensive_price_usd: float | None = None
    max_min_ratio: float | None = None
    cheapest_vs_us_pct: float | None = None


class ServiceOut(ServiceBase):
    model_config = ConfigDict(from_attributes=True)
    slug: str


class ServicePage(BaseModel):
    total: int
    items: list[ServiceOut]


class CountryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    iso: str
    name: str
    region: str | None = None
    currency: str | None = None
    services_compared: int | None = None
    median_price_vs_us_pct: float | None = None
    share_cheaper_than_us_pct: float | None = None
