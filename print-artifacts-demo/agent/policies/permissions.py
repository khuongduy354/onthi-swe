ALLOWED_TOOLS = {"check_inventory", "calculate_total"}


def require_permission(tool_name):
    if tool_name not in ALLOWED_TOOLS:
        raise PermissionError(f"Tool is not allowed: {tool_name}")

