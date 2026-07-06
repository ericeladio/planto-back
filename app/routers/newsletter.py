from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.database import get_db
from app.email_service import subscribe_newsletter

router = APIRouter()


class SubscribeRequest(BaseModel):
    email: EmailStr


@router.post("/subscribe")
def subscribe(req: SubscribeRequest, db: Session = Depends(get_db)):
    ok = subscribe_newsletter(req.email, db)
    if not ok:
        raise HTTPException(status_code=500, detail="Failed to subscribe")
    return {"message": "Subscribed successfully"}
