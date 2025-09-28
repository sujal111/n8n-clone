from fastapi import APIRouter, Request, Depends, BackgroundTasks, HTTPException
from app.db import get_db
from app.crud import get_webhook_by_path, get_workflow
from app.engine import run_workflow
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post("/webhook/{path:path}")
async def handle_webhook(path: str, request: Request, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    webhook = await get_webhook_by_path(db, "/webhook/" + path)
    if not webhook:
        raise HTTPException(status_code=404, detail="webhook not found")
    payload = await request.json()
    wf = await get_workflow(db, webhook.workflow_id)
    if not wf:
        raise HTTPException(status_code=404, detail="workflow not found")
    # background execution
    background_tasks.add_task(run_workflow, wf.spec, payload)
    return {"status": "accepted"}
