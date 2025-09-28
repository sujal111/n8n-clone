import uvicorn
from fastapi import FastAPI
from app.routers import workflows, triggers, actions
from app.triggers import webhook as webhook_router
from app.settings import settings
from app.db import engine, Base
import asyncio

app = FastAPI(title="n8n-fastapi")

app.include_router(workflows.router)
app.include_router(triggers.router)
app.include_router(actions.router)
app.include_router(webhook_router.router)  # webhook handler

@app.on_event("startup")
async def startup():
    # create tables for demo
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True)
