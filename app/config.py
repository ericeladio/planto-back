from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/planto"
    JWT_SECRET: str = "planto-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60
    RESET_TOKEN_EXPIRATION_MINUTES: int = 30
    BREVO_API_KEY: str = ""
    BREVO_SENDER_NAME: str = "Planto"
    BREVO_SENDER_EMAIL: str = "noreply@planto.com"
    BREVO_WELCOME_TEMPLATE_ID: int = 1
    BREVO_RESET_TEMPLATE_ID: int = 2
    BREVO_ORDER_TEMPLATE_ID: int = 4
    FRONTEND_URL: str = "http://localhost:5173"


settings = Settings()
