# ♟️ Woodpecker Method Chess Trainer & PGN Puzzle Engine

[![GitHub Pages](https://img.shields.io/badge/Live-GitHub%20Pages-brightgreen?style=flat-square&logo=github)](https://wasim-builds.github.io/chess_practice_WoodpeckerMethod-online/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)

An interactive, zero-latency web application designed for high-repetition chess tactical training using the **Woodpecker Method**, featuring 1,000+ curated tactical exercises and annotated grandmaster games.

🌐 **Live Web App**: [**wasim-builds.github.io/chess_practice_WoodpeckerMethod-online**](https://wasim-builds.github.io/chess_practice_WoodpeckerMethod-online/)

---

## 🎯 What is the Woodpecker Method?

Developed by GM Axel Smith and GM Hans Tikkanen, the **Woodpecker Method** is a high-intensity training regimen based on spaced repetition. By solving the same set of tactical puzzles in cycles with progressively shorter target times (e.g. 4 weeks → 2 weeks → 1 week → 4 days → 2 days), your subconscious pattern recognition sharpens dramatically, enabling you to spot tactical motifs instantly in over-the-board and blitz games.

---

## ✨ Features

- **⚡ Zero-Latency Movement & Sound**: Instant drag-and-drop and tap-to-move interactions with custom zero-latency piece placement audio.
- **🔄 True Board Orientation**: Automatic perspective synchronization with board-flipper and mathematically aligned rank/file coordinates.
- **🤖 Built-in Engine Analysis**: On-demand Stockfish engine evaluation and candidate move analysis toggleable on every puzzle.
- **♟️ Underpromotion & En-Passant**: Full chess rules engine support including pawn underpromotion (Queen, Rook, Bishop, Knight) and accurate en-passant tracking.
- **📱 Responsive Mobile & Desktop Layout**: Optimized touch support for mobile browsers, tablets, and desktop displays.
- **🎨 Modern Dark / Light Mode**: Clean glassmorphism UI with customizable piece sets and board colors (Wood, Forest Green, Tournament Blue).

---

## 📚 Included Puzzle & Game Collections

1. **Smith A. — The Woodpecker Method 2 (2024)**: 1,004 curated tactical puzzles across all difficulty chapters.
2. **1,300 Annotated Games of Bobby Fischer**: Complete game archive of the 11th World Champion.
3. **2,500 Annotated Games of Mikhail Tal**: The attacking genius and "Magician from Riga".
4. **4,560 Chess Endgames (László Polgár)**: Fundamental theoretical and tactical endgame positions.
5. **Judit Polgár 2,000 Annotated Games**: The strongest female player in chess history.
6. **Polgár 200 Mate Combinations**: Essential checkmating patterns and motifs.
7. **303 Tricky Chess Puzzles**: Sharp tactical traps and combination exercises.
8. **GM Shankland's Lifetime Repertoires**: 1. e4 preparation vs. the French and Caro-Kann.
9. **GM Mihail Marin's Complete Catalan Repertoire**: Positional and strategic opening guide for White.

---

## 🚀 Running Locally

No npm packages, build tools, or databases required. The entire application runs directly in any modern browser:

```bash
# Clone the repository
git clone https://github.com/wasim-builds/chess_practice_WoodpeckerMethod-online.git
cd chess_practice_WoodpeckerMethod-online

# Serve with any static web server (e.g. Python)
python3 -m http.server 8080
```

Open [http://localhost:8080](http://localhost:8080) in your browser.

---

## 🛠️ Tech Stack

- **Frontend**: Vanilla JavaScript (ES6+), HTML5 Canvas & SVG chess piece rendering.
- **Styling**: Modern CSS3 custom properties with glassmorphism and dynamic viewport scaling.
- **Data Engine**: Modular JSON & lightweight JavaScript array serialization for instant client-side puzzle access without network lag.
- **Deployment**: Automated continuous delivery via GitHub Pages.

---

## 📄 License

MIT © [Mohammed Wasim Khan (wasim-builds)](https://github.com/wasim-builds)
