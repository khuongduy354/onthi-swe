import json
from urllib.request import Request, urlopen


class OllamaPlanner:
    """Optional real LLM adapter; MockLLMPlanner keeps the exam demo offline."""

    def __init__(self, model="qwen2.5:0.5b", endpoint="http://localhost:11434/api/generate"):
        self.model = model
        self.endpoint = endpoint

    def complete(self, prompt):
        body = json.dumps({"model": self.model, "prompt": prompt, "stream": False}).encode()
        request = Request(self.endpoint, data=body, headers={"Content-Type": "application/json"})
        return json.loads(urlopen(request, timeout=30).read())["response"]

