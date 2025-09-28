import httpx
from typing import Dict, Any

async def send_telegram_message(config: Dict[str, Any], context: Dict[str, Any]):
    """
    config: { "credential_name": "my-tg", "chat_id": "...", "text": "Hello {{payload.foo}}" }
    """
    cred = config.get("credential") or config.get("credential_name")
    # For demo, we expect full token in config; in prod lookup from DB
    token = config.get("token")
    if not token:
        return {"error": "no telegram token provided"}
    chat_id = config.get("chat_id")
    text = config.get("text") or str(context.get("payload"))
    # basic templating
    if "{{payload" in text:
        try:
            text = text.replace("{{payload}}", str(context.get("payload")))
        except:
            pass
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    async with httpx.AsyncClient() as client:
        r = await client.post(url, json={"chat_id": chat_id, "text": text})
    if r.status_code >= 400:
        return {"error": r.text, "status_code": r.status_code}
    return r.json()
