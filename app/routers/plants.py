from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.data import get_plant_by_slug, get_plants, get_new_arrivals, get_top_selling_plants, get_trending_plants
from app.models import PlantListResponse, PlantOut

router = APIRouter()


@router.get("", response_model=PlantListResponse)
def list_plants(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    sort: Optional[str] = Query(None),
    page: Optional[int] = Query(None, ge=1),
    per_page: Optional[int] = Query(None, ge=1, le=50),
    db: Session = Depends(get_db),
):
    if page is None:
        page = 1
    if per_page is None:
        per_page = 20

    items, total, pages = get_plants(db, search, category, sort, page, per_page)

    return PlantListResponse(
        items=[PlantOut.model_validate(p) for p in items],
        total=total,
        page=page,
        per_page=per_page,
        pages=pages,
    )


@router.get("/trending", response_model=list[PlantOut])
def list_trending(db: Session = Depends(get_db)):
    return [PlantOut.model_validate(p) for p in get_trending_plants(db)]


@router.get("/new-arrivals", response_model=list[PlantOut])
def list_new_arrivals(db: Session = Depends(get_db)):
    return [PlantOut.model_validate(p) for p in get_new_arrivals(db)]


@router.get("/top-selling", response_model=list[PlantOut])
def list_top_selling(db: Session = Depends(get_db)):
    return [PlantOut.model_validate(p) for p in get_top_selling_plants(db)]


@router.get("/{slug}", response_model=PlantOut)
def get_plant(slug: str, db: Session = Depends(get_db)):
    plant = get_plant_by_slug(db, slug)
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    return PlantOut.model_validate(plant)
