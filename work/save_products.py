from pathlib import Path
import json
import re

html = Path("outputs/index.html").read_text(encoding="utf-8")
match = re.search(r"const PRODUCTS = (\[.*?\]);\n", html, re.S)
if not match:
    raise SystemExit("PRODUCTS not found")

products = json.loads(match.group(1))
Path("work/products.json").write_text(
    json.dumps(products, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print(f"Saved {len(products)} products")
