import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game constants
WIDTH = 400
HEIGHT = 400
BLOCK_SIZE = 20
SPEED = 15

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Initialize display
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.body = [[100, 50], [90, 50], [80, 50]]
        self.direction = 'RIGHT'
        self.change_to = self.direction

    def change_direction(self, new_dir):
        if new_dir == 'RIGHT' and not self.direction == 'LEFT':
            self.direction = 'RIGHT'
        if new_dir == 'LEFT' and not self.direction == 'RIGHT':
            self.direction = 'LEFT'
        if new_dir == 'UP' and not self.direction == 'DOWN':
            self.direction = 'UP'
        if new_dir == 'DOWN' and not self.direction == 'UP':
            self.direction = 'DOWN'

    def move(self, food_pos):
        if self.direction == 'RIGHT':
            self.body.insert(0, [self.body[0][0] + BLOCK_SIZE, self.body[0][1]])
        if self.direction == 'LEFT':
            self.body.insert(0, [self.body[0][0] - BLOCK_SIZE, self.body[0][1]])
        if self.direction == 'UP':
            self.body.insert(0, [self.body[0][0], self.body[0][1] - BLOCK_SIZE])
        if self.direction == 'DOWN':
            self.body.insert(0, [self.body[0][0], self.body[0][1] + BLOCK_SIZE])

        if self.body[0] == food_pos:
            return True
        else:
            self.body.pop()
            return False

    def check_collision(self):
        # Check collision with walls
        if (self.body[0][0] >= WIDTH or self.body[0][0] < 0 or
            self.body[0][1] >= HEIGHT or self.body[0][1] < 0):
            return True
        # Check collision with self
        for block in self.body[1:]:
            if self.body[0] == block:
                return True
        return False

    def draw(self):
        for block in self.body:
            pygame.draw.rect(window, GREEN, pygame.Rect(
                block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))

class Food:
    def __init__(self):
        self.position = [random.randrange(1, (WIDTH//BLOCK_SIZE)) * BLOCK_SIZE,
                        random.randrange(1, (HEIGHT//BLOCK_SIZE)) * BLOCK_SIZE]
        self.is_food_on_screen = True

    def draw(self):
        pygame.draw.rect(window, RED, pygame.Rect(
            self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

def game_loop():
    snake = Snake()
    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction('UP')
                if event.key == pygame.K_DOWN:
                    snake.change_direction('DOWN')
                if event.key == pygame.K_LEFT:
                    snake.change_direction('LEFT')
                if event.key == pygame.K_RIGHT:
                    snake.change_direction('RIGHT')

        window.fill(BLACK)
        
        if snake.move(food.position):
            food.position = [random.randrange(1, (WIDTH//BLOCK_SIZE)) * BLOCK_SIZE,
                            random.randrange(1, (HEIGHT//BLOCK_SIZE)) * BLOCK_SIZE]

        if snake.check_collision():
            break

        snake.draw()
        food.draw()

        pygame.display.update()
        clock.tick(SPEED)

    pygame.quit()

if __name__ == '__main__':
    game_loop()