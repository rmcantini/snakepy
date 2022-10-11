"""importing libraries"""
import random
import time
import pygame


SNAKE_SPEED = 15

# Window size
WINDOW_X = 720
WINDOW_Y = 480

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Initialising pygame
pygame.init()

# Initialise game window
pygame.display.set_caption("Joguinho de Cobrinha")
game_window = pygame.display.set_mode((WINDOW_X, WINDOW_Y))

# FPS (frames per second) controller
fps = pygame.time.Clock()

# defining snake default position
snake_position = [100, 50]

# defining first 4 blocks of snake body
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]

# fruit position
fruit_position = [
    random.randrange(1, (WINDOW_X // 10)) * 10,
    random.randrange(1, (WINDOW_Y // 10)) * 10,
]

FRUIT_SPAWN = True

# setting default snake direction towards
# right
DIRECTION = "RIGHT"
CHANGE_TO = DIRECTION

# initial score
SCORE = 0

# displaying Score function
def show_score(choice, color, font, size):

    # creating font object score_font
    score_font = pygame.font.SysFont(font, size)

    # create the display surface object
    # score_surface
    score_surface = score_font.render("Score : " + str(SCORE), True, color)

    # create a rectangular object for the text
    # surface object
    score_rect = score_surface.get_rect()

    # displaying text
    game_window.blit(score_surface, score_rect)


# game over function
def game_over():

    # creating font object my_font
    my_font = pygame.font.SysFont("roboto", 50)

    # creating a text surface on which text
    # will be drawn
    game_over_surface = my_font.render("Your Score is : " + str(SCORE), True, red)

    # create a rectangular object for the text
    # surface object
    game_over_rect = game_over_surface.get_rect()

    # setting position of the text
    game_over_rect.midtop = (WINDOW_X / 2, WINDOW_Y / 4)

    # blit will draw the text on screen
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    # after 2 seconds we will quit the program
    time.sleep(2)

    # deactivating pygame library
    pygame.quit()

    # quit the program
    quit()


# Main Function
while True:

    # handling key events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                CHANGE_TO = "UP"
            if event.key == pygame.K_DOWN:
                CHANGE_TO = "DOWN"
            if event.key == pygame.K_LEFT:
                CHANGE_TO = "LEFT"
            if event.key == pygame.K_RIGHT:
                CHANGE_TO = "RIGHT"

    # If two keys pressed simultaneously
    # we don't want snake to move into two
    # directions simultaneously
    if CHANGE_TO == "UP" and DIRECTION != "DOWN":
        DIRECTION = "UP"
    if CHANGE_TO == "DOWN" and DIRECTION != "UP":
        DIRECTION = "DOWN"
    if CHANGE_TO == "LEFT" and DIRECTION != "RIGHT":
        DIRECTION = "LEFT"
    if CHANGE_TO == "RIGHT" and DIRECTION != "LEFT":
        DIRECTION = "RIGHT"

    # Moving the snake
    if DIRECTION == "UP":
        snake_position[1] -= 10
    if DIRECTION == "DOWN":
        snake_position[1] += 10
    if DIRECTION == "LEFT":
        snake_position[0] -= 10
    if DIRECTION == "RIGHT":
        snake_position[0] += 10

    # Snake body growing mechanism
    # if fruits and snakes collide then scores
    # will be incremented by 10
    snake_body.insert(0, list(snake_position))
    if (
        snake_position[0] == fruit_position[0]
        and snake_position[1] == fruit_position[1]
    ):
        SCORE += 10
        FRUIT_SPAWN = False
    else:
        snake_body.pop()

    if not FRUIT_SPAWN:
        fruit_position = [
            random.randrange(1, (WINDOW_X // 10)) * 10,
            random.randrange(1, (WINDOW_Y // 10)) * 10,
        ]

    FRUIT_SPAWN = True
    game_window.fill(black)

    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(
        game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10)
    )

    # Game Over conditions
    if snake_position[0] < 0 or snake_position[0] > WINDOW_X - 10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > WINDOW_Y - 10:
        game_over()

    # Touching the snake body
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    # displaying score countinuously
    show_score(1, white, "roboto", 20)

    # Refresh game screen
    pygame.display.update()

    # Frame Per Second /Refresh Rate
    fps.tick(SNAKE_SPEED)
