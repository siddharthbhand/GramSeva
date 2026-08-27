from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # =====================================================
    # Application
    # =====================================================

    PROJECT_NAME: str = "GramSeva API"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"

    # =====================================================
    # Database
    # =====================================================

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # =====================================================
    # JWT Security
    # =====================================================

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # =====================================================
    # CORS
    # =====================================================

    FRONTEND_URL: str = "http://localhost:5173"

    # =====================================================
    # Environment Configuration
    # =====================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()