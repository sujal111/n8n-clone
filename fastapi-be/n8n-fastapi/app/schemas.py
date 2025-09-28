from pydantic import BaseModel
from typing import Any, Dict, Optional

class CredentialCreate(BaseModel):
    name: str
    kind: str
    data: Dict[str, Any]

class WorkflowCreate(BaseModel):
    name: str
    spec: Dict[str, Any]

class TriggerInvoke(BaseModel):
    workflow_id: int
    payload: Optional[Dict[str, Any]] = None
