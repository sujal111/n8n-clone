from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from db import SessionLocal, engine
from models import Base, Workflow, Node, Credential
from crypto_utils import encrypt_secret, decrypt_secret
from scheduler import start_scheduler, schedule_cron_nodes
from runner import run_workflow
from pydantic import BaseModel
import uvicorn
from typing import Optional, List



Base.metadata.create_all(bind=engine)
app = FastAPI(title="n8n-clone-starter")


class CredentialIn(BaseModel):
    name: str 
    type: str 
    secret: str 
    metadata:Optional[dict]={}



class Workflow()



class NodeIn(BaseModel):
    workflow_id: str 
    name: str 
    type: str 
    subtype: str 
    config: dict={}
    