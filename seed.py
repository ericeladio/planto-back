from app.database import engine, Base
from app.db_models import Plant, Review, BlogPost

plants_data = [
    {
        "id": 1,
        "name": "Hosta",
        "slug": "hosta",
        "description": "Planta de follaje vibrante, ideal para sombra y jardines húmedos.",
        "price": 399.0,
        "image_url": "https://api.builder.io/api/v1/image/assets/TEMP/d335a913dbba57246363adb5f6b65028d5a6abad?width=918",
        "rating": 4.5,
        "category": "Interior",
        "light": "Low to bright indirect light — thrives in shade",
        "water": "Keep soil consistently moist, water when top inch feels dry",
        "height": "30–60 cm",
        "toxicity": "Non-toxic to pets",
        "is_top_selling": True,
        "is_trending": False,
        "is_new_arrival": False,
    },
    {
        "id": 2,
        "name": "Haworthia",
        "slug": "haworthia",
        "description": "Suculenta pequeña con hojas rayadas, perfecta para interiores.",
        "price": 299.0,
        "image_url": "https://api.builder.io/api/v1/image/assets/TEMP/c3deee742429635aa5bd0be3d16a82edce2457f3?width=918",
        "rating": 4.5,
        "category": "Suculentas",
        "light": "Bright indirect light, tolerates low light",
        "water": "Water sparingly every 2–3 weeks, let soil dry completely",
        "height": "10–20 cm",
        "toxicity": "Non-toxic to pets",
        "is_top_selling": True,
        "is_trending": False,
        "is_new_arrival": False,
    },
    {
        "id": 3,
        "name": "Cactus columnar",
        "slug": "cactus-columnar",
        "description": "Cactus alto y esbelto que aporta un toque desértico y moderno.",
        "price": 459.0,
        "image_url": "https://api.builder.io/api/v1/image/assets/TEMP/31e5e608156f09389c0ac4e8bbdd7ff4b9fbb4be?width=918",
        "rating": 4.0,
        "category": "Suculentas",
        "light": "Full sun to bright direct light",
        "water": "Water every 3–4 weeks, allow soil to dry fully between waterings",
        "height": "60–150 cm",
        "toxicity": "Mildly toxic if ingested — keep away from pets",
        "is_top_selling": True,
        "is_trending": False,
        "is_new_arrival": False,
    },
    {
        "id": 4,
        "name": "Monstera deliciosa",
        "slug": "monstera-deliciosa",
        "description": "La clásica costilla de Adán con hojas grandes y frondosas.",
        "price": 599.0,
        "image_url": "https://api.builder.io/api/v1/image/assets/TEMP/12f34ae16439ae788c3fa31722bfa3b1a7a67fd9?width=918",
        "rating": 4.8,
        "category": "Interior",
        "light": "Bright indirect light, avoid direct sun",
        "water": "Water weekly, keep soil slightly moist but never soggy",
        "height": "60–200 cm",
        "toxicity": "Toxic to pets if ingested",
        "is_top_selling": True,
        "is_trending": False,
        "is_new_arrival": False,
    },
    {
        "id": 5,
        "name": "Strelitzia nicolai",
        "slug": "strelitzia-nicolai",
        "description": "Ave del paraíso gigante, hojas similares al banano para un look tropical.",
        "price": 799.0,
        "image_url": "https://api.builder.io/api/v1/image/assets/TEMP/b02a0413d3df262c6f931e3fa9ee7c1f1626f2f7?width=918",
        "rating": 4.6,
        "category": "Exterior",
        "light": "Bright direct to indirect light",
        "water": "Water 1–2 times per week, keep soil evenly moist",
        "height": "150–300 cm",
        "toxicity": "Non-toxic to pets",
        "is_top_selling": True,
        "is_trending": False,
        "is_new_arrival": True,
    },
    {
        "id": 6,
        "name": "Aloe vera",
        "slug": "aloe-vera",
        "description": "Suculenta medicinal con gel hidratante, fácil de cuidar.",
        "price": 349.0,
        "image_url": "https://api.builder.io/api/v1/image/assets/TEMP/5316816ff52ae9b3ef62af45bfce99cb08476b4c?width=918",
        "rating": 4.3,
        "category": "Suculentas",
        "light": "Bright indirect to direct light",
        "water": "Water every 2–3 weeks, allow soil to dry between waterings",
        "height": "30–60 cm",
        "toxicity": "Toxic to pets if ingested",
        "is_top_selling": True,
        "is_trending": False,
        "is_new_arrival": True,
    },
    {
        "id": 7,
        "name": "Hosta — Elegancia en Sombra",
        "slug": "hosta-elegancia",
        "description": "Hosta, conocida por su follaje exuberante en tonos verdes y dorados.",
        "price": 399.0,
        "image_url": "https://api.builder.io/api/v1/image/assets/TEMP/763dd970ada067132be533eb7ebccbde943dae86?width=1202",
        "rating": 4.5,
        "category": "Exterior",
        "light": "Shade to partial shade",
        "water": "Keep soil moist, water when top layer dries",
        "height": "30–60 cm",
        "toxicity": "Non-toxic to pets",
        "is_top_selling": False,
        "is_trending": True,
        "is_new_arrival": True,
    },
    {
        "id": 8,
        "name": "Haworthia — Belleza Minimalista",
        "slug": "haworthia-minimalista",
        "description": "Pequeña suculenta con patrones rayados únicos.",
        "price": 299.0,
        "image_url": "https://api.builder.io/api/v1/image/assets/TEMP/e44f8798449db0c15aa91c37cdce7c11975284dd?width=1464",
        "rating": 4.4,
        "category": "Suculentas",
        "light": "Bright indirect light",
        "water": "Water every 2–3 weeks, let soil dry completely",
        "height": "10–20 cm",
        "toxicity": "Non-toxic to pets",
        "is_top_selling": False,
        "is_trending": True,
        "is_new_arrival": True,
    }
]

