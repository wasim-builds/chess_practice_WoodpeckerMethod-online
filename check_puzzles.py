import json

with open('puzzles_data.json', 'r') as f:
    puzzles = json.load(f)

print(f"Total puzzles: {len(puzzles)}")

short_solutions = 0
for p in puzzles:
    if len(p['solution']) < 2:
        short_solutions += 1
        print(f"Puzzle {p['id']} ({p['category']}) has {len(p['solution'])} moves: {p['solution']}")

print(f"\nTotal short solutions (<2 moves): {short_solutions}")
