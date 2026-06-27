const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const engineCode = html.substring(html.indexOf('class ChessEngine'), html.indexOf('const engine = new ChessEngine()'));
eval(engineCode);
const content = fs.readFileSync('data/Play_The_Catalan_Complete_Repertoire_for_White_Part_1_by_GM_Mihail.js', 'utf8');
const lines = content.split('\n');
const jsonStr = lines[1].substring(lines[1].indexOf('['), lines[1].length - 1);
const arr = JSON.parse(jsonStr);
const engine = new ChessEngine();
engine.loadFEN(arr[0].fen);
for (let uci of arr[0].solution) {
    const move = engine.makeMoveUCI(uci);
    if (!move) {
        console.log('Failed at:', uci, 'FEN:', engine.getFEN());
        console.log('Legal moves:', engine.generateLegalMoves().map(m => engine.moveToUCI(m)));
        break;
    }
}
console.log('Done.');
