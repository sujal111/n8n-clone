from pydantic import BaseSettings


class Settings(BaseSettings):
database_url: str = "sqlite:///./data.db"
telegram_bot_token: str | None = None
resend_api_key: str | None = None
openai_api_key: str | None = None
anthropic_api_key: str | None = None


class Config:
env_file = ".env"


settings = Settings()