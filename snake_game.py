import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game constants
WIDTH = 750
HEIGHT = 750
BLOCK_SIZE = 10
SPEED = 10

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
    def __init__(self, color, start_pos):
        self.body = [start_pos]
        self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        self.change_to = self.direction
        self.color = color
        self.insult = ""
        self.insult_cooldown = 0

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
        for i, block in enumerate(self.body):
            x, y = block[0], block[1]
            # Create gradient surface
            gradient = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
            start_color = (76, 175, 80)  # Light green
            end_color = (56, 142, 60)    # Dark green
            for j in range(BLOCK_SIZE):
                ratio = j / BLOCK_SIZE
                color = (
                    int(start_color[0] + (end_color[0] - start_color[0]) * ratio),
                    int(start_color[1] + (end_color[1] - start_color[1]) * ratio),
                    int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
                )
                pygame.draw.line(gradient, color, (0, j), (BLOCK_SIZE, j))
            
            # Draw rounded rectangle
            radius = BLOCK_SIZE // 4
            mask = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(mask, (255, 255, 255), (radius, 0, BLOCK_SIZE - 2*radius, BLOCK_SIZE))
            pygame.draw.rect(mask, (255, 255, 255), (0, radius, BLOCK_SIZE, BLOCK_SIZE - 2*radius))
            pygame.draw.circle(mask, (255, 255, 255), (radius, radius), radius)
            pygame.draw.circle(mask, (255, 255, 255), (BLOCK_SIZE - radius, radius), radius)
            pygame.draw.circle(mask, (255, 255, 255), (radius, BLOCK_SIZE - radius), radius)
            pygame.draw.circle(mask, (255, 255, 255), (BLOCK_SIZE - radius, BLOCK_SIZE - radius), radius)
            
            gradient.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            window.blit(gradient, (x, y))

class Food:
    def __init__(self):
        self.position = [random.randrange(1, (WIDTH//BLOCK_SIZE)) * BLOCK_SIZE,
                        random.randrange(1, (HEIGHT//BLOCK_SIZE)) * BLOCK_SIZE]
        self.is_food_on_screen = True

    def draw(self):
        pygame.draw.rect(window, (255, 193, 7), pygame.Rect(
            self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

class InsultSystem:
    def __init__(self):
        self.red_insults = [
            "You move like a snail!",
            "Is that all you've got?",
            "My grandma plays better!",
            "You're making this too easy!",
            "Catch me if you can!"
        ]
        self.player_insults = [
            "You're too slow!",
            "Watch and learn!",
            "Is that your best?",
            "Try harder!",
            "I'm just warming up!"
        ]
        self.current_insult = ""
        self.insult_cooldown = 0

    def get_red_insult(self):
        if self.insult_cooldown <= 0:
            self.current_insult = random.choice(self.red_insults)
            self.insult_cooldown = 100
        else:
            self.insult_cooldown -= 1
        return self.current_insult

    def get_player_insult(self):
        self.current_insult = random.choice(self.player_insults)
        self.insult_cooldown = 100
        return self.current_insult

def game_loop():
    player_snake = Snake((76, 175, 80), [100, 50])
    red_snake = Snake((255, 82, 82), [600, 600])
    food = Food()
    insult_system = InsultSystem()
    font = pygame.font.SysFont('Arial', 12)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player_snake.change_direction('UP')
                if event.key == pygame.K_DOWN:
                    player_snake.change_direction('DOWN')
                if event.key == pygame.K_LEFT:
                    player_snake.change_direction('LEFT')
                if event.key == pygame.K_RIGHT:
                    player_snake.change_direction('RIGHT')
                if event.key == pygame.K_SPACE:  # Space bar for insults
                    player_snake.insult = insult_system.get_player_insult()
                    player_snake.insult_cooldown = 100

        window.fill(BLACK)
        
        # Update player snake
        if player_snake.move(food.position):
            food.position = [random.randrange(1, (WIDTH//BLOCK_SIZE)) * BLOCK_SIZE,
                           random.randrange(1, (HEIGHT//BLOCK_SIZE)) * BLOCK_SIZE]
            SPEED += 0.5

        # Update red snake
        update_red_snake(red_snake, player_snake)

        # Check collisions
        if (player_snake.check_collision() or
            check_snake_collision(player_snake, red_snake)):
            break

        # Draw game elements
        player_snake.draw()
        red_snake.draw()
        food.draw()

        # Draw insults
        if red_snake.insult:
            text = font.render(red_snake.insult, True, WHITE)
            window.blit(text, (red_snake.body[0][0], red_snake.body[0][1] - 15))
        if player_snake.insult:
            text = font.render(player_snake.insult, True, WHITE)
            window.blit(text, (player_snake.body[0][0], player_snake.body[0][1] - 15))

        pygame.display.update()
        clock.tick(SPEED)

    pygame.quit()

def update_red_snake(red_snake, player_snake):
    # Simple AI for red snake
    if random.random() < 0.1:  # 10% chance to change direction
        red_snake.change_direction(random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT']))
    
    # Move red snake
    red_snake.move([0, 0])  # Pass dummy food position
    
    # Update insult
    if red_snake.insult_cooldown <= 0:
        red_snake.insult = f"Red Snake: {random.choice([
            'You move like a snail!',
            'Is that all you\'ve got?',
            'My grandma plays better!',
            'You\'re making this too easy!',
            'Catch me if you can!'
        ])}"
        red_snake.insult_cooldown = 100
    else:
        red_snake.insult_cooldown -= 1

    # Keep red snake within bounds
    if (red_snake.body[0][0] >= WIDTH or red_snake.body[0][0] < 0 or
        red_snake.body[0][1] >= HEIGHT or red_snake.body[0][1] < 0):
        red_snake.change_direction(random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT']))

def check_snake_collision(snake1, snake2):
    # Check if snake1 collides with snake2
    for block in snake2.body:
        if snake1.body[0] == block:
            return True
    return False

if __name__ == '__main__':
    game_loop()