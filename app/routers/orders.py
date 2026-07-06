from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.data import create_order, get_cart_items, get_user_orders
from app.dependencies import get_current_user
from app.db_models import SavedCard
from app.email_service import send_order_confirmation_email
from app.models import CartItemOut, OrderOut, PlaceOrderRequest

router = APIRouter()


@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def place_order(
    body: PlaceOrderRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if body.type == "saved":
        if body.cvv == "000":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pago rechazado",
            )
        card = (
            db.query(SavedCard)
            .filter(SavedCard.id == body.card_id, SavedCard.user_id == current_user.id)
            .first()
        )
        if not card:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Card not found",
            )
    else:
        if body.cvv == "000":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pago rechazado",
            )

    cart_items = get_cart_items(db, current_user.id)
    if not cart_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty",
        )

    order = create_order(db, current_user.id)

    items_data = [
        {"plant_name": oi.plant_name, "quantity": oi.quantity}
        for oi in order.items
    ]
    send_order_confirmation_email(
        to=current_user.email,
        name=current_user.full_name or current_user.email,
        order_id=order.id,
        total=order.total,
        items=items_data,
    )

    return OrderOut(
        id=order.id,
        status=order.status,
        total=order.total,
        items=[
            CartItemOut(
                id=oi.id,
                plant_id=oi.plant_id,
                plant_name=oi.plant_name,
                plant_price=oi.plant_price,
                plant_image=oi.plant_image,
                quantity=oi.quantity,
            )
            for oi in order.items
        ],
        created_at=order.created_at.isoformat(),
    )


@router.get("", response_model=list[OrderOut])
def list_orders(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    orders = get_user_orders(db, current_user.id)
    return [
        OrderOut(
            id=o.id,
            status=o.status,
            total=o.total,
            items=[
                CartItemOut(
                    id=oi.id,
                    plant_id=oi.plant_id,
                    plant_name=oi.plant_name,
                    plant_price=oi.plant_price,
                    plant_image=oi.plant_image,
                    quantity=oi.quantity,
                )
                for oi in o.items
            ],
            created_at=o.created_at.isoformat(),
        )
        for o in orders
    ]
