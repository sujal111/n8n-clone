import time
from typing import Dict, Any, List

from app.models import Node, Execution
from app.services import ActionService
from app.models import TelegramActionData, ResendActionData, LLMActionData
from app.db.inmemory import WORKFLOWS_DB, EXECUTIONS_DB

# ----------------------------------------------------------------------
# Workflow Execution Engine (Background Task)
# ----------------------------------------------------------------------

def execute_workflow_in_background(workflow_id: str, input_data: Dict[str, Any], trigger_type: str):
    """
    The core asynchronous execution logic.
    Runs as a decoupled background task (simulating an external worker/queue).
    """
    workflow = WORKFLOWS_DB.get(workflow_id)
    if not workflow or not workflow.get('is_active'):
        print(f"Workflow {workflow_id} not found or inactive.")
        return

    # 1. Create initial Execution record
    execution = Execution(
        workflow_id=workflow_id,
        trigger_type=trigger_type,
        input_data=input_data
    )
    EXECUTIONS_DB[execution.id] = execution.dict()
    print(f"--- Workflow {workflow_id} started (Execution ID: {execution.id}) ---")

    current_node_id = workflow.get('start_node_id')
    success = True

    try:
        # 2. Start node traversal
        while current_node_id:
            node_data = workflow['nodes'].get(current_node_id)
            if not node_data:
                execution.log.append(f"Error: Node ID {current_node_id} not found.")
                success = False
                break

            node = Node(**node_data)
            log_message = ""

            # Dispatch action based on node type
            if node.type == "telegram":
                action_data = TelegramActionData(**node.data)
                log_message = ActionService.execute_telegram(action_data, execution.id)
            elif node.type == "resend":
                action_data = ResendActionData(**node.data)
                log_message = ActionService.execute_resend(action_data, execution.id)
            elif node.type == "llm":
                action_data = LLMActionData(**node.data)
                log_message = ActionService.execute_llm(action_data, execution.id)
            else:
                log_message = f"Warning: Unknown node type {node.type}. Skipping."

            execution.log.append(log_message)
            print(f"  -> {log_message}") # Print log step

            if "Failed" in log_message:
                success = False
                break

            # Move to the next node
            current_node_id = node.next

    except Exception as e:
        execution.log.append(f"CRITICAL ERROR during execution: {e}")
        success = False

    finally:
        # 3. Finalize Execution record
        execution.end_time = time.time()
        execution.duration = execution.end_time - execution.start_time
        execution.status = "success" if success else "failed"

        EXECUTIONS_DB[execution.id] = execution.dict()
        print(f"--- Workflow {workflow_id} execution finished: {execution.status} (Duration: {execution.duration:.2f}s) ---")
