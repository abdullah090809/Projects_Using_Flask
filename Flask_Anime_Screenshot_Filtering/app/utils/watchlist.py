import re

def parse_watchlist(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    entries = []
    pattern = re.compile(r"^\d+\.\s+([\s\S]+?)\s*\((\d+(?:\.\d+)?\/5)\)", re.MULTILINE)

    matches = pattern.finditer(content)
    for match in matches:
        name = match.group(1).replace("\n", " ").strip()
        rating = match.group(2).strip()
        entries.append({
            "name": name,
            "rating": rating
        })

    return entries