class MockLLMPlanner:
    """Offline replacement for an LLM that emits structured tool calls."""

    def plan(self, task):
        return [
            ("check_inventory", {"item": "room-night"}),
            ("calculate_total", {"price": 120.0, "quantity": 2}),
        ]

