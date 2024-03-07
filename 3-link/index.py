import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
BIRD_IMG = pygame.image.load('bird.png')
BACKGROUND_IMG = pygame.image.load('background.jpg')
PIPE_IMG = pygame.image.load('pipe.png')
PIPE_GAP = 200
BIRD_MOTION = 10
GRAVITY = 1

# Create the game screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Create a clock to manage the game's FPS
clock = pygame.time.Clock()

# Create a Bird object
bird = pygame.sprite.Sprite()
bird.rect = pygame.Rect(100, HEIGHT // 2, 50, 50)
bird.velocity = 0
bird.jumped = False

# Create a Group for the bird
bird_group = pygame.sprite.Group()
bird_group.add(bird)

# Create a list to store the pipes
pipes = []

# Create a function to spawn a new pipe
def spawn_pipe():
    pipe_top = pygame.sprite.Sprite()
    pipe_top.rect = pygame.Rect(WIDTH, 0, 50, PIPE_IMG.get_height() + PIPE_GAP)
    pipe_bottom = pygame.sprite.Sprite()
    pipe_bottom.rect = pygame.Rect(WIDTH, PIPE_IMG.get_height() + PIPE_GAP, 50, HEIGHT - (PIPE_IMG.get_height() + PIPE_GAP))
    pipe_top.image = PIPE_IMG
    pipe_bottom.image = PIPE_IMG
    pipes.append((pipe_top, pipe_bottom))

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update the bird's position
    bird.velocity += GRAVITY
    bird.rect.y += bird.velocity

    if bird.rect.y + bird.rect.height > HEIGHT:
        bird.rect.y = HEIGHT - bird.rect.height
        bird.velocity = 0

    # Check for a jump
    if not bird.jumped and pygame.key.get_pressed()[pygame.K_SPACE]:
        bird.velocity = -BIRD_MOTION
        bird.jumped = True

    # Update the bird's jumping status
    if bird.jumped and bird.velocity < 0:
        bird.jumped = False

    # Move the pipes
    for i, (pipe_top, pipe_bottom) in enumerate(pipes):
        pipe_top.rect.x -= 5
        pipe_bottom.rect.x -= 5
        if pipe_top.rect.x < -50:
            pipes.pop(i)

    # Spawn new pipes
    if len(pipes) < 5:
        spawn_pipe()

    # Check for collisions
    for pipe in pipes:
        if bird.rect.colliderect(pipe[0]) or bird.rect.colliderect(pipe[1]):
            pygame.quit()
            sys.exit()

    # Draw everything
    screen.blit(BACKGROUND_IMG, (0, 0))
    for pipe in pipes:
        screen.blit(pipe[0].image, pipe[0].rect)
        screen.blit(pipe[1].image, pipe[1].rect)

    pygame.display.flip()
    clock.tick(30)
