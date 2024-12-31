import sys
import pygame
from src.pygame.ping_pong_game.Ball import Ball
from src.pygame.ping_pong_game.Paddle import Paddle

# initialize pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# PADDLE_WIDTH = 10
# PADDLE_HEIGHT = 100
FPS = 60

# Set up some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

# Set up the font
font = pygame.font.Font(None, 36)
ball = Ball(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 5, 5, 20)

# Set up the paddles
paddle1 = Paddle(0, SCREEN_HEIGHT / 2 - 50, 10, 100, 0)
paddle2 = Paddle(SCREEN_WIDTH - 10, SCREEN_HEIGHT / 2 - 50, 10, 100, 0)

# Game loop
while True:
    # read all input keys
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    # Move the paddles
    if keys[pygame.K_w]:
        paddle1.move_up()
    if keys[pygame.K_s]:
        paddle1.move_down()
    if keys[pygame.K_UP]:
        paddle2.move_up()
    if keys[pygame.K_DOWN]:
        paddle2.move_down()

    # Move the ball
    ball.move()

    # Collision with walls (up and down)
    if ball.y < 0 or ball.y > SCREEN_HEIGHT - ball.radius:
        ball.bounce_y()

    # Collision of the ball with paddles
    if ball.x <= paddle1.width + ball.radius and paddle1.y < ball.y < paddle1.y + paddle1.height:
        ball.bounce_x()
    elif ball.x >= SCREEN_WIDTH - paddle2.width - ball.radius and paddle2.y < ball.y < paddle2.y + paddle2.height:
        ball.bounce_x()

    # scoring the ball
    if ball.x <= 0:
        paddle2.score += 1
        ball.reset(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    elif ball.x >= SCREEN_WIDTH:
        paddle1.score += 1
        ball.reset(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (0, paddle1.y, paddle1.width, paddle1.height))  # paddle on left
    pygame.draw.rect(screen, WHITE,
                     (SCREEN_WIDTH - paddle2.width, paddle2.y, paddle2.width, paddle2.height))  # paddle on right
    pygame.draw.circle(screen, WHITE, (ball.x, ball.y), ball.radius)
    text = font.render(f"{paddle1.score} - {paddle2.score}", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, 10))

    # Update the display
    pygame.display.flip()
    pygame.time.Clock().tick(FPS)
