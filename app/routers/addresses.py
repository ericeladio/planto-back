from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.data import (
    get_user_addresses,
    get_address_by_id,
    create_address,
    update_address,
    delete_address,
    set_default_address,
)
from app.dependencies import get_current_user
from app.models import AddressCreate, AddressOut, AddressUpdate

router = APIRouter()


@router.get("", response_model=list[AddressOut])
def list_addresses(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_user_addresses(db, current_user.id)


@router.post("", response_model=AddressOut, status_code=status.HTTP_201_CREATED)
def create_new_address(
    body: AddressCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_address(
        db,
        current_user.id,
        label=body.label,
        street=body.street,
        number=body.number,
        colony=body.colony,
        city=body.city,
        state=body.state,
        zip_code=body.zip_code,
        country=body.country,
        reference=body.reference,
        is_default=body.is_default,
    )


@router.get("/{address_id}", response_model=AddressOut)
def get_address(
    address_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    addr = get_address_by_id(db, address_id, current_user.id)
    if not addr:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found",
        )
    return addr


@router.patch("/{address_id}", response_model=AddressOut)
def update_existing_address(
    address_id: int,
    body: AddressUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    update_data = body.model_dump(exclude_unset=True)
    addr = update_address(db, address_id, current_user.id, **update_data)
    if not addr:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found",
        )
    return addr


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_address(
    address_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    success = delete_address(db, address_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found",
        )


@router.patch("/{address_id}/default", response_model=AddressOut)
def set_address_default(
    address_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    addr = set_default_address(db, address_id, current_user.id)
    if not addr:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found",
        )
    return addr
