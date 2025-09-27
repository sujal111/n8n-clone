import uuid
from typing import Dict, Any
from app.models import Credential, Workflow, WorkflowTrigger, Node

# ----------------------------------------------------------------------
# In-Memory Data Storage (Simulating a Database)
# ----------------------------------------------------------------------
# In production, this would be replaced by SQLAlchemy/Alembic connecting to PostgreSQL.

CREDENTIALS_DB: Dict[str, Any] = {}
WORKFLOWS_DB: Dict[str, Any] = {}
EXECUTIONS_DB: Dict[str, Any] = {}

# Store example workflow ID globally for easy access in API docs
EXAMPLE_WEBHOOK_WORKFLOW_ID: str = ""

def setup_example_data():
    """Seeds the in-memory database with example credentials and a workflow."""
    global EXAMPLE_WEBHOOK_WORKFLOW_ID
    print("Initializing example credentials and workflow...")

    # 1. Credentials
    tg_cred_id = str(uuid.uuid4())
    resend_cred_id = str(uuid.uuid4())
    llm_cred_id = str(uuid.uuid4())

    CREDENTIALS_DB[tg_cred_id] = Credential(
        id=tg_cred_id,
        name="My Telegram Bot",
        type="telegram",
        data={
            "bot_token": "mock-tg-token-123456",
            "chat_id": "123456789"
        }
    ).dict()

    CREDENTIALS_DB[resend_cred_id] = Credential(
        id=resend_cred_id,
        name="My Resend Email Key",
        type="resend",
        data={
            "api_key": "mock-resend-key-987654",
            "sender_email": "hello@example.com"
        }
    ).dict()

    CREDENTIALS_DB[llm_cred_id] = Credential(
        id=llm_cred_id,
        name="Gemini LLM Key",
        type="llm",
        data={
            "api_key": "mock-gemini-key-0000",
            "model_name": "gemini-2.5-flash"
        }
    ).dict()


    # 2. Workflow Nodes
    # Node 1: Telegram Notification
    node_tg_id = str(uuid.uuid4())
    node_tg = Node(
        id=node_tg_id,
        type="telegram",
        data={
            "message": "Webhook execution completed. Final step success.",
            "credential_id": tg_cred_id
        },
    )

    # Node 2: Send Email
    node_email_id = str(uuid.uuid4())
    node_email = Node(
        id=node_email_id,
        type="resend",
        data={
            "to": "admin@company.com",
            "subject": "Pipeliner Execution Alert",
            "body": "The webhook workflow has completed successfully.",
            "credential_id": resend_cred_id
        },
        next=node_tg_id # Email runs, then Telegram
    )

    # Node 3: LLM Action (Start Node)
    node_llm_id = str(uuid.uuid4())
    node_llm = Node(
        id=node_llm_id,
        type="llm",
        data={
            "prompt": "Analyze the input data and generate a summary report.",
            "credential_id": llm_cred_id
        },
        next=node_email_id # LLM runs, then Email
    )

    # 3. Workflow Definition (Webhook Trigger)
    webhook_workflow_id = str(uuid.uuid4())
    WORKFLOWS_DB[webhook_workflow_id] = Workflow(
        id=webhook_workflow_id,
        name="E-Commerce Order Processor",
        trigger=WorkflowTrigger(type="webhook"),
        start_node_id=node_llm_id, # Start with LLM
        nodes={
            node_llm.id: node_llm.dict(),
            node_email.id: node_email.dict(),
            node_tg.id: node_tg.dict(),
        }
    ).dict()

    EXAMPLE_WEBHOOK_WORKFLOW_ID = webhook_workflow_id
    print(f"\nExample Webhook Workflow ID: {EXAMPLE_WEBHOOK_WORKFLOW_ID}")
    print("Credentials loaded: Telegram, Resend, Gemini/LLM.")
