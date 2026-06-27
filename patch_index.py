import re
import json

with open('index.html', 'r') as f:
    html = f.read()

with open('pieces_css.txt', 'r') as f:
    svg_css = f.read()

with open('puzzles_data.json', 'r') as f:
    puzzles_json_str = f.read()

# 1. CSS patches
# Remove unicode colors
html = re.sub(r'/\* Unicode pieces color fix \*/.*?\n.*?\n.*?\n', '', html, flags=re.DOTALL)

# Update .piece
new_piece_css = """
        .piece {
            position: absolute;
            width: 12.5%;
            height: 12.5%;
            background-size: cover;
            z-index: 10;
            transition: transform 0.2s ease;
            cursor: pointer;
            -webkit-user-drag: none;
        }
        .dragging {
            z-index: 1000 !important;
            transition: none !important;
            cursor: grabbing !important;
        }
""" + svg_css

html = re.sub(r'\.piece \{.*?-webkit-user-drag: none;\s*\}', new_piece_css, html, flags=re.DOTALL)

# Remove dragging piece old css
html = re.sub(r'\.dragging \{.*?\}', '', html, flags=re.DOTALL)


# 2. JS patches
# Replace DEFAULT_PUZZLES
html = re.sub(r'const DEFAULT_PUZZLES = \[.*?\];', f'const DEFAULT_PUZZLES = {puzzles_json_str};', html, flags=re.DOTALL)

# Replace pieceUnicode
html = re.sub(r'const pieceUnicode = \{.*?\};', "const pieceClasses = {'wk':'wk','wq':'wq','wr':'wr','wb':'wb','wn':'wn','wp':'wp','bk':'bk','bq':'bq','br':'br','bb':'bb','bn':'bn','bp':'bp'};", html, flags=re.DOTALL)


# Overwrite renderBoard and piece moving logic
# We need to completely replace renderBoard and related interaction to use absolute pieces
new_render_js = """
        // ---- Render Board ----
        
        let lastMoveSquares = [];
        let pieceElements = {}; // track DOM elements by a unique id or square
        
        function getSquareTransform(sq) {
            const file = sq % 8;
            const rank = Math.floor(sq / 8);
            return `translate(${file * 100}%, ${rank * 100}%)`;
        }

        function createSquares() {
            boardEl.innerHTML = '';
            for (let rank = 0; rank < 8; rank++) {
                for (let file = 0; file < 8; file++) {
                    const sq = rank * 8 + file;
                    const isLight = (rank + file) % 2 === 0;
                    const div = document.createElement('div');
                    div.className = `square ${isLight ? 'light' : 'dark'}`;
                    div.dataset.sq = sq;
                    boardEl.appendChild(div);
                }
            }
        }

        function renderBoard(fullRedraw = false) {
            if (boardEl.children.length === 0) createSquares();
            
            // Clear highlights
            document.querySelectorAll('.square').forEach(el => {
                el.classList.remove('highlight-last');
            });
            lastMoveSquares.forEach(sq => {
                const el = document.querySelector(`.square[data-sq="${sq}"]`);
                if(el) el.classList.add('highlight-last');
            });

            if (fullRedraw) {
                // Remove all piece elements
                document.querySelectorAll('.piece').forEach(el => el.remove());
                pieceElements = {};
                
                for (let sq = 0; sq < 64; sq++) {
                    const piece = engine.board[sq];
                    if (piece) {
                        const pDiv = document.createElement('div');
                        const cls = piece.color + piece.type;
                        pDiv.className = `piece ${cls}`;
                        pDiv.dataset.sq = sq;
                        pDiv.style.transform = getSquareTransform(sq);
                        boardEl.appendChild(pDiv);
                        pieceElements[sq] = pDiv;
                    }
                }
            } else {
                // Sync pieces to board state
                const currentBoard = engine.board;
                // Identify what needs to be added, removed, or moved
                // Since this is called after a move, we just rebuild if it's too complex
                // But for animation, it's better to update transform directly in attemptMove/playOpponentMove
                // Wait, if we just call fullRedraw = true on loadFEN, and let the move functions handle DOM updates, we get animations!
            }
        }
        
        // We redefine attemptMove and playOpponentMove below...
"""

# Replace renderBoard
html = re.sub(r'let lastMoveSquares = \[\];\s*function renderBoard\(\) \{.*?\}(?=\s*function highlightLegalMoves)', new_render_js, html, flags=re.DOTALL)


# We need to inject the DOM updates into attemptMove and playOpponentMove
# The easiest way is to fully replace the script tags or specific functions.

with open('index.html', 'w') as f:
    f.write(html)
print("Applied initial patches.")
