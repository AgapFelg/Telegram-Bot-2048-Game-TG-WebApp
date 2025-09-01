document.addEventListener('DOMContentLoaded', () => {
    const gridSize = 4;
    let grid = [];
    let score = 0;
    let bestScore = localStorage.getItem('bestScore') || 0;
    let gameOver = false;
    let gameWon = false;
    let isClassicTheme = false;

    const gameBoard = document.getElementById('game-board');
    const scoreDisplay = document.getElementById('score');
    const bestScoreDisplay = document.getElementById('best-score');
    const gameOverMessage = document.getElementById('game-over');
    const gameWonMessage = document.getElementById('game-won');
    const restartButton = document.getElementById('restart');
    const themeToggle = document.getElementById('theme-toggle');

    const upButton = document.getElementById('up');
    const downButton = document.getElementById('down');
    const leftButton = document.getElementById('left');
    const rightButton = document.getElementById('right');

    function initGame() {
        createGrid();
        setupSwipeEvents();
        addButtonListeners();
        resetGame();
        updateBestScore();
    }

    function createGrid() {
        gameBoard.innerHTML = '';

        for (let i = 0; i < gridSize * gridSize; i++) {
            const cell = document.createElement('div');
            cell.classList.add('grid-cell');
            gameBoard.appendChild(cell);
        }

        grid = Array(gridSize).fill().map(() => Array(gridSize).fill(0));
    }

    function addTile() {
        const emptyCells = [];

        for (let row = 0; row < gridSize; row++) {
            for (let col = 0; col < gridSize; col++) {
                if (grid[row][col] === 0) {
                    emptyCells.push({ row, col });
                }
            }
        }

        if (emptyCells.length > 0) {
            const randomCell = emptyCells[Math.floor(Math.random() * emptyCells.length)];
            grid[randomCell.row][randomCell.col] = Math.random() < 0.9 ? 2 : 4;
            renderTiles();

            if (isGameOver()) {
                endGame();
            }
        }
    }

    function renderTiles() {
        const tiles = document.querySelectorAll('.tile');
        tiles.forEach(tile => tile.remove());

        const cellSize = 100 / gridSize;
        const gapPercentage = 15;

        for (let row = 0; row < gridSize; row++) {
            for (let col = 0; col < gridSize; col++) {
                if (grid[row][col] !== 0) {
                    const tileValue = grid[row][col];
                    const tile = document.createElement('div');

                    tile.classList.add('tile');
                    tile.classList.add(`tile-${tileValue}`);
                    tile.textContent = tileValue;

                    tile.style.top = `calc(${row * cellSize}% + ${row * gapPercentage / 4}px)`;
                    tile.style.left = `calc(${col * cellSize}% + ${col * gapPercentage / 4}px)`;

                    gameBoard.appendChild(tile);

                    if (tileValue === 2048 && !gameWon) {
                        winGame();
                    }
                }
            }
        }
    }

    function move(direction) {
        if (gameOver || gameWon) return;

        let moved = false;
        const oldGrid = JSON.parse(JSON.stringify(grid));

        switch (direction) {
            case 'up':
                moved = moveUp();
                break;
            case 'down':
                moved = moveDown();
                break;
            case 'left':
                moved = moveLeft();
                break;
            case 'right':
                moved = moveRight();
                break;
        }

        if (moved) {
            addTile();
            updateScore();
        }
    }

    function moveUp() {
        let moved = false;

        for (let col = 0; col < gridSize; col++) {
            for (let row = 1; row < gridSize; row++) {
                if (grid[row][col] !== 0) {
                    let currentRow = row;

                    while (currentRow > 0) {
                        if (grid[currentRow - 1][col] === 0) {
                            grid[currentRow - 1][col] = grid[currentRow][col];
                            grid[currentRow][col] = 0;
                            currentRow--;
                            moved = true;
                        } else if (grid[currentRow - 1][col] === grid[currentRow][col]) {
                            grid[currentRow - 1][col] *= 2;
                            grid[currentRow][col] = 0;
                            score += grid[currentRow - 1][col];
                            moved = true;
                            break;
                        } else {
                            break;
                        }
                    }
                }
            }
        }

        return moved;
    }

    function moveDown() {
        let moved = false;

        for (let col = 0; col < gridSize; col++) {
            for (let row = gridSize - 2; row >= 0; row--) {
                if (grid[row][col] !== 0) {
                    let currentRow = row;

                    while (currentRow < gridSize - 1) {
                        if (grid[currentRow + 1][col] === 0) {
                            grid[currentRow + 1][col] = grid[currentRow][col];
                            grid[currentRow][col] = 0;
                            currentRow++;
                            moved = true;
                        } else if (grid[currentRow + 1][col] === grid[currentRow][col]) {
                            grid[currentRow + 1][col] *= 2;
                            grid[currentRow][col] = 0;
                            score += grid[currentRow + 1][col];
                            moved = true;
                            break;
                        } else {
                            break;
                        }
                    }
                }
            }
        }

        return moved;
    }

    function moveLeft() {
        let moved = false;

        for (let row = 0; row < gridSize; row++) {
            for (let col = 1; col < gridSize; col++) {
                if (grid[row][col] !== 0) {
                    let currentCol = col;

                    while (currentCol > 0) {
                        if (grid[row][currentCol - 1] === 0) {
                            grid[row][currentCol - 1] = grid[row][currentCol];
                            grid[row][currentCol] = 0;
                            currentCol--;
                            moved = true;
                        } else if (grid[row][currentCol - 1] === grid[row][currentCol]) {
                            grid[row][currentCol - 1] *= 2;
                            grid[row][currentCol] = 0;
                            score += grid[row][currentCol - 1];
                            moved = true;
                            break;
                        } else {
                            break;
                        }
                    }
                }
            }
        }

        return moved;
    }

    function moveRight() {
        let moved = false;

        for (let row = 0; row < gridSize; row++) {
            for (let col = gridSize - 2; col >= 0; col--) {
                if (grid[row][col] !== 0) {
                    let currentCol = col;

                    while (currentCol < gridSize - 1) {
                        if (grid[row][currentCol + 1] === 0) {
                            grid[row][currentCol + 1] = grid[row][currentCol];
                            grid[row][currentCol] = 0;
                            currentCol++;
                            moved = true;
                        } else if (grid[row][currentCol + 1] === grid[row][currentCol]) {
                            grid[row][currentCol + 1] *= 2;
                            grid[row][currentCol] = 0;
                            score += grid[row][currentCol + 1];
                            moved = true;
                            break;
                        } else {
                            break;
                        }
                    }
                }
            }
        }

        return moved;
    }

    function isGameOver() {
        for (let row = 0; row < gridSize; row++) {
            for (let col = 0; col < gridSize; col++) {
                if (grid[row][col] === 0) {
                    return false;
                }
            }
        }

        for (let row = 0; row < gridSize; row++) {
            for (let col = 0; col < gridSize; col++) {
                const value = grid[row][col];

                if (
                    (row < gridSize - 1 && grid[row + 1][col] === value) ||
                    (col < gridSize - 1 && grid[row][col + 1] === value)
                ) {
                    return false;
                }
            }
        }

        return true;
    }

    function endGame() {
        gameOver = true;
        gameOverMessage.classList.remove('hidden');
    }

    function winGame() {
        gameWon = true;
        gameWonMessage.classList.remove('hidden');
    }

    function updateScore() {
        scoreDisplay.textContent = score;

        if (score > bestScore) {
            bestScore = score;
            localStorage.setItem('bestScore', bestScore);
            updateBestScore();
        }
    }

    function updateBestScore() {
        bestScoreDisplay.textContent = bestScore;
    }

    function resetGame() {
        grid = Array(gridSize).fill().map(() => Array(gridSize).fill(0));
        score = 0;
        gameOver = false;
        gameWon = false;

        updateScore();
        renderTiles();

        gameOverMessage.classList.add('hidden');
        gameWonMessage.classList.add('hidden');

        addTile();
        addTile();
    }

    function toggleTheme() {
        isClassicTheme = !isClassicTheme;

        if (isClassicTheme) {
            document.body.classList.add('classic');
            themeToggle.textContent = 'Цвет: Классика';
        } else {
            document.body.classList.remove('classic');
            themeToggle.textContent = 'Цвет: Ч/Б';
        }
    }

function setupSwipeEvents() {
        let touchStartX, touchStartY, touchEndX, touchEndY;
        const gameBoard = document.getElementById('game-board');

        gameBoard.addEventListener('touchstart', e => {
            e.preventDefault();
            touchStartX = e.touches[0].clientX;
            touchStartY = e.touches[0].clientY;
        }, { passive: false });

        gameBoard.addEventListener('touchmove', e => {
            e.preventDefault();
        }, { passive: false });

        gameBoard.addEventListener('touchend', e => {
            e.preventDefault();
            touchEndX = e.changedTouches[0].clientX;
            touchEndY = e.changedTouches[0].clientY;

            handleSwipe();
        }, { passive: false });

        function handleSwipe() {
            const dx = touchEndX - touchStartX;
            const dy = touchEndY - touchStartY;
            const minSwipeDistance = 30;

            if (Math.abs(dx) > minSwipeDistance || Math.abs(dy) > minSwipeDistance) {
                if (Math.abs(dx) > Math.abs(dy)) {
                    if (dx > 0) {
                        move('right');
                    } else {
                        move('left');
                    }
                } else {
                    if (dy > 0) {
                        move('down');
                    } else {
                        move('up');
                    }
                }
            }
        }
    }

    function addButtonListeners() {
        restartButton.addEventListener('click', resetGame);

        themeToggle.addEventListener('click', toggleTheme);

        upButton.addEventListener('click', () => move('up'));
        downButton.addEventListener('click', () => move('down'));
        leftButton.addEventListener('click', () => move('left'));
        rightButton.addEventListener('click', () => move('right'));

        document.querySelector('.try-again').addEventListener('click', resetGame);
        document.querySelector('.continue').addEventListener('click', () => {
            gameWonMessage.classList.add('hidden');
            gameWon = false;
        });

        document.addEventListener('keydown', e => {
            if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)) {
                e.preventDefault();

                switch (e.key) {
                    case 'ArrowUp':
                        move('up');
                        break;
                    case 'ArrowDown':
                        move('down');
                        break;
                    case 'ArrowLeft':
                        move('left');
                        break;
                    case 'ArrowRight':
                        move('right');
                        break;
                }
            }
        });
    }

    initGame();
});