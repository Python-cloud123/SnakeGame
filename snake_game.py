import sys
import pygame
import random

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)

eat_sound = pygame.mixer.Sound("eat.wav")
gameover_sound = pygame.mixer.Sound("gameover.wav")

# Colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Screen size
width = 600
height = 400

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

snake_block = 10
speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def show_score(score, high_score):

    value = score_font.render(
        "Score: " + str(score) + "  High Score: " + str(high_score),
        True,
        yellow
    )

    screen.blit(value, [0, 0])

def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(
            screen,
            green,
            [x[0], x[1], snake_block, snake_block],
             border_radius=3
        )

    if len(snake_list) > 0:

        head_x = int(snake_list[-1][0])
        head_y = int(snake_list[-1][1])

        pygame.draw.circle(screen, white, (head_x + 7, head_y + 3), 2)
        pygame.draw.circle(screen, white, (head_x + 7, head_y + 7), 2)    

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [width / 6, height / 3])
def start_screen():

    waiting = True

    while waiting:

        screen.fill(blue)

        title = score_font.render("SNAKE GAME", True, yellow)
        text = font_style.render("Press SPACE to Start", True, white)

        screen.blit(title, [170, 150])
        screen.blit(text, [150, 220])

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.sys.exit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    waiting = False

def gameLoop():

    game_over = False
    game_close = False

    speed = 15

    with open("highscore.txt", "r") as file:
        high_score = int(file.read())

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close:
            screen.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            show_score(Length_of_snake - 1, high_score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        pygame.quit()
                        sys.exit()
                        game_close = False

                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0

                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0

                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0

                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

                elif event.key == pygame.K_p:

                    paused = True

                    while paused:

                        screen.fill(black)

                        message("Paused - Press P Again", white)

                        pygame.display.update()

                        for event in pygame.event.get():

                            if event.type == pygame.QUIT:
                                pygame.sys.exit()
                                sys.exit()

                            if event.type == pygame.KEYDOWN:

                                if event.key == pygame.K_p:
                                    paused = False    

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:

            gameover_sound.play()

            game_close = True

        x1 += x1_change
        y1 += y1_change

        screen.fill(black)

        for x in range(0, width, 20):
            pygame.draw.line(screen, blue, (x, 0), (x, height))

        for y in range(0, height, 20):
            pygame.draw.line(screen, blue, (0, y), (width, y))

        pygame.draw.circle(
            screen,
            red,
            (int(foodx + snake_block / 2), int(foody + snake_block / 2)),
            snake_block // 2
        )

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)

        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:

                gameover_sound.play()

                game_close = True

        draw_snake(snake_block, snake_List)
        show_score(Length_of_snake - 1, high_score)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

            Length_of_snake += 1
            eat_sound.play()

            speed += 1

            if Length_of_snake - 1 > high_score:

                high_score = Length_of_snake - 1

                with open("highscore.txt", "w") as file:
                    file.write(str(high_score))

        clock.tick(speed)

    pygame.sys.exit()
    sys.exit()

start_screen()
gameLoop()