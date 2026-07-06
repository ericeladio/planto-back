from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import plants, auth, cart, orders, blog, reviews, newsletter, cards

app = FastAPI(title="Planto API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plants.router, prefix="/api/plants", tags=["Plants"])
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(cart.router, prefix="/api/cart", tags=["Cart"])
app.include_router(orders.router, prefix="/api/orders", tags=["Orders"])
app.include_router(blog.router, prefix="/api/blog", tags=["Blog"])
app.include_router(reviews.router, prefix="/api/reviews", tags=["Reviews"])
app.include_router(newsletter.router, prefix="/api/newsletter", tags=["Newsletter"])
app.include_router(cards.router, prefix="/api/cards", tags=["Cards"])


@app.get("/api/health")
def health():
    return {"status": "ok"}
