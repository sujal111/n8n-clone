

# README (quick start)


```
1. copy .env.example to .env and fill keys
2. pip install -r requirements.txt
3. uvicorn app.main:app --reload


Endpoints:
- POST /workflows {name, trigger_type, nodes, cron_expr?, webhook_secret?}
- POST /workflows/{id}/run -> manual
- POST /webhook/{secret} -> webhook trigger
- GET /workflows


Node action examples (in workflow.nodes):
[
{"type": "action", "action": "send_telegram", "config": {"chat_id":"123", "text":"hello"}},
{"type": "action", "action": "send_resend_email", "config": {"from":"a@b.com","to":"c@d.com","subject":"hi","text":"body"}},
{"type": "action", "action": "llm", "config": {"provider":"openai","prompt":"Say hi"}}
]
```


---


# Notes and next steps


- This is a minimal but extendable scaffold. For production, add:
- Authentication & per-user/workflow isolation
- Persistent task queue (Celery/RQ) for reliability
- Retries, concurrency controls, node inputs/outputs, branching, and node-level logging
- UI to author workflows




---