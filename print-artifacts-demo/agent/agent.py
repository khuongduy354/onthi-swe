"""Offline agent demo. MockLLMPlanner replaces a hosted LLM, tools are real functions."""


def check_inventory(item):
    return {"item": item, "available": True, "units": 8}


def calculate_total(price, quantity):
    return round(price * quantity, 2)


class MockLLMPlanner:
    def plan(self, task):
        return [
            ("check_inventory", {"item": "room-night"}),
            ("calculate_total", {"price": 120.0, "quantity": 2}),
        ]


def run(task):
    steps = []
    for tool, args in MockLLMPlanner().plan(task):
        result = check_inventory(**args) if tool == "check_inventory" else calculate_total(**args)
        steps.append({"tool": tool, "args": args, "result": result})
    return {"task": task, "steps": steps, "answer": "Two room-nights are available. Total: $240.00."}

