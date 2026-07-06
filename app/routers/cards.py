import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.db_models import SavedCard
from app.models import SavedCardOut, SaveCardRequest

router = APIRouter()


def _detect_brand(card_number: str) -> str:
    if card_number.startswith("4"):
        return "Visa"
    if card_number.startswith("5") or card_number.startswith("2"):
        return "Mastercard"
    return "Unknown"


@router.get("", response_model=list[SavedCardOut])
def list_cards(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cards = db.query(SavedCard).filter(SavedCard.user_id == current_user.id).all()
    return cards


@router.post("", response_model=SavedCardOut, status_code=status.HTTP_201_CREATED)
def save_card(
    body: SaveCardRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if body.cvv == "000":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pago rechazado",
        )

    card = SavedCard(
        user_id=current_user.id,
        last_four=body.card_number[-4:],
        exp_month=body.exp_month,
        exp_year=body.exp_year,
        token=f"tok_sim_{secrets.token_hex(8)}",
        brand=_detect_brand(body.card_number),
    )
    db.add(card)
    db.commit()
    db.refresh(card)
    return card


@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card(
    card_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    card = (
        db.query(SavedCard)
        .filter(SavedCard.id == card_id, SavedCard.user_id == current_user.id)
        .first()
    )
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found",
        )
    db.delete(card)
    db.commit()
