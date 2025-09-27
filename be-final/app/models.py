from sqlmodel import SQLModel, Field, JSON
from typing import Optional, List, Dict
from datetime import datetime


class Node(JSON):
...


class Workflow(SQLModel, table=True):
id: Optional[int] = Field(default=None, primary_key=True)
name: str
trigger_type: str # manual | webhook | cron
trigger_config: Dict | None = {}
nodes: List[Dict] | None = [] # list of action nodes in sequence
webhook_secret: Optional[str] = None
cron_expr: Optional[str] = None
created_at: datetime = Field(default_factory=datetime.utcnow)