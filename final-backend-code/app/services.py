import time
from typing import Dict, Any

from app.models import (
    TelegramCreds, ResendCreds, LLMCreds,
    TelegramActionData, ResendActionData, LLMActionData
)
from app.db.inmemory import CREDENTIALS_DB

# ----------------------------------------------------------------------
# Action Services (Core Logic for External APIs)
# ----------------------------------------------------------------------

class ActionService:
    """Simulates the service layer for executing external API calls."""

    @staticmethod
    def get_creds(credential_id: str):
        """Retrieves and validates credentials."""
        creds = CREDENTIALS_DB.get(credential_id)
        if not creds:
            raise ValueError(f"Credential ID '{credential_id}' not found.")
        return creds

    @staticmethod
    def execute_telegram(data: TelegramActionData, execution_id: str) -> str:
        """Mocks sending a Telegram message."""
        try:
            creds = TelegramCreds(**ActionService.get_creds(data.credential_id)['data'])
            # Simulate network latency
            time.sleep(0.1)
            # Mock API call using the credentials
            log = (f"[Execution {execution_id}] Telegram Action Success: "
                   f"Using Bot: {creds.bot_token[:8]}... "
                   f"Sent message '{data.message}' to Chat ID: {creds.chat_id}.")
            return log
        except Exception as e:
            return f"[Execution {execution_id}] Telegram Action Failed: {e}"

    @staticmethod
    def execute_resend(data: ResendActionData, execution_id: str) -> str:
        """Mocks sending an email via Resend."""
        try:
            creds = ResendCreds(**ActionService.get_creds(data.credential_id)['data'])
            # Simulate network latency
            time.sleep(0.1)
            # Mock API call using the credentials
            log = (f"[Execution {execution_id}] Resend Action Success: "
                   f"Using Key: {creds.api_key[:8]}... "
                   f"Sent '{data.subject}' from '{creds.sender_email}' to '{data.to}'.")
            return log
        except Exception as e:
            return f"[Execution {execution_id}] Resend Action Failed: {e}"

    @staticmethod
    def execute_llm(data: LLMActionData, execution_id: str) -> str:
        """Mocks calling an LLM API (DIFFICULT feature placeholder)."""
        try:
            creds = LLMCreds(**ActionService.get_creds(data.credential_id)['data'])
            # Simulate LLM processing time
            time.sleep(0.3)
            # In a real app, this would be an API call to Gemini/Anthropic
            response = f"LLM generated response for prompt: '{data.prompt[:30]}...'"
            log = (f"[Execution {execution_id}] LLM Action Success: "
                   f"Using Model: {creds.model_name}. Response: {response}")
            return log
        except Exception as e:
            return f"[Execution {execution_id}] LLM Action Failed: {e}"
