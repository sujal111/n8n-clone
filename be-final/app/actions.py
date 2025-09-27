


# app/actions.py


```python
import httpx
import asyncio
import os
from .settings import settings


async def action_dispatch(name: str, config: dict, context: dict):
if name == "send_telegram":
return await send_telegram(config, context)
if name == "send_resend_email":
return await send_resend_email(config, context)
if name == "llm":
return await llm_call(config, context)
raise ValueError("unknown action")


async def send_telegram(config: dict, context: dict):
token = config.get("token") or settings.telegram_bot_token
chat_id = config.get("chat_id")
text = config.get("text") or context.get("text")
if not token or not chat_id:
return {"error": "missing token or chat_id"}
url = f"https://api.telegram.org/bot{token}/sendMessage"
async with httpx.AsyncClient() as client:
r = await client.post(url, json={"chat_id": chat_id, "text": text})
return r.json()


async def send_resend_email(config: dict, context: dict):
api_key = config.get("api_key") or settings.resend_api_key
if not api_key:
return {"error": "missing resend api key"}
url = "https://api.resend.com/emails"
payload = {
"from": config.get("from"),
"to": config.get("to"),
"subject": config.get("subject"),
"html": config.get("html") or config.get("text"),
}
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
async with httpx.AsyncClient() as client:
r = await client.post(url, json=payload, headers=headers)
return r.json()


async def llm_call(config: dict, context: dict):
provider = config.get("provider", "openai")
prompt = config.get("prompt") or context.get("prompt")
if provider == "openai":
import openai
openai.api_key = config.get("api_key") or settings.openai_api_key
if not openai.api_key:
return {"error": "missing openai key"}
resp = openai.ChatCompletion.create(
model=config.get("model", "gpt-4o-mini"),
else: