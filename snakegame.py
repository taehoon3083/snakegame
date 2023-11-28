import pygame
import random
from datetime import datetime, timedelta

pygame.init()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
size = [400, 400]
screen = pygame.display.set_mode(size)

done = False
clock = pygame.time.Clock()
last_moved_time = datetime.now()

KEY_DIRECTION = {
    pygame.K_UP: 'N',
    pygame.K_DOWN: 'S',
    pygame.K_LEFT: 'W',
    pygame.K_RIGHT: 'E',
}


def draw_block(screen, color, position):
    block = pygame.Rect((position[1] * 20, position[0] * 20), (20, 20))
    pygame.draw.rect(screen, color, block)


class Snake:
    def __init__(self):
        self.positions = [(0, 2), (0, 1), (0, 0)]
        self.direction = ''
        self.score = 0

    def draw(self):
        for position in self.positions:
            draw_block(screen, GREEN, position)

    def move(self):
        head_position = self.positions[0]
        y, x = head_position
        if self.direction == 'N':
            self.positions = [(y - 1, x)] + self.positions[:-1]
        elif self.direction == 'S':
            self.positions = [(y + 1, x)] + self.positions[:-1]
        elif self.direction == 'W':
            self.positions = [(y, x - 1)] + self.positions[:-1]
        elif self.direction == 'E':
            self.positions = [(y, x + 1)] + self.positions[:-1]

    def grow(self):
        tail_position = self.positions[-1]
        y, x = tail_position
        if self.direction == 'N':
            self.positions.append((y - 1, x))
        elif self.direction == 'S':
            self.positions.append((y + 1, x))
        elif self.direction == 'W':
            self.positions.append((y, x - 1))
        elif self.direction == 'E':
            self.positions.append((y, x + 1))
        self.score += 1

    def check_collision(self):
        head_position = self.positions[0]
        y, x = head_position
        if (
            x < 0 or x >= 20 or
            y < 0 or y >= 20 or
            head_position in self.positions[1:]
        ):
            return True
        return False


class Apple:
    def __init__(self, position=(5, 5)):
        self.position = position

    def draw(self):
        draw_block(screen, RED, self.position)
        font = pygame.font.Font(None, 24)
        text = font.render(f"Score: {snake.score}", True, BLACK)  # 색상을 검은색으로 변경
        screen.blit(text, (10, 10))


def runGame():
    global done, last_moved_time, snake
    snake = Snake()
    apple = Apple()

    while not done:
        clock.tick(10)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key in KEY_DIRECTION:
                    snake.direction = KEY_DIRECTION[event.key]

        if timedelta(seconds=0.1) <= datetime.now() - last_moved_time:
            snake.move()
            last_moved_time = datetime.now()

        if snake.positions[0] == apple.position:
            snake.grow()
            apple.position = (random.randint(0, 19), random.randint(0, 19))

        if snake.check_collision():
            done = True

        snake.draw()
        apple.draw()
        pygame.display.update()


runGame()
pygame.quit()
