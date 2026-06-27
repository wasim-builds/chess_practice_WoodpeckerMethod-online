import chess.pgn
import json
import glob
import os
import re

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

STARTING_FEN_PREFIX = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
REPERTOIRE_KEYWORDS = ['repertoire', 'catalan', 'opening', 'system', 'defense', 'sicilian']

pgn_files = sorted(glob.glob('*.pgn'))
books_list = []  # list of {key, name} dicts

for pgn_file in pgn_files:
    book_key = os.path.splitext(pgn_file)[0]           # used as JS key & filename
    book_name = book_key.replace('_', ' ').strip()      # human-readable display name
    books_list.append({'key': book_key, 'name': book_name})

    is_repertoire_book = any(kw in book_key.lower() for kw in REPERTOIRE_KEYWORDS)

    puzzles = []
    current_id = 1
    positions_only = 0
    with_moves = 0

    print(f"Parsing: {book_name}")
    with open(pgn_file, 'r', encoding='utf-8', errors='ignore') as f:
        while True:
            try:
                game = chess.pgn.read_game(f)
            except Exception:
                continue
            if game is None:
                break

            fen = game.headers.get("FEN", STARTING_FEN_PREFIX + " w KQkq - 0 1")
            white = game.headers.get("White", "?")
            black = game.headers.get("Black", "?")
            event = game.headers.get("Event", "?")
            annotator = game.headers.get("Annotator", "")

            # Build a clean category label
            if event and event not in ("?", ""):
                # Skip events that are just numbers/codes (e.g. "7/528")
                if re.match(r'^[\d/\.\-]+$', event.strip()):
                    category = f"{white} vs {black}"
                else:
                    category = event if (white == '?' or white == 'Unknown') else f"{event}"
            else:
                category = f"{white} vs {black}"

            moves_uci = []
            try:
                for move in game.mainline_moves():
                    moves_uci.append(move.uci())
            except Exception:
                pass

            # Determine entry type based on FEN and move count
            if len(moves_uci) > 0:
                is_starting_pos = fen.startswith(STARTING_FEN_PREFIX)
                if is_starting_pos and is_repertoire_book:
                    entry_type = "repertoire"
                elif is_starting_pos:
                    entry_type = "game"
                else:
                    entry_type = "puzzle"
                with_moves += 1
            else:
                entry_type = "position"
                positions_only += 1

            puzzles.append({
                "id": current_id,
                "fen": fen,
                "solution": moves_uci,
                "category": category,
                "annotator": annotator,
                "type": entry_type
            })
            current_id += 1

    js_filename = f"data/{book_key}.js"
    with open(js_filename, 'w', encoding='utf-8') as out:
        out.write(f"window.CHESS_BOOKS = window.CHESS_BOOKS || {{}};\n")
        out.write(f"window.CHESS_BOOKS[{json.dumps(book_key)}] = ")
        json.dump(puzzles, out)
        out.write(";\n")
    print(f"  -> {len(puzzles)} entries ({with_moves} with moves, {positions_only} positions) -> {js_filename}")

# Generate the book list file (now stores {key, name} objects)
with open('data/books_list.js', 'w', encoding='utf-8') as out:
    out.write(f"window.CHESS_BOOKS_LIST = {json.dumps(books_list)};\n")
print("Finished parsing all books!")
