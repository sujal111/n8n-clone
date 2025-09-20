
from sqlalchemy import (
    Column, Integer, String, JSON, DateTime, ForeignKey, Boolean, Text
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import enum



class Credential(BaseModel):
    __tablename__ = "credentials"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)  # "telegram", "resend", "openai", etc
    encrypted_secret = Column(Text, nullable=False)
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
