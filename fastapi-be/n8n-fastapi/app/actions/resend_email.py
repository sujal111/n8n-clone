import httpx
from typing import Dict, Any

async def send_resend_email(config: Dict[str, Any], context: Dict[str, Any]):
    """
    config: { "api_key": "...", "from": "on@you.com", "to": ["a@b.com"], "subject": "...", "html": "<p>Hi</p>" }
    """
    api_key = config.get("api_key")
    if not api_key:
        return {"error": "no resend api key"}
    payload = {
        "from": config.get("from"),
        "to": config.get("to"),
        "subject": config.get("subject"),
        "html": config.get("html") or str(context.get("payload"))
    }
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        r = await client.post("https://api.resend.com/emails", json=payload, headers=headers)
    if r.status_code >= 400:
        return {"error": r.text, "status_code": r.status_code}
    return r.json()
