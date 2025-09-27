# src/fastflow/core/config.py
# -------------------------
from pydantic import BaseSettings, Field, AnyHttpUrl
from typing import Optional


class Settings(BaseSettings):
APP_NAME: str = "fastflow"
DEBUG: bool = False
DATABASE_URL: str = Field(..., env='DATABASE_URL')
REDIS_URL: str = Field('redis://localhost:6379/0', env='REDIS_URL')
CELERY_BROKER_URL: str = Field('redis://localhost:6379/1', env='CELERY_BROKER_URL')
CELERY_RESULT_BACKEND: str = Field('redis://localhost:6379/2', env='CELERY_RESULT_BACKEND')
TELEGRAM_BOT_TOKEN: Optional[str]
RESEND_API_KEY: Optional[str]
LLM_PROVIDER: str = Field('openai')
OPENAI_API_KEY: Optional[str]


class Config:
env_file = '.env'
env_file_encoding = 'utf-8'


settings = Settings()