import pygame
import random
import math

# initialize pygame
pygame.init()

# screen create tuple (pixels)
screen = pygame.display.set_mode((800, 600))

# BG
bg = pygame.image.load("bg.jpg")

# Personalize display
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Player
playerIMG = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

# Alien

alienIMG = pygame.image.load("alien.png")
alienX = random.randint(0, 734)
alienY = random.randint(30, 150)
alienX_change = 0.1
alienY_change = 40

# Rocket
rocketIMG = pygame.image.load("rocket.png")
rocketX = 0
rocketY = 480
rocketY_change = 0.3
rocket_state = "ready"

score = 0


def player(x, y):
    screen.blit(playerIMG, (x, y))


def alien(x, y):
    screen.blit(alienIMG, (x, y))


def fire_rocket(x, y):
    global rocket_state
    rocket_state = "fire"
    screen.blit(rocketIMG, (x + 16, y + 10))


def isCollision(alienX, alienY, rocketX, rocketY):
    distance = math.sqrt(math.pow(alienX - rocketX, 2) + math.pow(alienY - rocketY, 2))
    if distance < 27:
        return True
    else:
        return False


# game run loop
running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerX_change = -0.2
            if event.key == pygame.K_d:
                playerX_change = 0.2
            if event.key == pygame.K_SPACE:
                if rocket_state is "ready":
                    rocketX = playerX
                    fire_rocket(rocketX, rocketY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    alienX += alienX_change
    if alienX <= 0:
        alienX_change = 0.1
        alienY += alienY_change
    elif alienX >= 736:
        alienX_change = -0.1
        alienY += alienY_change

    # rocket shoot
    if rocketY <= 0:
        rocketY = 480
        rocket_state = "ready"
    if rocket_state is "fire":
        fire_rocket(rocketX, rocketY)
        rocketY -= rocketY_change

    # Collision
    collision = isCollision(alienX, alienY, rocketX, rocketY)
    if collision:
        rocketY = 480
        rocket_state = "ready"
        score += 1
        print(score)
        alienX = random.randint(0, 734)
        alienY = random.randint(30, 150)

    player(playerX, playerY)
    alien(alienX, alienY)

    pygame.display.update()
