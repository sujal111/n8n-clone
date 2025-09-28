from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./n8n.db"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    # optional defaults
    DEFAULT_LLM_PROVIDER: str = "openai"  # openai | anthropic | google_gemini

    class Config:
        env_file = ".env"

settings = Settings()
