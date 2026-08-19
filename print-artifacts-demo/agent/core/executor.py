from agent.models.mock_llm import MockLLMPlanner
from agent.policies.permissions import require_permission
from agent.tools.registry import TOOLS
from agent.core.state import initial_state
from agent.memory.checkpoint_store import save


def run(task):
    state = initial_state(task)
    for tool_name, args in MockLLMPlanner().plan(task)[:state["max_steps"]]:
        require_permission(tool_name)
        result = TOOLS[tool_name](**args)
        state["steps"].append({"tool": tool_name, "args": args, "result": result})
    state["answer"] = "Two room-nights are available. Total: $240.00."
    save("demo-run", state)
    return state
