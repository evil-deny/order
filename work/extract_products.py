from pathlib import Path
import json
import re

source = Path(r"C:\Users\煞氣\Desktop\煞氣\index.html")
text = source.read_text(encoding="utf-8")

pattern = re.compile(
    r'\{\s*category:\s*"(?P<cat>.*?)",\s*'
    r'name:\s*"(?P<name>.*?)",\s*'
    r'price:\s*(?P<price>\d+),\s*'
    r'stock:\s*(?P<stock>null|\d+),\s*'
    r'image:\s*"(?P<img>.*?)"\s*\}',
    re.S,
)

items = []
for index, match in enumerate(pattern.finditer(text)):
    item = match.groupdict()
    item["id"] = f"p{index + 1}"
    item["category"] = item.pop("cat").strip()
    item["name"] = item["name"].strip()
    item["price"] = int(item["price"])
    item["stock"] = None if item["stock"] == "null" else int(item["stock"])
    item["image"] = item.pop("img").strip()
    items.append(item)

print(len(items))
print(json.dumps(items[:8], ensure_ascii=False, indent=2))
