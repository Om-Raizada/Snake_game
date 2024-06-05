import pygame
import random

WIDTH = 800
HEIGHT = 600
SPEED = 5
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)] * BODY_PARTS
        self.direction = RIGHT

    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0] * SPACE_SIZE, head_y + self.direction[1] * SPACE_SIZE)
        self.body = [new_head] + self.body[:-1]

    def grow(self):
        self.body.append(self.body[-1])

    def check_collision(self):
        head = self.body[0]
        return (
            head in self.body[1:] or
            head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT
        )

    def change_direction(self, direction):
        if direction == UP and self.direction != DOWN:
            self.direction = UP
        elif direction == DOWN and self.direction != UP:
            self.direction = DOWN
        elif direction == LEFT and self.direction != RIGHT:
            self.direction = LEFT
        elif direction == RIGHT and self.direction != LEFT:
            self.direction = RIGHT


class Food:
    def __init__(self):
        self.position = (random.randint(0, (WIDTH // SPACE_SIZE) -1) * SPACE_SIZE, random.randint(0, (HEIGHT // SPACE_SIZE) -1) * SPACE_SIZE)

    def respawn(self):
        self.position = (random.randint(0, (WIDTH // SPACE_SIZE) -1) * SPACE_SIZE, random.randint(0, (HEIGHT // SPACE_SIZE) -1) * SPACE_SIZE)


def text_generator(surface, content, x, y, color, font):
    text = font.render(content, True, color)
    textRect = text.get_rect(center=(x, y))
    surface.blit(text, textRect)


def main():
    running = True
    state = 0

    pygame.init()


    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    big_font = pygame.font.Font(None, 128)
    small_font = pygame.font.Font(None, 64)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN and state == 0:
                    state = 1
                elif event.key == pygame.K_RETURN and state == 2:
                    state = 0
                elif event.key == pygame.K_UP:
                    snake.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(RIGHT)

        WIN.fill(BACKGROUND_COLOR)

        if state == 0:
            score = 0
            speed = 0
            text_generator(WIN, "Snake", WIDTH // 2, 150, (0, 236, 0), big_font)
            text_generator(WIN, "Press Enter to Play", (WIDTH // 2), 450, (0, 236, 0), small_font)

        elif state == 1:
            for segment in snake.body:
                pygame.draw.rect(WIN, SNAKE_COLOR, (segment[0], segment[1], SPACE_SIZE, SPACE_SIZE))
            pygame.draw.rect(WIN, FOOD_COLOR, (food.position[0], food.position[1], SPACE_SIZE, SPACE_SIZE))
            snake.move()

            if snake.body[0] == food.position:
                snake.grow()
                food.respawn()
                score += 1
                speed += 0.25

            if snake.check_collision():
                snake.__init__()
                food.__init__()
                state = 2

        if state == 2:
            text_generator(WIN, "Game Over", WIDTH // 2, 200, (0, 236, 0), big_font)
            text_generator(WIN, f"Score: {score}", WIDTH // 2, HEIGHT // 1.75, (0, 236, 0), small_font)

        pygame.display.update()
        clock.tick(SPEED + speed)


if __name__ == "__main__":
    main()




