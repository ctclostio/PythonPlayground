const canvas = document.getElementById('game-board');
const ctx = canvas.getContext('2d');

const GRID_SIZE = 20;
const TILE_COUNT = 20;
const INITIAL_SPEED = 100;

let snake = [{x: 10, y: 10}];
let food = {x: 15, y: 15};
let direction = {x: 0, y: 0};
let lastRenderTime = 0;
let gameOver = false;
let speed = INITIAL_SPEED;

function main(currentTime) {
    if (gameOver) {
        if (confirm('Game Over! Play again?')) {
            resetGame();
        }
        return;
    }

    window.requestAnimationFrame(main);
    const secondsSinceLastRender = (currentTime - lastRenderTime) / 1000;
    if (secondsSinceLastRender < 1 / speed) return;

    lastRenderTime = currentTime;

    update();
    draw();
}

function update() {
    const head = {x: snake[0].x + direction.x, y: snake[0].y + direction.y};

    // Check collision with walls
    if (head.x < 0 || head.x >= TILE_COUNT || head.y < 0 || head.y >= TILE_COUNT) {
        gameOver = true;
        return;
    }

    // Check collision with self
    for (let i = 1; i < snake.length; i++) {
        if (head.x === snake[i].x && head.y === snake[i].y) {
            gameOver = true;
            return;
        }
    }

    snake.unshift(head);

    // Check if snake eats food
    if (head.x === food.x && head.y === food.y) {
        speed += 5;
        placeFood();
    } else {
        snake.pop();
    }
}

function draw() {
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = '#0f0';
    snake.forEach(segment => {
        ctx.fillRect(segment.x * GRID_SIZE, segment.y * GRID_SIZE, GRID_SIZE, GRID_SIZE);
    });

    ctx.fillStyle = '#f00';
    ctx.fillRect(food.x * GRID_SIZE, food.y * GRID_SIZE, GRID_SIZE, GRID_SIZE);
}

function placeFood() {
    food = {
        x: Math.floor(Math.random() * TILE_COUNT),
        y: Math.floor(Math.random() * TILE_COUNT)
    };

    // Make sure food doesn't spawn on snake
    for (let segment of snake) {
        if (food.x === segment.x && food.y === segment.y) {
            return placeFood();
        }
    }
}

function resetGame() {
    snake = [{x: 10, y: 10}];
    direction = {x: 0, y: 0};
    speed = INITIAL_SPEED;
    gameOver = false;
    placeFood();
    window.requestAnimationFrame(main);
}

window.addEventListener('keydown', e => {
    switch (e.key) {
        case 'ArrowUp':
            if (direction.y === 0) direction = {x: 0, y: -1};
            break;
        case 'ArrowDown':
            if (direction.y === 0) direction = {x: 0, y: 1};
            break;
        case 'ArrowLeft':
            if (direction.x === 0) direction = {x: -1, y: 0};
            break;
        case 'ArrowRight':
            if (direction.x === 0) direction = {x: 1, y: 0};
            break;
    }
});

placeFood();
window.requestAnimationFrame(main);