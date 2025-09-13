
from sqlalchemy import (
    Column, Integer, String, JSON, DateTime, ForeignKey, Boolean, Text
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import enum

Base = declarative_base()

class Credential(Base):
    __tablename__ = "credentials"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)  # "telegram", "resend", "openai", etc
    encrypted_secret = Column(Text, nullable=False)
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)

class Workflow(Base):
    __tablename__ = "workflows"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    nodes = relationship("Node", back_populates="workflow", cascade="all,delete-orphan")

class Node(Base):
    __tablename__ = "nodes"
    id = Column(Integer, primary_key=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"))
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # "trigger" or "action"
    subtype = Column(String, nullable=False)  # e.g., "manual", "webhook", "cron", "telegram", "resend", "llm"
    config = Column(JSON, default={})  # arbitrary config (cron expr, webhook path, action args)
    credential_id = Column(Integer, ForeignKey("credentials.id"), nullable=True)
    order = Column(Integer, default=0)  # simple sequential runner
    workflow = relationship("Workflow", back_populates="nodes")
    credential = relationship("Credential")

class Run(Base):
    __tablename__ = "runs"
    id = Column(Integer, primary_key=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"))
    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)
    status = Column(String, default="running")  # running, success, failed
    logs = Column(JSON, default=[])
