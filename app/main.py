from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select, func, or_
from sqlalchemy.orm import Session
from . import schemas
from .db import Base, engine, get_db, SessionLocal
from .etl import load_all
from .models import Service, Country, CategoryCountryMedian

STATIC = Path(__file__).parent / "static"
SORTABLE = {"name", "category", "max_min_ratio", "cheapest_vs_us_pct",
            "yearly_saving_vs_us_usd", "us_price_usd", "cheapest_price_usd"}


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        load_all(db)
    yield


app = FastAPI(title="Subscription Price Gaps API", version="1.0.0", lifespan=lifespan)


# ---------- services (full CRUD) ----------
@app.get("/api/services", response_model=schemas.ServicePage, tags=["services"])
def list_services(
    q: str | None = None,
    category: str | None = None,
    sort: str = "max_min_ratio",
    order: str = Query("desc", pattern="^(asc|desc)$"),
    limit: int = Query(25, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    if sort not in SORTABLE:
        raise HTTPException(400, f"sort must be one of {sorted(SORTABLE)}")
    stmt = select(Service)
    if q:
        stmt = stmt.where(or_(Service.name.ilike(f"%{q}%"), Service.slug.ilike(f"%{q}%")))
    if category:
        stmt = stmt.where(Service.category == category)
    total = db.scalar(select(func.count()).select_from(stmt.subquery()))
    col = getattr(Service, sort)
    stmt = stmt.order_by(col.desc().nulls_last() if order == "desc" else col.asc().nulls_last())
    items = db.scalars(stmt.limit(limit).offset(offset)).all()
    return {"total": total, "items": items}


@app.get("/api/services/{slug}", response_model=schemas.ServiceOut, tags=["services"])
def get_service(slug: str, db: Session = Depends(get_db)):
    obj = db.get(Service, slug)
    if not obj:
        raise HTTPException(404, "Service not found")
    return obj


@app.post("/api/services", response_model=schemas.ServiceOut, status_code=201, tags=["services"])
def create_service(body: schemas.ServiceCreate, db: Session = Depends(get_db)):
    if db.get(Service, body.slug):
        raise HTTPException(409, "Slug already exists")
    obj = Service(**body.model_dump())
    db.add(obj)
    db.commit()
    return obj


@app.patch("/api/services/{slug}", response_model=schemas.ServiceOut, tags=["services"])
def update_service(slug: str, body: schemas.ServiceUpdate, db: Session = Depends(get_db)):
    obj = db.get(Service, slug)
    if not obj:
        raise HTTPException(404, "Service not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    return obj


@app.delete("/api/services/{slug}", status_code=204, tags=["services"])
def delete_service(slug: str, db: Session = Depends(get_db)):
    obj = db.get(Service, slug)
    if not obj:
        raise HTTPException(404, "Service not found")
    db.delete(obj)
    db.commit()


# ---------- countries & categories ----------
@app.get("/api/countries", response_model=list[schemas.CountryOut], tags=["countries"])
def list_countries(db: Session = Depends(get_db)):
    return db.scalars(select(Country).order_by(Country.median_price_vs_us_pct.asc().nulls_last())).all()


@app.get("/api/countries/{iso}", response_model=schemas.CountryOut, tags=["countries"])
def get_country(iso: str, db: Session = Depends(get_db)):
    obj = db.get(Country, iso.upper())
    if not obj:
        raise HTTPException(404, "Country not found")
    return obj


@app.get("/api/categories/matrix", tags=["categories"])
def category_matrix(db: Session = Depends(get_db)):
    rows = db.scalars(select(CategoryCountryMedian)).all()
    out: dict[str, dict[str, float | None]] = {}
    for r in rows:
        out.setdefault(r.category, {})[r.country] = r.median_price_vs_us_pct
    return out


# ---------- stats for the dashboard ----------
@app.get("/api/stats/summary", tags=["stats"])
def summary(db: Session = Depends(get_db)):
    top = db.scalars(select(Service).order_by(Service.max_min_ratio.desc().nulls_last()).limit(1)).first()
    return {
        "services": db.scalar(select(func.count()).select_from(Service)),
        "countries": db.scalar(select(func.count()).select_from(Country).where(Country.iso != "US")),
        "avg_cheapest_vs_us_pct": db.scalar(select(func.avg(Service.cheapest_vs_us_pct))),
        "avg_max_min_ratio": db.scalar(select(func.avg(Service.max_min_ratio))),
        "largest_gap": {"name": top.name, "ratio": top.max_min_ratio} if top else None,
    }


@app.get("/api/stats/by-category", tags=["stats"])
def by_category(db: Session = Depends(get_db)):
    rows = db.execute(
        select(Service.category, func.count(), func.avg(Service.max_min_ratio),
               func.avg(Service.cheapest_vs_us_pct)).group_by(Service.category)
    ).all()
    return [{"category": c, "services": n, "avg_ratio": r, "avg_cheapest_vs_us_pct": p} for c, n, r, p in rows]


@app.get("/api/stats/extremes", tags=["stats"])
def extremes(db: Session = Depends(get_db)):
    """How often each country is the cheapest / most expensive for a service."""
    def count(col):
        rows = db.execute(select(col, func.count()).group_by(col).order_by(func.count().desc())).all()
        return [{"country": c, "services": n} for c, n in rows if c]
    return {"cheapest": count(Service.cheapest_country),
            "most_expensive": count(Service.most_expensive_country)}


# ---------- front end ----------
app.mount("/static", StaticFiles(directory=STATIC), name="static")


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(STATIC / "index.html")
