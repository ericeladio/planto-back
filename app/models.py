from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Optional, Literal


class PlantOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    description: Optional[str] = None
    price: float
    currency: str = "Rs"
    image_url: str
    rating: Optional[float] = None
    category: Optional[str] = None
    light: Optional[str] = None
    water: Optional[str] = None
    height: Optional[str] = None
    toxicity: Optional[str] = None
    is_top_selling: bool = False
    is_trending: bool = False
    is_new_arrival: bool = False


class PlantListResponse(BaseModel):
    items: list[PlantOut]
    total: int
    page: int
    per_page: int
    pages: int


class UserRegister(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None


class UserOut(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class CartItemOut(BaseModel):
    id: int
    plant_id: int
    plant_name: str
    plant_price: float
    plant_image: str
    quantity: int


class CartResponse(BaseModel):
    items: list[CartItemOut]
    total_items: int
    total_price: float


class CartAddRequest(BaseModel):
    plant_id: int
    quantity: int = Field(default=1, ge=1, le=99)


class CartUpdateRequest(BaseModel):
    quantity: int = Field(ge=1, le=99)


class OrderOut(BaseModel):
    id: int
    status: str
    total: float
    items: list[CartItemOut]
    created_at: str


class BlogPostOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    title: str
    excerpt: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None
    date: Optional[str] = None
    author: str = "Planto"


class ReviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    plant_id: int
    name: str
    rating: float
    text: str
    avatar_color: str


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class PaymentRequest(BaseModel):
    card_number: str = Field(..., min_length=16, max_length=16)
    exp_month: int = Field(..., ge=1, le=12)
    exp_year: int = Field(..., ge=2025)
    cvv: str = Field(..., min_length=3, max_length=3)


class SavedCardOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    last_four: str
    exp_month: int
    exp_year: int
    brand: str


class SaveCardRequest(BaseModel):
    card_number: str = Field(..., min_length=16, max_length=16)
    exp_month: int = Field(..., ge=1, le=12)
    exp_year: int = Field(..., ge=2025)
    cvv: str = Field(..., min_length=3, max_length=3)


class PayWithSavedCardRequest(BaseModel):
    card_id: int
    cvv: str = Field(..., min_length=3, max_length=3)


class PlaceOrderRequest(BaseModel):
    type: Literal["new", "saved"]
    card_number: Optional[str] = Field(None, min_length=16, max_length=16)
    exp_month: Optional[int] = Field(None, ge=1, le=12)
    exp_year: Optional[int] = Field(None, ge=2025)
    cvv: str = Field(..., min_length=3, max_length=3)
    card_id: Optional[int] = None

    @model_validator(mode="after")
    def validate_fields(self):
        if self.type == "new":
            if not self.card_number:
                raise ValueError("card_number required when type='new'")
            if not self.exp_month:
                raise ValueError("exp_month required when type='new'")
            if not self.exp_year:
                raise ValueError("exp_year required when type='new'")
        elif self.type == "saved":
            if not self.card_id:
                raise ValueError("card_id required when type='saved'")
        return self


class BlogListResponse(BaseModel):
    items: list[BlogPostOut]
    total: int
