


from pydantic import BaseModel
from typing import Any, Dict, Optional


class WorkflowCreate(BaseModel):
name: str
spec: Dict[str, Any]


class WorkflowRead(BaseModel):
id: int
name: str
spec: Dict[str, Any]


class Config:
orm_mode = True


class RunCreate(BaseModel):
input: Optional[Dict[str, Any]] = None

class RunRead(BaseModel):
id: int
workflow_id: int
status: str
input: Optional[Dict[str, Any]]
output: Optional[Dict[str, Any]]


    class Config:
        orm_mode = True


