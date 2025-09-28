from fastapi import APIRouter, BackgroundTasks
from app.engine import run_workflow

router = APIRouter(prefix="/actions")

@router.post("/test-run")
async def test_run(spec: dict, background_tasks: BackgroundTasks):
    # simple way to test a workflow spec immediately
    background_tasks.add_task(run_workflow, spec, {})
    return {"status": "started"}
