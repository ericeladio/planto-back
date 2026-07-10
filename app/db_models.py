from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    cart_items: Mapped[list["CartItem"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    orders: Mapped[list["Order"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    saved_cards: Mapped[list["SavedCard"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    addresses: Mapped[list["Address"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class ResetToken(Base):
    __tablename__ = "reset_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    used: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Plant(Base):
    __tablename__ = "plants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="Rs")
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    light: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    water: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    height: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    toxicity: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_top_selling: Mapped[bool] = mapped_column(Boolean, default=False)
    is_trending: Mapped[bool] = mapped_column(Boolean, default=False)
    is_new_arrival: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    reviews: Mapped[list["Review"]] = relationship(back_populates="plant", cascade="all, delete-orphan")
    cart_items: Mapped[list["CartItem"]] = relationship(back_populates="plant", cascade="all, delete-orphan")


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    plant_id: Mapped[int] = mapped_column(Integer, ForeignKey("plants.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    avatar_color: Mapped[str] = mapped_column(String(7), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    plant: Mapped["Plant"] = relationship(back_populates="reviews")


class BlogPost(Base):
    __tablename__ = "blog_posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(500), default="")
    excerpt: Mapped[str] = mapped_column(Text, default="")
    content: Mapped[str] = mapped_column(Text, default="")
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    date: Mapped[str] = mapped_column(String(50), default="")
    author: Mapped[str] = mapped_column(String(255), default="Planto")
    published: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class CartItem(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    plant_id: Mapped[int] = mapped_column(Integer, ForeignKey("plants.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    user: Mapped["User"] = relationship(back_populates="cart_items")
    plant: Mapped["Plant"] = relationship(back_populates="cart_items")


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    label: Mapped[str] = mapped_column(String(50), nullable=False)
    street: Mapped[str] = mapped_column(String(255), nullable=False)
    number: Mapped[str] = mapped_column(String(20), nullable=False)
    colony: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(255), nullable=False)
    state: Mapped[str] = mapped_column(String(255), nullable=False)
    zip_code: Mapped[str] = mapped_column(String(10), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    reference: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="addresses")
    orders: Mapped[list["Order"]] = relationship(back_populates="address")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="confirmed")
    total: Mapped[float] = mapped_column(Float, nullable=False)
    address_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("addresses.id"), nullable=True)
    address_street: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    address_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    address_colony: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    address_city: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    address_state: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    address_zip_code: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    address_country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")
    address: Mapped[Optional["Address"]] = relationship(back_populates="orders")


class NewsletterSubscriber(Base):
    __tablename__ = "newsletter_subscribers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"), nullable=False)
    plant_id: Mapped[int] = mapped_column(Integer, ForeignKey("plants.id"), nullable=False)
    plant_name: Mapped[str] = mapped_column(String(255), nullable=False)
    plant_price: Mapped[float] = mapped_column(Float, nullable=False)
    plant_image: Mapped[str] = mapped_column(String(500), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    order: Mapped["Order"] = relationship(back_populates="items")


class SavedCard(Base):
    __tablename__ = "saved_cards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    last_four: Mapped[str] = mapped_column(String(4), nullable=False)
    exp_month: Mapped[int] = mapped_column(Integer, nullable=False)
    exp_year: Mapped[int] = mapped_column(Integer, nullable=False)
    token: Mapped[str] = mapped_column(String(50), nullable=False)
    brand: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="saved_cards")
