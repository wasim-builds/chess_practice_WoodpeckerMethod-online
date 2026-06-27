import json

with open('puzzles_data.json', 'r') as f:
    puzzles = json.load(f)

zero_moves = 0
for p in puzzles:
    if len(p['solution']) == 0:
        zero_moves += 1
        print(f"Puzzle {p['id']} has 0 moves")

print(f"Total zero moves: {zero_moves}")
