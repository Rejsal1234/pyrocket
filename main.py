import pygame
import random
import math
from pygame import mixer

# space invader game using pygame

# initialize pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# background
backgroundImg = pygame.image.load('background.png')

# background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('space.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('space.png')
playerX = 370
playerX_change = 0
playerY = 480
playerY_change = 0

# enemies
enemyImg = []
enemyX = []
enemyX_change = []
enemyY = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyX_change.append(3)
    enemyY.append(random.randint(50, 150))
    enemyY_change.append(40)

# bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletX_change = 0
bulletY = 480
bulletY_change = 10
is_bullet_fired = False

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 28)
textX = 10
textY = 10

# game over
game_over_font = pygame.font.Font('RampartOne-Regular.ttf', 64)
is_game_over = False


def display_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over(x, y):
    game_over_text = game_over_font.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(game_over_text, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, pos):
    screen.blit(enemyImg[pos], (x, y))


def fire_bullet(x, y):
    global is_bullet_fired
    is_bullet_fired = True
    screen.blit(bulletImg, (x + 16, y - 10))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2))))
    if distance < 27:
        return True
    else:
        return False


def is_collide_with_player(enemy_x, enemy_y, player_x, player_y):
    distance = math.sqrt(((math.pow(enemy_x - player_x, 2)) + (math.pow(enemy_y - player_y, 2))))
    if distance < 36:
        return True
    else:
        return False


# game loop
running = True
while running:

    # screen color - should be in running to make persistent
    screen.fill((0, 0, 0))
    screen.blit(backgroundImg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # check if keystroke is pressed for up/down/left/right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                if not is_bullet_fired:
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # player boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy boundaries
    for i in range(num_of_enemies):
        if is_collide_with_player(enemyX[i], enemyY[i], playerX, playerY):
            is_game_over = True
            num_of_enemies = 0
            mixer.music.stop()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 735:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # collision occurs
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bullet_sound = mixer.Sound('explosion.wav')
            bullet_sound.play()
            if is_bullet_fired:
                score_value += 1
            is_bullet_fired = False
            bulletY = 480
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        is_bullet_fired = False
        bulletY = 480
    if is_bullet_fired:
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    display_score(textX, textY)
    if is_game_over:
        game_over(200, 250)
    pygame.display.update()
