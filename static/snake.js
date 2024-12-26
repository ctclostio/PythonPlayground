const canvas = document.getElementById('game-board');
const ctx = canvas.getContext('2d');

const GRID_SIZE = 10; // Smaller blocks for larger grid
const TILE_COUNT = 75; // 75x75 grid
const INITIAL_SPEED = 8;

// Player snake
let snake = [{x: 10, y: 10}];
let direction = {x: 0, y: 0};

// Red enemy snake
let redSnake = [{x: 60, y: 60}];
let redDirection = {x: 1, y: 0};
let redSpeed = INITIAL_SPEED * 0.8; // Starts slower than player
let redInsults = [
    "You move like a snail!",
    "Is that all you've got?",
    "My grandma plays better!",
    "You're making this too easy!",
    "Catch me if you can!"
];
let currentInsult = "";
let insultCooldown = 0;

// Food
let food = {x: 15, y: 15};

// Game state
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
    // Update player snake
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
        speed += 0.5;
        placeFood();
    } else {
        snake.pop();
    }

    // Update red snake
    updateRedSnake();
}

function updateRedSnake() {
    // Move red snake
    const redHead = {x: redSnake[0].x + redDirection.x, y: redSnake[0].y + redDirection.y};
    
    // Keep red snake within bounds
    if (redHead.x < 0 || redHead.x >= TILE_COUNT || redHead.y < 0 || redHead.y >= TILE_COUNT) {
        // Change direction when hitting wall
        redDirection = getRandomDirection();
        return;
    }

    redSnake.unshift(redHead);
    redSnake.pop();

    // Update insult
    if (insultCooldown <= 0) {
        currentInsult = redInsults[Math.floor(Math.random() * redInsults.length)];
        insultCooldown = 100; // Cooldown in frames
    } else {
        insultCooldown--;
    }

    // Increase red snake speed based on player snake size
    redSpeed = INITIAL_SPEED * 0.8 + (snake.length * 0.1);
}

function getRandomDirection() {
    const directions = [
        {x: 1, y: 0},
        {x: -1, y: 0},
        {x: 0, y: 1},
        {x: 0, y: -1}
    ];
    return directions[Math.floor(Math.random() * directions.length)];
}

function draw() {
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw player snake
    drawSnake(snake, '#4CAF50', '#388E3C');

    // Draw red snake
    drawSnake(redSnake, '#FF5252', '#D32F2F');

    // Draw food
    ctx.fillStyle = '#FFC107';
    ctx.fillRect(food.x * GRID_SIZE, food.y * GRID_SIZE, GRID_SIZE, GRID_SIZE);

    // Draw insult
    if (currentInsult) {
        ctx.fillStyle = '#FFF';
        ctx.font = '12px Arial';
        ctx.fillText(currentInsult, redSnake[0].x * GRID_SIZE, redSnake[0].y * GRID_SIZE - 5);
    }
}

function drawSnake(snakeBody, startColor, endColor) {
    snakeBody.forEach((segment, index) => {
        const x = segment.x * GRID_SIZE;
        const y = segment.y * GRID_SIZE;
        const radius = GRID_SIZE / 4;
        
        // Create gradient
        const gradient = ctx.createRadialGradient(
            x + GRID_SIZE/2, y + GRID_SIZE/2, 0,
            x + GRID_SIZE/2, y + GRID_SIZE/2, GRID_SIZE
        );
        gradient.addColorStop(0, startColor);
        gradient.addColorStop(1, endColor);
        
        ctx.fillStyle = gradient;
        
        // Draw rounded rectangle
        ctx.beginPath();
        ctx.moveTo(x + radius, y);
        ctx.lineTo(x + GRID_SIZE - radius, y);
        ctx.arcTo(x + GRID_SIZE, y, x + GRID_SIZE, y + radius, radius);
        ctx.lineTo(x + GRID_SIZE, y + GRID_SIZE - radius);
        ctx.arcTo(x + GRID_SIZE, y + GRID_SIZE, x + GRID_SIZE - radius, y + GRID_SIZE, radius);
        ctx.lineTo(x + radius, y + GRID_SIZE);
        ctx.arcTo(x, y + GRID_SIZE, x, y + GRID_SIZE - radius, radius);
        ctx.lineTo(x, y + radius);
        ctx.arcTo(x, y, x + radius, y, radius);
        ctx.closePath();
        ctx.fill();
    });
}

function placeFood() {
    food = {
        x: Math.floor(Math.random() * TILE_COUNT),
        y: Math.floor(Math.random() * TILE_COUNT)
    };

    // Make sure food doesn't spawn on snakes
    for (let segment of snake) {
        if (food.x === segment.x && food.y === segment.y) {
            return placeFood();
        }
    }
    for (let segment of redSnake) {
        if (food.x === segment.x && food.y === segment.y) {
            return placeFood();
        }
    }
}

function resetGame() {
    snake = [{x: 10, y: 10}];
    redSnake = [{x: 60, y: 60}];
    direction = {x: 0, y: 0};
    redDirection = {x: 1, y: 0};
    speed = INITIAL_SPEED;
    redSpeed = INITIAL_SPEED * 0.8;
    gameOver = false;
    currentInsult = "";
    insultCooldown = 0;
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
        case ' ': // Space bar for insults
            const playerInsults = [
                "You're too slow!",
                "Watch and learn!",
                "Is that your best?",
                "Try harder!",
                "I'm just warming up!"
            ];
            currentInsult = playerInsults[Math.floor(Math.random() * playerInsults.length)];
            insultCooldown = 100;
            break;
    }
});

placeFood();
window.requestAnimationFrame(main);