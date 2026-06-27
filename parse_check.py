import chess.pgn
import json
with open('Smith A. - The Woodpecker Method 2 (2024) quiz.pgn') as f:
    count = 0
    while True:
        game = chess.pgn.read_game(f)
        if game is None:
            break
        count += 1
print(f"Total games: {count}")
