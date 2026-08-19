import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
content = json.loads((ROOT / "src/content/site.json").read_text())
template = (ROOT / "src/pages/index.html").read_text()
for key, value in content.items():
    template = template.replace("{{ " + key + " }}", value)
(ROOT / "dist").mkdir(exist_ok=True)
(ROOT / "dist/index.html").write_text(template)

