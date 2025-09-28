from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio
from app.engine import run_workflow

scheduler = AsyncIOScheduler()

def start_scheduler():
    if not scheduler.running:
        scheduler.start()

def schedule_workflow(id: int, spec: dict, cron_expr: dict):
    """
    cron_expr: dict like {"minute":"0", "hour":"*/1"} or full cronstring mapping
    """
    def job():
        # run in background
        asyncio.create_task(run_workflow(spec, {}))
    trigger = CronTrigger(**cron_expr)
    scheduler.add_job(job, trigger, id=str(id), replace_existing=True)
