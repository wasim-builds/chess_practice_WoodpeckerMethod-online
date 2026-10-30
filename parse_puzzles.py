import chess.pgn
import json
import glob
import os
import re

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

STARTING_FEN_PREFIX = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
REPERTOIRE_KEYWORDS = ['repertoire', 'catalan', 'opening', 'system', 'defense', 'sicilian']

pgn_files = sorted(glob.glob('*.pgn'), key=lambda f: (0 if 'woodpecker' in f.lower() else 1, f))
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

    # Special handling for Woodpecker 2 quiz PGN to extract clean, ordered 1004 puzzles
    if "Woodpecker Method 2" in book_name:
        import io
        with open(pgn_file, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()

        games_raw = re.split(r'\n(?=\[Event )', text)
        games_by_black = {}
        for g in games_raw:
            b_m = re.search(r'\[Black \"([^\"]*)\"\]', g)
            if b_m:
                b = b_m.group(1)
                if b in games_by_black:
                    if isinstance(games_by_black[b], list):
                        games_by_black[b].append(g)
                    else:
                        games_by_black[b] = [games_by_black[b], g]
                else:
                    games_by_black[b] = g

        def extract_clean_moves(game, fen_str):
            if not game:
                return []
            b = chess.Board(fen_str)
            m_list = []
            for move in game.mainline_moves():
                if move in b.legal_moves:
                    b.push(move)
                    m_list.append(move.uci())
                else:
                    break
            return m_list

        # 1. Add exercises 1 to 1000 in exact order
        for i in range(1, 1001):
            sol_key = f'solution ex {i}'
            if sol_key in games_by_black:
                raw = games_by_black[sol_key]
                g = chess.pgn.read_game(io.StringIO(raw))
                fen = g.headers.get('FEN')
                event = g.headers.get('Event', f'Chapter {i}')
                moves = extract_clean_moves(g, fen)
                puzzles.append({
                    'id': current_id,
                    'fen': fen,
                    'solution': moves,
                    'category': event,
                    'annotator': g.headers.get('Annotator', ''),
                    'type': 'puzzle'
                })
                with_moves += 1
                current_id += 1

        # 2. Add Example 1 (Bonus puzzle 1001)
        if 'solution Example 1' in games_by_black:
            g = chess.pgn.read_game(io.StringIO(games_by_black['solution Example 1']))
            fen = g.headers.get('FEN')
            moves = extract_clean_moves(g, fen)
            puzzles.append({
                'id': current_id,
                'fen': fen,
                'solution': moves,
                'category': 'Example 1 (Intro)',
                'annotator': '',
                'type': 'puzzle'
            })
            with_moves += 1
            current_id += 1

        # 3. Add Example 2 (Bonus puzzle 1002)
        if 'solution Example 2' in games_by_black:
            g = chess.pgn.read_game(io.StringIO(games_by_black['solution Example 2']))
            fen = g.headers.get('FEN')
            moves = extract_clean_moves(g, fen)
            puzzles.append({
                'id': current_id,
                'fen': fen,
                'solution': moves,
                'category': 'Example 2 (Intro)',
                'annotator': '',
                'type': 'puzzle'
            })
            with_moves += 1
            current_id += 1

        # 4. Add Note ex 325 Part 1 (Bonus puzzle 1003)
        if 'note ex 325' in games_by_black:
            notes = games_by_black['note ex 325']
            note_1 = notes[0] if isinstance(notes, list) else notes
            g = chess.pgn.read_game(io.StringIO(note_1))
            fen = g.headers.get('FEN')
            moves = extract_clean_moves(g, fen)
            puzzles.append({
                'id': current_id,
                'fen': fen,
                'solution': moves,
                'category': 'Bonus: Ex 325 Variation',
                'annotator': '',
                'type': 'puzzle'
            })
            with_moves += 1
            current_id += 1

            # 5. Add Note ex 325 Part 2 (Bonus puzzle 1004)
            if isinstance(notes, list) and len(notes) > 1:
                g = chess.pgn.read_game(io.StringIO(notes[1]))
                fen = g.headers.get('FEN')
                moves = extract_clean_moves(g, fen)
                puzzles.append({
                    'id': current_id,
                    'fen': fen,
                    'solution': moves,
                    'category': 'Bonus: English Line',
                    'annotator': '',
                    'type': 'puzzle'
                })
                with_moves += 1
                current_id += 1
    else:
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
                    b = chess.Board(fen)
                    for move in game.mainline_moves():
                        if move in b.legal_moves:
                            b.push(move)
                            moves_uci.append(move.uci())
                        else:
                            break
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
