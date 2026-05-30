import pygame
import random
import sys

pygame.init()

# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# ---------------- COLORS ----------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# ---------------- SETTINGS ----------------
block = 10

# 🐢 SLOW SPEED (lower = slower snake)
speed = 5

font = pygame.font.SysFont("arial", 25)

# ---------------- TEXT ----------------
def draw_text(text, color, x, y):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# ---------------- HOME SCREEN ----------------
def home_screen():
    while True:
        screen.fill(BLACK)
        draw_text("SNAKE GAME", GREEN, 220, 100)
        draw_text("Press ENTER to Play", WHITE, 180, 180)
        draw_text("Press Q to Quit", WHITE, 200, 220)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# ---------------- GAME LOOP ----------------
def gameLoop():
    game_over = False
    game_close = False
    paused = False

    x = WIDTH // 2
    y = HEIGHT // 2

    dx = 0
    dy = 0

    snake = []
    length = 1

    foodx = random.randrange(0, WIDTH, block)
    foody = random.randrange(0, HEIGHT, block)

    while not game_over:

        while game_close:
            screen.fill(BLACK)
            draw_text("GAME OVER", RED, 230, 120)
            draw_text("Press C to Restart", WHITE, 200, 180)
            draw_text("Press Q for Home", WHITE, 200, 220)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        gameLoop()
                    if event.key == pygame.K_q:
                        return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -block
                    dy = 0
                elif event.key == pygame.K_RIGHT:
                    dx = block
                    dy = 0
                elif event.key == pygame.K_UP:
                    dx = 0
                    dy = -block
                elif event.key == pygame.K_DOWN:
                    dx = 0
                    dy = block
                elif event.key == pygame.K_p:
                    paused = True
                elif event.key == pygame.K_q:
                    return

        # ---------------- PAUSE ----------------
        while paused:
            draw_text("PAUSED - Press R to Resume", BLUE, 150, 180)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        paused = False
                    if event.key == pygame.K_q:
                        return

            clock.tick(5)

        x += dx
        y += dy

        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        screen.fill(BLACK)

        pygame.draw.rect(screen, GREEN, [foodx, foody, block, block])

        snake_head = [x, y]
        snake.append(snake_head)

        if len(snake) > length:
            del snake[0]

        for segment in snake[:-1]:
            if segment == snake_head:
                game_close = True

        for segment in snake:
            pygame.draw.rect(screen, WHITE, [segment[0], segment[1], block, block])

        pygame.display.update()

        if x == foodx and y == foody:
            foodx = random.randrange(0, WIDTH, block)
            foody = random.randrange(0, HEIGHT, block)
            length += 1

        clock.tick(speed)

# ---------------- MAIN ----------------
while True:
    home_screen()
    gameLoop()