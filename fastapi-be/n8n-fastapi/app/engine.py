import asyncio
from typing import Dict, Any
from app.actions.telegram import send_telegram_message
from app.actions.resend_email import send_resend_email
from app.actions.llm_provider import LLMProvider

# node types: action, trigger. action types: telegram, resend_email, llm
async def execute_node(node: Dict[str, Any], context: Dict[str, Any]):
    node_type = node.get("type")
    config = node.get("config", {})
    if node_type == "action":
        action = node.get("action")
        if action == "telegram_send":
            return await send_telegram_message(config, context)
        elif action == "resend_send":
            return await send_resend_email(config, context)
        elif action == "llm_call":
            provider = config.get("provider", "openai")
            prompt = config.get("prompt") or context.get("payload", "")
            llm = LLMProvider(provider_name=provider)
            return await llm.generate(prompt, config.get("params", {}))
        else:
            return {"error": f"unknown action {action}"}
    elif node_type == "trigger":
        return {"status": "triggered", "info": config}
    else:
        return {"error": "unknown node type"}

async def run_workflow(spec: Dict[str, Any], payload: Dict[str, Any]):
    """
    Very simple runner: expects spec to be:
    { "nodes": { "n1": {...}, "n2": {...} }, "edges": [{"from":"n1","to":"n2"}], "start_node": "n1" }
    Runs breadth-first following edges
    """
    nodes = spec.get("nodes", {})
    edges = spec.get("edges", [])
    adjacency = {}
    for e in edges:
        adjacency.setdefault(e["from"], []).append(e["to"])

    started = spec.get("start_node")
    results = {}
    queue = [started]
    context = {"payload": payload}
    while queue:
        node_id = queue.pop(0)
        node = nodes.get(node_id)
        if not node:
            continue
        res = await execute_node(node, context)
        results[node_id] = res
        # pass result to context for downstream nodes
        context["last_result"] = res
        for nxt in adjacency.get(node_id, []):
            queue.append(nxt)
    return results
