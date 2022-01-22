import pygame
import random
import math
from pygame import mixer

# initialize pygame
pygame.init()

# screen create tuple (pixels)
screen = pygame.display.set_mode((800, 600))

# BG
bg = pygame.image.load("bg.jpg")
mixer.music.load("bg.wav")
mixer.music.play(-1)
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
alienIMG = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
alienNum = 6
for i in range(alienNum):
    alienIMG.append(pygame.image.load("alien.png"))
    alienX.append(random.randint(0, 734))
    alienY.append(random.randint(30, 150))
    alienX_change.append(0.1)
    alienY_change.append(40)

# Rocket
rocketIMG = pygame.image.load("rocket.png")
rocketX = 0
rocketY = 480
rocketY_change = 0.3
rocket_state = "ready"

# Score
score = 0
font = pygame.font.Font("Starjedi.ttf", 32)
textX = 10
textY = 10

# game over
over_font = pygame.font.Font("Starjedi.ttf", 64)


def game_over():
    over_txt = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_txt, (200,250))


def show_score(x, y):
    score_font = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(score_font, (10, 10))


def player(x, y):
    screen.blit(playerIMG, (x, y))


def alien(x, y, i):
    screen.blit(alienIMG[i], (x, y))


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
                if rocket_state == "ready":
                    rocket_sound = mixer.Sound("laser.wav")
                    rocket_sound.play()
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

    for i in range(alienNum):

        # game over
        if alienY[i] > 440:
            for j in range(alienNum):
                alienY[j] = 2000
            game_over()
            break

        alienX[i] += alienX_change[i]
        if alienX[i] <= 0:
            alienX_change[i] = 0.1
            alienY[i] += alienY_change[i]
        elif alienX[i] >= 736:
            alienX_change[i] = -0.1
            alienY[i] += alienY_change[i]
        # Collision
        collision = isCollision(alienX[i], alienY[i], rocketX, rocketY)
        if collision:
            rocketY = 480
            rocket_state = "ready"
            score += 1
            kill_sound = mixer.Sound("kill.wav")
            kill_sound.play()
            alienX[i] = random.randint(0, 734)
            alienY[i] = random.randint(30, 150)
        alien(alienX[i], alienY[i], i)
    # rocket shoot
    if rocketY <= 0:
        rocketY = 480
        rocket_state = "ready"
    if rocket_state == "fire":
        fire_rocket(rocketX, rocketY)
        rocketY -= rocketY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
