from sqlalchemy import Column, Integer, String, Text, JSON, Boolean
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from app.db import Base

class Credential(Base):
    __tablename__ = "credentials"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    kind = Column(String)  # e.g., 'telegram', 'resend', 'openai'
    data = Column(JSON)    # store keys and metadata (be careful in prod)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Workflow(Base):
    __tablename__ = "workflows"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    spec = Column(JSON)  # workflow graph definition
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class WebhookEndpoint(Base):
    __tablename__ = "webhooks"
    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, unique=True, index=True)  # e.g., /webhook/<uuid>
    workflow_id = Column(Integer)
    method = Column(String, default="POST")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