reviews_data = [
    {"id": 1, "plant_id": 1, "name": "Maxn Raval", "rating": 4.5, "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,", "avatar_color": "#5a3a28"},
    {"id": 2, "plant_id": 1, "name": "Sophia Chen", "rating": 5.0, "text": "Absolutely love this plant! It arrived healthy and has been thriving in my living room. Highly recommend for beginners.", "avatar_color": "#2a6b4a"},
    {"id": 3, "plant_id": 2, "name": "venely k", "rating": 4.5, "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,", "avatar_color": "#7a4a3a"},
    {"id": 4, "plant_id": 3, "name": "Lii thakur", "rating": 4.5, "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,", "avatar_color": "#4a5a6a"},
    {"id": 5, "plant_id": 3, "name": "Marco V.", "rating": 4.0, "text": "Great cactus, very low maintenance. Looks stunning on my desk. Shipping was fast and packaging was secure.", "avatar_color": "#8a6a3a"},
    {"id": 6, "plant_id": 4, "name": "Aria K.", "rating": 5.0, "text": "The Monstera is simply gorgeous! Big fenestrated leaves, very healthy roots. Will buy again from Planto.", "avatar_color": "#3a5a7a"},
    {"id": 7, "plant_id": 4, "name": "James Park", "rating": 4.5, "text": "Beautiful plant, exactly as pictured. It's growing new leaves every week. Customer service was helpful too.", "avatar_color": "#6a3a5a"},
    {"id": 8, "plant_id": 5, "name": "Elena R.", "rating": 4.5, "text": "This Strelitzia is the centerpiece of my garden. It's growing so fast! The tropical vibe is unmatched.", "avatar_color": "#3a6a6a"},
    {"id": 9, "plant_id": 6, "name": "David M.", "rating": 4.0, "text": "Healthy aloe plant, perfect size for my kitchen. Have already used the gel for a small burn — it works!", "avatar_color": "#5a5a3a"},
    {"id": 10, "plant_id": 7, "name": "Clara W.", "rating": 4.5, "text": "The Hosta is beautiful and full. The variegated leaves are stunning. Arrived well-packaged and on time.", "avatar_color": "#4a4a6a"},
    {"id": 11, "plant_id": 8, "name": "Tom S.", "rating": 4.0, "text": "Tiny but mighty! This Haworthia sits perfectly on my desk. Only needs water every few weeks. Perfect for busy people.", "avatar_color": "#6a5a4a"},
]

blog_posts_data = [
    {
        "id": 1,
        "slug": "choose-the-perfect-houseplant",
        "title": "How to Choose the Perfect Houseplant",
        "excerpt": "A beginner's guide to selecting the right indoor plants for your space and lifestyle.",
        "content": "Choosing the perfect houseplant depends on several factors including light availability, your schedule, and experience level...",
        "image_url": "https://api.builder.io/api/v1/image/assets/TEMP/ef8a32dcec484a9b60dbaa0f8ae73718cced7c81?width=918",
        "author": "Planto",
        "published": True,
    },
    {
        "id": 2,
        "slug": "succulent-care-guide",
        "title": "Succulent Care Guide",
        "excerpt": "Everything you need to know about keeping succulents happy and healthy.",
        "content": "Succulents are some of the easiest plants to care for, but they do have specific needs...",
        "image_url": "https://api.builder.io/api/v1/image/assets/TEMP/e44f8798449db0c15aa91c37cdce7c11975284dd?width=1464",
        "author": "Planto",
        "published": True,
    },
    {
        "id": 3,
        "slug": "benefits-of-indoor-plants",
        "title": "Benefits of Indoor Plants",
        "excerpt": "Discover how indoor plants can improve your health, mood, and productivity.",
        "content": "Studies have shown that having indoor plants can reduce stress, improve air quality, and boost creativity...",
        "image_url": "https://api.builder.io/api/v1/image/assets/TEMP/fa3a58342254182b92a36092f9d4f5a0b11ecf6a?width=1789",
        "author": "Planto",
        "published": True,
    },
]


def seed():
    Base.metadata.create_all(bind=engine)

    from sqlalchemy.orm import Session
    from app.database import SessionLocal

    db: Session = SessionLocal()

    try:
        if db.query(Plant).count() > 0:
            print("Database already seeded, skipping.")
            return

        for p in plants_data:
            db.add(Plant(**p))
        db.flush()

        for r in reviews_data:
            db.add(Review(**r))
        db.flush()

        for b in blog_posts_data:
            db.add(BlogPost(**b))

        db.commit()
        print(f"Seeded {len(plants_data)} plants, {len(reviews_data)} reviews, {len(blog_posts_data)} blog posts.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
