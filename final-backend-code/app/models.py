import uuid
from typing import Dict, Any, List, Optional, Literal
from pydantic import BaseModel, Field
import time

# --- Credentials Models ---

class TelegramCreds(BaseModel):
    """Credentials for Telegram Bot API."""
    bot_token: str = Field(..., description="The Telegram Bot Token.")
    chat_id: str = Field(..., description="The default Chat ID for sending messages.")

class ResendCreds(BaseModel):
    """Credentials for Resend/SMTP Email API."""
    api_key: str = Field(..., description="The Resend API Key or SMTP password.")
    sender_email: str = Field(..., description="The verified sender email address.")

class LLMCreds(BaseModel):
    """Placeholder Credentials for LLM Services (Anthropic/Gemini/OpenAI)."""
    api_key: str = Field(..., description="The API Key for the LLM service.")
    model_name: str = Field("gemini-2.5-flash", description="Default model to use.")


class Credential(BaseModel):
    """Base model for storing credentials."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., description="A human-readable name for the credential.")
    type: Literal["telegram", "resend", "llm"]
    data: Dict[str, Any] # Will hold the specific credentials (e.g., TelegramCreds.dict())

# --- Node/Action Models ---

class TelegramActionData(BaseModel):
    """Configuration for the Telegram Send Message action."""
    message: str = Field(..., description="The message content to send.")
    credential_id: str = Field(..., description="ID of the Telegram credential to use.")

class ResendActionData(BaseModel):
    """Configuration for the Resend Send Email action."""
    to: str = Field(..., description="Recipient email address.")
    subject: str = Field(..., description="Email subject line.")
    body: str = Field(..., description="Email body content.")
    credential_id: str = Field(..., description="ID of the Resend credential to use.")

class LLMActionData(BaseModel):
    """Configuration for the LLM Generation action."""
    prompt: str = Field(..., description="The prompt to send to the LLM.")
    credential_id: str = Field(..., description="ID of the LLM credential to use.")

class Node(BaseModel):
    """A single node (action) in the workflow."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: Literal["telegram", "resend", "llm"]
    data: Dict[str, Any] # Specific action data (e.g., TelegramActionData.dict())
    next: Optional[str] = Field(None, description="The ID of the next node to execute.")

# --- Workflow and Execution Models ---

class WorkflowTrigger(BaseModel):
    """Defines the trigger type for a workflow."""
    type: Literal["manual", "webhook", "cron"] = "manual"

class Workflow(BaseModel):
    """The complete workflow definition."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    is_active: bool = True
    trigger: WorkflowTrigger
    nodes: Dict[str, Node] = Field(description="Dictionary of nodes keyed by ID.")
    start_node_id: Optional[str] = Field(None, description="The ID of the first action node to execute.")

class Execution(BaseModel):
    """Record of a workflow execution."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    workflow_id: str
    trigger_type: Literal["manual", "webhook"]
    status: Literal["running", "success", "failed"] = "running"
    input_data: Dict[str, Any]
    log: List[str] = []
    start_time: float = Field(default_factory=time.time)
    end_time: Optional[float] = None
    duration: Optional[float] = None
