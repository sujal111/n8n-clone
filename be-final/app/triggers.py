

# app/triggers.py


```python
from fastapi import APIRouter, BackgroundTasks, HTTPException
from sqlmodel import Session, select
from .models import Workflow
from .db import engine
from .utils import run_nodes


router = APIRouter()


@router.post("/workflows/{workflow_id}/run")
async def manual_run(workflow_id: int, background_tasks: BackgroundTasks):
with Session(engine) as session:
wf = session.get(Workflow, workflow_id)
if not wf:
raise HTTPException(status_code=404, detail="workflow not found")
# run in background
background_tasks.add_task(run_nodes, wf.nodes or [], {"trigger": "manual"})
return {"status": "scheduled manual run"}


@router.post("/webhook/{secret}")
async def webhook_handler(secret: str, payload: dict, background_tasks: BackgroundTasks):
with Session(engine) as session:
statement = select(Workflow).where(Workflow.webhook_secret == secret)
wf = session.exec(statement).first()
if not wf:
raise HTTPException(status_code=404, detail="workflow not found")
background_tasks.add_task(run_nodes, wf.nodes or [], {"trigger": "webhook", "payload": payload})
return {"status": "accepted"}
```