const fs = require('fs');

const html = fs.readFileSync('index.html', 'utf8');
const engineCode = html.substring(html.indexOf('class ChessEngine'), html.indexOf('const engine = new ChessEngine()'));
eval('global.ChessEngine = ' + engineCode.replace('class ChessEngine', 'class'));

const engine = new global.ChessEngine();

// 1. Test puzzles_data.json
console.log('=== Testing puzzles_data.json (1,000 puzzles) ===');
const puzzles1000 = JSON.parse(fs.readFileSync('puzzles_data.json', 'utf8'));
let failed1000 = 0;
for (const p of puzzles1000) {
    if (!p.solution || p.solution.length === 0) {
        failed1000++;
        console.log('Zero moves in puzzle ' + p.id);
        continue;
    }
    engine.loadFEN(p.fen);
    for (const uci of p.solution) {
        const move = engine.makeMoveUCI(uci);
        if (!move) {
            failed1000++;
            console.log('Failed move in puzzle ' + p.id + ': ' + uci + ' on FEN: ' + p.fen);
            break;
        }
    }
}
console.log(`puzzles_data.json results: ${puzzles1000.length - failed1000} / ${puzzles1000.length} passed! (failed: ${failed1000})`);

// 2. Test current Smith quiz.js
console.log('\n=== Testing data/Smith A. - The Woodpecker Method 2 (2024) quiz.js ===');
const quizContent = fs.readFileSync('data/Smith A. - The Woodpecker Method 2 (2024) quiz.js', 'utf8');
const lines = quizContent.split('\n');
const jsonPart = lines[1].substring(lines[1].indexOf('=') + 1).trim().replace(/;$/, '');
const quizData = JSON.parse(jsonPart);
let failedQuiz = 0;
let zeroMoves = 0;
for (const p of quizData) {
    if (!p.solution || p.solution.length === 0) {
        zeroMoves++;
        failedQuiz++;
        console.log(`Zero moves in quiz entry ID ${p.id} (Category: ${p.category})`);
        continue;
    }
    engine.loadFEN(p.fen);
    for (const uci of p.solution) {
        const move = engine.makeMoveUCI(uci);
        if (!move) {
            failedQuiz++;
            console.log(`Failed move in quiz entry ID ${p.id}: ${uci} on FEN: ${p.fen}`);
            break;
        }
    }
}
console.log(`current quiz.js results: ${quizData.length - failedQuiz} / ${quizData.length} passed! (zero moves: ${zeroMoves}, failed: ${failedQuiz})`);
