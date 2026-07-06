import secrets
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.config import settings
from app.db_models import (
    CartItem,
    Order,
    OrderItem,
    Plant,
    ResetToken,
    Review,
    User,
)


# ─── USERS ────────────────────────────────────────────────────────────────────


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def add_user(db: Session, email: str, password_hash: str, full_name: Optional[str] = None) -> User:
    user = User(email=email, password_hash=password_hash, full_name=full_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_password(db: Session, email: str, password_hash: str) -> None:
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.password_hash = password_hash
        db.commit()


# ─── RESET TOKENS ─────────────────────────────────────────────────────────────


def create_reset_token(db: Session, email: str) -> str:
    token = secrets.token_urlsafe(32)
    rt = ResetToken(
        email=email,
        token=token,
        expires_at=datetime.utcnow() + timedelta(minutes=settings.RESET_TOKEN_EXPIRATION_MINUTES),
    )
    db.add(rt)
    db.commit()
    return token


def get_reset_token(db: Session, token: str) -> Optional[ResetToken]:
    now = datetime.utcnow()
    return (
        db.query(ResetToken)
        .filter(
            ResetToken.token == token,
            ResetToken.used == False,
            ResetToken.expires_at > now,
        )
        .first()
    )


def mark_token_used(db: Session, token: str) -> None:
    rt = db.query(ResetToken).filter(ResetToken.token == token).first()
    if rt:
        rt.used = True
        db.commit()


# ─── PLANTS ────────────────────────────────────────────────────────────────────


def get_plant_by_slug(db: Session, slug: str) -> Optional[Plant]:
    return db.query(Plant).filter(Plant.slug == slug).first()


def get_plant_by_id(db: Session, plant_id: int) -> Optional[Plant]:
    return db.query(Plant).filter(Plant.id == plant_id).first()


def get_plants(
    db: Session,
    search: Optional[str] = None,
    category: Optional[str] = None,
    sort: Optional[str] = None,
    page: int = 1,
    per_page: int = 20,
):
    q = db.query(Plant)

    if search:
        like = f"%{search.lower()}%"
        q = q.filter(
            or_(
                Plant.name.ilike(like),
                Plant.description.ilike(like),
            )
        )

    if category:
        q = q.filter(Plant.category.ilike(category))

    total = q.count()

    if sort == "price-asc":
        q = q.order_by(Plant.price.asc())
    elif sort == "price-desc":
        q = q.order_by(Plant.price.desc())
    elif sort == "name-asc":
        q = q.order_by(Plant.name.asc())
    elif sort == "name-desc":
        q = q.order_by(Plant.name.desc())

    pages = (total + per_page - 1) // per_page
    items = q.offset((page - 1) * per_page).limit(per_page).all()

    return items, total, pages


def get_trending_plants(db: Session):
    return db.query(Plant).filter(Plant.is_trending == True).all()


def get_new_arrivals(db: Session):
    return db.query(Plant).filter(Plant.is_new_arrival == True).order_by(Plant.id.desc()).all()


def get_top_selling_plants(db: Session):
    return db.query(Plant).filter(Plant.is_top_selling == True).all()


# ─── REVIEWS ──────────────────────────────────────────────────────────────────


def get_reviews_by_plant_id(db: Session, plant_id: int):
    return db.query(Review).filter(Review.plant_id == plant_id).all()


def get_best_reviews(db: Session, min_rating: float = 4.0, limit: int = 6):
    return (
        db.query(Review)
        .filter(Review.rating >= min_rating)
        .order_by(Review.rating.desc())
        .limit(limit)
        .all()
    )


# ─── BLOG POSTS ───────────────────────────────────────────────────────────────


def get_blog_by_slug(db: Session, slug: str):
    from app.db_models import BlogPost
    return db.query(BlogPost).filter(BlogPost.slug == slug).first()


def get_published_posts(db: Session):
    from app.db_models import BlogPost
    return db.query(BlogPost).filter(BlogPost.published == True).all()


# ─── CART ─────────────────────────────────────────────────────────────────────


def get_cart_items(db: Session, user_id: int):
    return db.query(CartItem).filter(CartItem.user_id == user_id).all()


def add_cart_item(db: Session, user_id: int, plant_id: int, quantity: int) -> CartItem:
    existing = (
        db.query(CartItem)
        .filter(CartItem.user_id == user_id, CartItem.plant_id == plant_id)
        .first()
    )
    if existing:
        new_qty = min(existing.quantity + quantity, 99)
        existing.quantity = new_qty
        db.commit()
        db.refresh(existing)
        return existing

    item = CartItem(user_id=user_id, plant_id=plant_id, quantity=min(quantity, 99))
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def clear_cart(db: Session, user_id: int) -> None:
    db.query(CartItem).filter(CartItem.user_id == user_id).delete()
    db.commit()


# ─── ORDERS ───────────────────────────────────────────────────────────────────


def create_order(db: Session, user_id: int) -> Order:
    cart_items = get_cart_items(db, user_id)
    total = sum(item.plant.price * item.quantity for item in cart_items)

    order = Order(user_id=user_id, total=total)
    db.add(order)
    db.flush()

    for ci in cart_items:
        oi = OrderItem(
            order_id=order.id,
            plant_id=ci.plant_id,
            plant_name=ci.plant.name,
            plant_price=ci.plant.price,
            plant_image=ci.plant.image_url,
            quantity=ci.quantity,
        )
        db.add(oi)

    db.query(CartItem).filter(CartItem.user_id == user_id).delete()
    db.commit()
    db.refresh(order)
    return order


def get_user_orders(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).all()
