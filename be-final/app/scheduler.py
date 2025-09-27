from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlmodel import select, Session
from .db import engine
from .models import Workflow
from .utils import run_nodes


scheduler = AsyncIOScheduler()


def load_cron_jobs():
with Session(engine) as session:
statement = select(Workflow).where(Workflow.trigger_type == "cron")
cron_wfs = session.exec(statement).all()
for wf in cron_wfs:
if not wf.cron_expr:
continue
# For simplicity, assume cron_expr is a standard 5-field expression
trigger = CronTrigger.from_crontab(wf.cron_expr)
scheduler.add_job(run_nodes, trigger=trigger, args=[wf.nodes or [], {"trigger":"cron", "workflow_id": wf.id}], id=f"wf_cron_{wf.id}")


def start():
load_cron_jobs()
scheduler.start()