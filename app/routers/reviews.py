from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.data import get_best_reviews, get_reviews_by_plant_id
from app.models import ReviewOut

router = APIRouter()


@router.get("", response_model=list[ReviewOut])
def list_best_reviews(db: Session = Depends(get_db)):
    return [ReviewOut.model_validate(r) for r in get_best_reviews(db)]


@router.get("/plant/{plant_id}", response_model=list[ReviewOut])
def list_plant_reviews(plant_id: int, db: Session = Depends(get_db)):
    reviews = get_reviews_by_plant_id(db, plant_id)
    return [ReviewOut.model_validate(r) for r in reviews]
