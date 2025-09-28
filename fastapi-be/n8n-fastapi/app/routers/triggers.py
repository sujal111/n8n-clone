from fastapi import APIRouter
from app.triggers.cron_manager import start_scheduler, schedule_workflow

router = APIRouter(prefix="/triggers")

@router.post("/cron/schedule")
async def schedule_cron(body: dict):
    """
    body: { "workflow_id": 1, "spec": {...}, "cron": {"minute":"0","hour":"*/1"} }
    """
    workflow_id = body.get("workflow_id")
    spec = body.get("spec")
    cron = body.get("cron")
    start_scheduler()
    schedule_workflow(workflow_id, spec, cron)
    return {"status": "scheduled"}
