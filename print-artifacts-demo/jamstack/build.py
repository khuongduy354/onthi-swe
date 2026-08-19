"""Minimal JAMstack build: content becomes pre-rendered HTML in dist/."""
from pathlib import Path

content = "Fast architecture notes delivered as pre-rendered markup."
html = f"<h1>Architecture Notes</h1><p>{content}</p>"
Path(__file__).with_name("dist").mkdir(exist_ok=True)
Path(__file__).with_name("dist").joinpath("index.html").write_text(html)

