import uuid
from typing import Any, Dict


def gen_secret():
return uuid.uuid4().hex


async def run_nodes(nodes: list, context: Dict[str, Any]):
"""Simple sequential node runner.
Each node is dict: {"type": "action", "action": "send_telegram", "config": {...}}
"""
from .actions import action_dispatch
results = []
for node in nodes:
if node.get("type") == "action":
fn = node.get("action")
cfg = node.get("config", {})
res = await action_dispatch(fn, cfg, context)
results.append(res)
return results