



# -------------------------
# src/fastflow/models.py
# -------------------------
from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from .db.session import Base
from sqlalchemy.orm import relationship


class Workflow(Base):
__tablename__ = 'workflows'
id = Column(Integer, primary_key=True, index=True)
name = Column(String(255), nullable=False)
spec = Column(JSON, nullable=False) # nodes + edges
created_at = Column(DateTime(timezone=True), server_default=func.now())


class Credential(Base):
__tablename__ = 'credentials'
id = Column(Integer, primary_key=True, index=True)
owner = Column(String(128), nullable=False)
type = Column(String(50), nullable=False)
data = Column(JSON, nullable=False) # encrypted in prod
created_at = Column(DateTime(timezone=True), server_default=func.now())


class RunHistory(Base):
__tablename__ = 'run_history'
id = Column(Integer, primary_key=True, index=True)
workflow_id = Column(Integer, ForeignKey('workflows.id'), nullable=False)
status = Column(String(50), default='pending')
input = Column(JSON)
output = Column(JSON)
created_at = Column(DateTime(timezone=True), server_default=func.now())


workflow = relationship('Workflow')