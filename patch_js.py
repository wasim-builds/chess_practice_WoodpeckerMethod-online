import re

with open('index.html', 'r') as f:
    html = f.read()

# Replace all of the interaction and flow control logic
new_js = """
        // ---- Interaction logic ----
        let selectedSq = -1;
        let isDragging = false;

        function getSquareFromEvent(e) {
            const boardRect = boardEl.getBoundingClientRect();
            if (e.clientX >= boardRect.left && e.clientX <= boardRect.right && 
                e.clientY >= boardRect.top && e.clientY <= boardRect.bottom) {
                const file = Math.floor((e.clientX - boardRect.left) / (boardRect.width / 8));
                const rank = Math.floor((e.clientY - boardRect.top) / (boardRect.height / 8));
                return rank * 8 + file;
            }
            return -1;
        }

        function onBoardMouseDown(e) {
            if (!playerTurnToMove) return;
            
            // Allow clicking either on a piece or the board directly
            const targetSq = getSquareFromEvent(e);
            if (targetSq === -1) return;
            
            const piece = engine.board[targetSq];
            
            if (selectedSq !== -1 && (!piece || piece.color !== engine.turn)) {
                // Click-to-move
                attemptMove(selectedSq, targetSq);
                selectedSq = -1;
                document.querySelectorAll('.square').forEach(el => el.classList.remove('legal-move', 'capture'));
                return;
            }

            if (piece && piece.color === engine.turn) {
                dragSourceSq = targetSq;
                isDragging = false;
                
                const moves = engine.generateLegalMoves().filter(m => m.from === targetSq);
                highlightLegalMoves(moves);
                
                // Grab the DOM element
                dragElement = pieceElements[dragSourceSq];
            }
        }

        function onDocumentMouseMove(e) {
            if (dragSourceSq === -1 || !dragElement) return;
            
            if (!isDragging) {
                isDragging = true;
                dragElement.style.transition = 'none'; // disable animation while dragging
                dragElement.style.zIndex = '1000';
            }
            
            if (isDragging) {
                // Center the piece on the mouse
                const boardRect = boardEl.getBoundingClientRect();
                const pieceWidth = boardRect.width / 8;
                
                let x = e.clientX - boardRect.left - (pieceWidth / 2);
                let y = e.clientY - boardRect.top - (pieceWidth / 2);
                
                // Keep within reasonable bounds
                dragElement.style.transform = `translate(${x}px, ${y}px)`;
            }
        }

        function onDocumentMouseUp(e) {
            if (dragSourceSq === -1 || !dragElement) return;
            
            const targetSq = getSquareFromEvent(e);

            if (isDragging) {
                dragElement.style.transition = 'transform 0.2s ease';
                dragElement.style.zIndex = '10';
                
                if (targetSq !== -1 && targetSq !== dragSourceSq) {
                    const moved = attemptMove(dragSourceSq, targetSq);
                    if (!moved) {
                        // Snap back
                        dragElement.style.transform = getSquareTransform(dragSourceSq);
                    }
                    document.querySelectorAll('.square').forEach(sq => sq.classList.remove('legal-move', 'capture'));
                    selectedSq = -1;
                } else {
                    dragElement.style.transform = getSquareTransform(dragSourceSq);
                    if (targetSq === dragSourceSq) selectedSq = dragSourceSq;
                    else {
                        document.querySelectorAll('.square').forEach(sq => sq.classList.remove('legal-move', 'capture'));
                        selectedSq = -1;
                    }
                }
            } else {
                // Just a click
                if (targetSq === dragSourceSq) {
                    if (selectedSq === dragSourceSq) {
                        selectedSq = -1;
                        document.querySelectorAll('.square').forEach(sq => sq.classList.remove('legal-move', 'capture'));
                    } else {
                        selectedSq = dragSourceSq;
                    }
                }
            }
            
            dragSourceSq = -1;
            isDragging = false;
            dragElement = null;
        }

        // Animate DOM piece from one square to another, handling captures
        function animatePieceMove(fromSq, toSq, promotion = null, isCastling = null) {
            const pDiv = pieceElements[fromSq];
            if (!pDiv) return;
            
            // Handle capture
            if (pieceElements[toSq]) {
                const captured = pieceElements[toSq];
                setTimeout(() => captured.remove(), 200); // Wait for transition
            }
            // Update tracking
            pieceElements[toSq] = pDiv;
            delete pieceElements[fromSq];
            pDiv.dataset.sq = toSq;
            pDiv.style.transform = getSquareTransform(toSq);
            
            if (promotion) {
                const color = pDiv.className.split(' ')[1][0]; // get 'w' or 'b'
                setTimeout(() => {
                    pDiv.className = `piece ${color}${promotion}`;
                }, 200);
            }
            
            if (isCastling === 'castle_k') {
                const rFrom = toSq + 1;
                const rTo = toSq - 1;
                const rDiv = pieceElements[rFrom];
                if (rDiv) {
                    pieceElements[rTo] = rDiv;
                    delete pieceElements[rFrom];
                    rDiv.dataset.sq = rTo;
                    rDiv.style.transform = getSquareTransform(rTo);
                }
            } else if (isCastling === 'castle_q') {
                const rFrom = toSq - 2;
                const rTo = toSq + 1;
                const rDiv = pieceElements[rFrom];
                if (rDiv) {
                    pieceElements[rTo] = rDiv;
                    delete pieceElements[rFrom];
                    rDiv.dataset.sq = rTo;
                    rDiv.style.transform = getSquareTransform(rTo);
                }
            }
        }

        function attemptMove(fromSq, toSq) {
            if (!playerTurnToMove) return false;

            const legalMoves = engine.generateLegalMoves();
            let moveObj = legalMoves.find(m => m.from === fromSq && m.to === toSq && !m.promotion);
            if (!moveObj) {
                moveObj = legalMoves.find(m => m.from === fromSq && m.to === toSq && m.promotion === 'q');
            }

            if (!moveObj) return false;

            const uciMove = engine.moveToUCI(moveObj);
            const expectedMove = currentPuzzle.solution[moveIndex];

            if (uciMove === expectedMove) {
                // Correct Move!
                animatePieceMove(moveObj.from, moveObj.to, moveObj.promotion, moveObj.type);
                engine.makeMoveInternal(moveObj);
                
                lastMoveSquares = [moveObj.from, moveObj.to];
                renderBoard(false); // updates highlights only since fullRedraw is false
                flashBoard('correct');
                
                moveIndex++;
                if (moveIndex >= currentPuzzle.solution.length) {
                    playerTurnToMove = false;
                    setStatus("Correct! ✓", "correct");
                    
                    const status = appState.puzzleStatuses[currentPuzzle.id];
                    if (status !== 'solved_with_hint' && status !== 'failed') {
                        appState.puzzleStatuses[currentPuzzle.id] = 'solved';
                    }
                    storage.saveState(appState);
                    updateStats();
                } else {
                    playerTurnToMove = false;
                    setStatus("Opponent is thinking...", "");
                    setTimeout(playOpponentMove, 500);
                }
                return true;
            } else {
                // Wrong move
                flashBoard('wrong');
                setStatus("Wrong move, try again.", "wrong");
                appState.puzzleStatuses[currentPuzzle.id] = 'failed';
                storage.saveState(appState);
                updateStats();
                return false;
            }
        }

        function playOpponentMove() {
            const oppUci = currentPuzzle.solution[moveIndex];
            const moveObj = engine.makeMoveUCI(oppUci);
            
            if (moveObj) {
                animatePieceMove(moveObj.from, moveObj.to, moveObj.promotion, moveObj.type);
                lastMoveSquares = [moveObj.from, moveObj.to];
                renderBoard(false);
                moveIndex++;
                playerTurnToMove = true;
                
                if (moveIndex >= currentPuzzle.solution.length) {
                    playerTurnToMove = false;
                    setStatus("Correct! ✓", "correct");
                    const status = appState.puzzleStatuses[currentPuzzle.id];
                    if (status !== 'solved_with_hint' && status !== 'failed') {
                        appState.puzzleStatuses[currentPuzzle.id] = 'solved';
                    }
                    storage.saveState(appState);
                    updateStats();
                } else {
                    setStatus("Your turn.", "info");
                }
            } else {
                console.error("Invalid opponent move in solution: " + oppUci);
            }
        }

        // ---- Flow Control ----

        function loadPuzzleIndex(idx) {
            if (idx < 0) idx = 0;
            if (idx >= puzzles.length) idx = puzzles.length - 1;
            
            appState.currentPuzzleIndex = idx;
            storage.saveState(appState);
            
            currentPuzzle = puzzles[idx];
            moveIndex = 0;
            currentPuzzleTimeMs = 0;
            lastMoveSquares = [];
            
            engine.loadFEN(currentPuzzle.fen);
            playerTurnToMove = true;
            
            document.getElementById('puzzle-number').textContent = `Puzzle ${idx + 1} / ${puzzles.length}`;
            
            const turnInd = document.getElementById('turn-indicator');
            turnInd.textContent = engine.turn === 'w' ? 'White to move' : 'Black to move';
            turnInd.className = `turn-indicator ${engine.turn === 'w' ? 'white' : 'black'}`;
            
            setStatus("Ready", "");
            
            renderBoard(true); // Full redraw to render pieces from scratch
            updateStats();
        }

        function showSolution() {
            if (!currentPuzzle) return;
            appState.puzzleStatuses[currentPuzzle.id] = 'solved_with_hint';
            storage.saveState(appState);
            updateStats();
            
            engine.loadFEN(currentPuzzle.fen);
            lastMoveSquares = [];
            renderBoard(true);
            
            setStatus("Solution shown.", "warning");
            playerTurnToMove = false;
            
            let tempIndex = 0;
            const playNextHintMove = () => {
                if (tempIndex < currentPuzzle.solution.length) {
                    const uci = currentPuzzle.solution[tempIndex];
                    const m = engine.makeMoveUCI(uci);
                    if (m) {
                        animatePieceMove(m.from, m.to, m.promotion, m.type);
                        lastMoveSquares = [m.from, m.to];
                    }
                    renderBoard(false);
                    tempIndex++;
                    setTimeout(playNextHintMove, 500);
                }
            };
            playNextHintMove();
        }
"""

# Now replace everything from '// ---- Interaction logic ----' up to 'function resumeUnsolved()'
html = re.sub(r'// ---- Interaction logic ----.*?function resumeUnsolved\(\)', new_js + "\n        function resumeUnsolved()", html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
print("Applied JS logic patch.")
