from fastapi import FastAPI
from app.routers import workflows, triggers, actions, credentials
from app.db import init_db

app = FastAPI(title="n8n-clone")

app.include_router(workflows.router, prefix="/workflows")
app.include_router(triggers.router, prefix="/triggers")
app.include_router(actions.router, prefix="/actions")
app.include_router(credentials.router, prefix="/credentials")

@app.on_event("startup")
def startup():
    init_db()
