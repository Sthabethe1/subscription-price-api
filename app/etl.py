"""Loads the three Kaggle CSVs into PostgreSQL (only if the DB is empty)."""
from pathlib import Path
import pandas as pd
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from .models import Country, Service, CategoryCountryMedian

DATA = Path(__file__).resolve().parent.parent / "data"


def _clean(df: pd.DataFrame) -> list[dict]:
    return df.astype(object).where(df.notna(), None).to_dict("records")


def load_all(db: Session) -> bool:
    if db.scalar(select(func.count()).select_from(Service)):
        return False

    c = pd.read_csv(DATA / "country_price_index.csv").rename(columns={"country": "iso", "country_name": "name"})
    rows = _clean(c)
    rows.append({"iso": "US", "name": "United States", "region": "North America", "currency": "USD"})
    db.add_all(Country(**r) for r in rows)
    db.flush()

    s = pd.read_csv(DATA / "service_price_gaps.csv").rename(
        columns={"service": "slug", "service_name": "name", "countries": "countries_count"}
    )
    s["last_verified"] = pd.to_datetime(s["last_verified"]).dt.date
    db.add_all(Service(**r) for r in _clean(s))

    m = pd.read_csv(DATA / "category_country_matrix.csv").melt(
        id_vars="category", var_name="country", value_name="median_price_vs_us_pct"
    )
    db.add_all(CategoryCountryMedian(**r) for r in _clean(m))
    db.commit()
    return True
