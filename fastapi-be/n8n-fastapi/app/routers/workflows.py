from fastapi import APIRouter, Depends, BackgroundTasks
from app.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import WorkflowCreate, TriggerInvoke
from app.crud import create_workflow, get_workflow, create_webhook
from app.engine import run_workflow
import uuid

router = APIRouter(prefix="/workflows")

@router.post("/")
async def create_workflow_endpoint(wf: WorkflowCreate, db: AsyncSession = Depends(get_db)):
    obj = await create_workflow(db, wf)
    return obj

@router.post("/invoke")
async def manual_invoke(payload: TriggerInvoke, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    wf = await get_workflow(db, payload.workflow_id)
    if not wf:
        return {"error": "workflow not found"}
    background_tasks.add_task(run_workflow, wf.spec, payload.payload or {})
    return {"status": "scheduled"}

@router.post("/{workflow_id}/webhook")
async def create_webhook_endpoint(workflow_id: int, db: AsyncSession = Depends(get_db)):
    path = f"/webhook/{uuid.uuid4().hex}"
    obj = await create_webhook(db, path, workflow_id)
    return {"path": obj.path}
