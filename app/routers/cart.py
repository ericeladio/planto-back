from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.data import add_cart_item, clear_cart, get_cart_items, get_plant_by_id
from app.dependencies import get_current_user
from app.models import (
    CartAddRequest,
    CartItemOut,
    CartResponse,
    CartUpdateRequest,
)

router = APIRouter()


def _cart_response(db: Session, user_id: int) -> CartResponse:
    items = get_cart_items(db, user_id)
    total_items = sum(i.quantity for i in items)
    total_price = sum(i.plant.price * i.quantity for i in items)
    return CartResponse(
        items=[
            CartItemOut(
                id=i.id,
                plant_id=i.plant_id,
                plant_name=i.plant.name,
                plant_price=i.plant.price,
                plant_image=i.plant.image_url,
                quantity=i.quantity,
            )
            for i in items
        ],
        total_items=total_items,
        total_price=total_price,
    )


@router.get("", response_model=CartResponse)
def get_cart(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _cart_response(db, current_user.id)


@router.post("", response_model=CartResponse)
def add_to_cart(
    body: CartAddRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    plant = get_plant_by_id(db, body.plant_id)
    if plant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plant not found",
        )

    add_cart_item(db, current_user.id, body.plant_id, body.quantity)
    return _cart_response(db, current_user.id)


@router.patch("/{item_id}", response_model=CartResponse)
def update_cart_item(
    item_id: int,
    body: CartUpdateRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    from app.db_models import CartItem

    item = (
        db.query(CartItem)
        .filter(CartItem.id == item_id, CartItem.user_id == current_user.id)
        .first()
    )
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found",
        )

    item.quantity = body.quantity
    db.commit()
    return _cart_response(db, current_user.id)


@router.delete("/{item_id}", response_model=CartResponse)
def remove_from_cart(
    item_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    from app.db_models import CartItem

    item = (
        db.query(CartItem)
        .filter(CartItem.id == item_id, CartItem.user_id == current_user.id)
        .first()
    )
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found",
        )

    db.delete(item)
    db.commit()
    return _cart_response(db, current_user.id)
