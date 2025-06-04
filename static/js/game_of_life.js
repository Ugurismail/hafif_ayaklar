const canvas = document.getElementById('lifeCanvas');
const ctx = canvas.getContext('2d');
const cellSize = 10;
const cols = canvas.width / cellSize;
const rows = canvas.height / cellSize;
let grid = Array.from({length: rows}, () => Array(cols).fill(0));
let running = false;
let interval;

canvas.addEventListener('click', (e) => {
    const rect = canvas.getBoundingClientRect();
    const x = Math.floor((e.clientX - rect.left) / cellSize);
    const y = Math.floor((e.clientY - rect.top) / cellSize);
    grid[y][x] = grid[y][x] ? 0 : 1;
    draw();
});

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let y = 0; y < rows; y++) {
        for (let x = 0; x < cols; x++) {
            if (grid[y][x]) {
                ctx.fillRect(x * cellSize, y * cellSize, cellSize, cellSize);
            }
            ctx.strokeRect(x * cellSize, y * cellSize, cellSize, cellSize);
        }
    }
}

function step() {
    const newGrid = grid.map(row => row.slice());
    for (let y = 0; y < rows; y++) {
        for (let x = 0; x < cols; x++) {
            let neighbors = 0;
            for (let j = -1; j <= 1; j++) {
                for (let i = -1; i <= 1; i++) {
                    if (i === 0 && j === 0) continue;
                    const nx = x + i;
                    const ny = y + j;
                    if (nx >= 0 && nx < cols && ny >= 0 && ny < rows) {
                        neighbors += grid[ny][nx];
                    }
                }
            }
            if (grid[y][x]) {
                if (neighbors < 2 || neighbors > 3) newGrid[y][x] = 0;
            } else {
                if (neighbors === 3) newGrid[y][x] = 1;
            }
        }
    }
    grid = newGrid;
    draw();
}

function start() {
    if (!running) {
        running = true;
        interval = setInterval(step, 100);
    }
}

function stop() {
    running = false;
    clearInterval(interval);
}

document.getElementById('startBtn').addEventListener('click', start);
document.getElementById('stopBtn').addEventListener('click', stop);
document.getElementById('clearBtn').addEventListener('click', () => {
    grid = grid.map(row => row.fill(0));
    draw();
});

draw();
