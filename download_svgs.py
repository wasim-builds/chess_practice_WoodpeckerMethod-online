import urllib.request
import base64
import os

pieces = ['wK', 'wQ', 'wR', 'wB', 'wN', 'wP', 'bK', 'bQ', 'bR', 'bB', 'bN', 'bP']
css_classes = ""

for p in pieces:
    url = f"https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/cburnett/{p}.svg"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            svg_data = response.read()
            b64 = base64.b64encode(svg_data).decode('utf-8')
            css_classes += f".piece.{p.lower()} {{ background-image: url('data:image/svg+xml;base64,{b64}'); }}\n"
    except Exception as e:
        print(f"Failed to download {p}: {e}")

with open('pieces_css.txt', 'w') as f:
    f.write(css_classes)

print("Generated CSS")
