const canvas = document.getElementById('lifeCanvas');
const ctx = canvas.getContext('2d');
const cellSize = 10;
const cols = Math.floor(canvas.width / cellSize);
const rows = Math.floor(canvas.height / cellSize);

let grid = Array.from({length: rows}, () => Array(cols).fill(0));
let running = false;
let interval = null;

// Toroidal (wrap-around) komşu sayma fonksiyonu
const countNeighbors = (y, x) => {
    let n = 0;
    for (let dy = -1; dy <= 1; dy++) {
        for (let dx = -1; dx <= 1; dx++) {
            if (dx === 0 && dy === 0) continue;
            // wrap-around ile komşu bak
            const ny = (y + dy + rows) % rows;
            const nx = (x + dx + cols) % cols;
            n += grid[ny][nx];
        }
    }
    return n;
};

const draw = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let y = 0; y < rows; y++) {
        for (let x = 0; x < cols; x++) {
            ctx.strokeStyle = "#e0e0e0";
            ctx.strokeRect(x * cellSize, y * cellSize, cellSize, cellSize);
            if (grid[y][x]) {
                ctx.fillStyle = "#222";
                ctx.fillRect(x * cellSize, y * cellSize, cellSize, cellSize);
            }
        }
    }
};

const step = () => {
    const newGrid = Array.from({length: rows}, () => Array(cols).fill(0));
    for (let y = 0; y < rows; y++) {
        for (let x = 0; x < cols; x++) {
            const neighbors = countNeighbors(y, x);
            if (grid[y][x]) {
                newGrid[y][x] = (neighbors === 2 || neighbors === 3) ? 1 : 0;
            } else {
                newGrid[y][x] = (neighbors === 3) ? 1 : 0;
            }
        }
    }
    grid = newGrid;
    draw();
};

const start = () => {
    if (!running) {
        running = true;
        interval = setInterval(step, 100);
    }
};

const stop = () => {
    running = false;
    clearInterval(interval);
};

canvas.addEventListener('click', (e) => {
    const rect = canvas.getBoundingClientRect();
    const x = Math.floor((e.clientX - rect.left) / cellSize);
    const y = Math.floor((e.clientY - rect.top) / cellSize);
    grid[y][x] = grid[y][x] ? 0 : 1;
    draw();
});

document.getElementById('startBtn').addEventListener('click', start);
document.getElementById('stopBtn').addEventListener('click', stop);
document.getElementById('clearBtn').addEventListener('click', () => {
    grid = Array.from({length: rows}, () => Array(cols).fill(0));
    draw();
});

draw();
