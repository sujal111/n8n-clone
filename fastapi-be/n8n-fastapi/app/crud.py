from sqlalchemy.future import select
from sqlalchemy import insert
from app.models import Credential, Workflow, WebhookEndpoint
from app.schemas import CredentialCreate, WorkflowCreate
from app.db import AsyncSession

async def create_credential(db: AsyncSession, cred: CredentialCreate):
    obj = Credential(name=cred.name, kind=cred.kind, data=cred.data)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def list_credentials(db: AsyncSession):
    result = await db.execute(select(Credential))
    return result.scalars().all()

async def create_workflow(db: AsyncSession, wf: WorkflowCreate):
    obj = Workflow(name=wf.name, spec=wf.spec)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def get_workflow(db: AsyncSession, workflow_id: int):
    result = await db.execute(select(Workflow).filter(Workflow.id == workflow_id))
    return result.scalar_one_or_none()

async def create_webhook(db: AsyncSession, path: str, workflow_id: int, method="POST"):
    obj = WebhookEndpoint(path=path, workflow_id=workflow_id, method=method)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def get_webhook_by_path(db: AsyncSession, path: str):
    result = await db.execute(select(WebhookEndpoint).filter(WebhookEndpoint.path == path))
    return result.scalar_one_or_none()
