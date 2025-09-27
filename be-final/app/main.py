
# app/main.py


```python
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from .db import init_db, engine
from .models import Workflow
from .settings import settings
from .triggers import router as triggers_router
from .scheduler import start as start_scheduler
from .utils import gen_secret


app = FastAPI(title="n8n-clone-fastapi")


app.include_router(triggers_router)


@app.on_event("startup")
def startup():
init_db()
start_scheduler()


@app.post("/workflows")
def create_workflow(payload: dict):
name = payload.get("name")
trigger_type = payload.get("trigger_type")
nodes = payload.get("nodes", [])
webhook_secret = payload.get("webhook_secret")
cron_expr = payload.get("cron_expr")
if trigger_type == "webhook" and not webhook_secret:
webhook_secret = gen_secret()
wf = Workflow(name=name, trigger_type=trigger_type, nodes=nodes, webhook_secret=webhook_secret, cron_expr=cron_expr)
with Session(engine) as session:
session.add(wf)
session.commit()
session.refresh(wf)
return wf


@app.get("/workflows")
def list_workflows():
with Session(engine) as session:
statement = select(Workflow)
wfs = session.exec(statement).all()
return wfs


@app.get("/workflows/{workflow_id}")
def get_workflow(workflow_id: int):
with Session(engine) as session:
```