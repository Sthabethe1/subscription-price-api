from datetime import date
from sqlalchemy import String, Integer, Float, Date, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base


class Country(Base):
    __tablename__ = "countries"
    iso: Mapped[str] = mapped_column(String(2), primary_key=True)
    name: Mapped[str] = mapped_column(String(80))
    region: Mapped[str | None] = mapped_column(String(40))
    currency: Mapped[str | None] = mapped_column(String(3))
    services_compared: Mapped[int | None] = mapped_column(Integer)
    median_price_vs_us_pct: Mapped[float | None] = mapped_column(Float)
    share_cheaper_than_us_pct: Mapped[float | None] = mapped_column(Float)
    page: Mapped[str | None] = mapped_column(String(200))


class Service(Base):
    __tablename__ = "services"
    slug: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    category: Mapped[str] = mapped_column(String(30), index=True)
    plan: Mapped[str | None] = mapped_column(String(100))
    store: Mapped[str | None] = mapped_column(String(30))
    billing_period: Mapped[str | None] = mapped_column(String(20))
    countries_count: Mapped[int | None] = mapped_column(Integer)
    us_price_usd: Mapped[float | None] = mapped_column(Float)
    cheapest_country: Mapped[str | None] = mapped_column(ForeignKey("countries.iso"))
    cheapest_price_usd: Mapped[float | None] = mapped_column(Float)
    cheapest_local_price: Mapped[str | None] = mapped_column(String(40))
    most_expensive_country: Mapped[str | None] = mapped_column(ForeignKey("countries.iso"))
    most_expensive_price_usd: Mapped[float | None] = mapped_column(Float)
    max_min_ratio: Mapped[float | None] = mapped_column(Float, index=True)
    cheapest_vs_us_pct: Mapped[float | None] = mapped_column(Float)
    yearly_saving_vs_us_usd: Mapped[float | None] = mapped_column(Float)
    last_verified: Mapped[date | None] = mapped_column(Date)
    page: Mapped[str | None] = mapped_column(String(200))


class CategoryCountryMedian(Base):
    __tablename__ = "category_country_medians"
    category: Mapped[str] = mapped_column(String(30), primary_key=True)
    country: Mapped[str] = mapped_column(ForeignKey("countries.iso"), primary_key=True)
    median_price_vs_us_pct: Mapped[float | None] = mapped_column(Float)
