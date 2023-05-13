from pygame import mixer
import pygame as pg
import random
import math

# Initialize the pygame
pg.init()

# Create the screen
screen = pg.display.set_mode((800, 600))

# Background
background = pg.image.load('Space.png')
moon = pg.image.load('moon.png')

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and icon
pg.display.set_caption("Shooting Loads in Space: The Sequel")
icon = pg.image.load('space-ship.png')
pg.display.set_icon(icon)

# Player ship
playerShip = pg.image.load('player-spaceship.png')
playerX = 360
playerY = 480
playerX_change = 0
playerY_change = 0

# Alien enemy
alien1 = []
alien1X = []
alien1Y = []
alien1X_change = []
alien1Y_change = []
num_enemies = 12

for i in range(num_enemies):
    alien1.append(pg.image.load('alien1.png'))
    alien1X.append(random.randint(0, 736))
    alien1Y.append(random.randint(50, 200))
    alien1X_change.append(3)
    alien1Y_change.append(32)

# Projectile
bullet = pg.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 10
# Ready state means you cannot see the bullet on the screen
# Fire state means the bullet is currently moving
bullet_state = "ready"

# Player socre
player_score = 0
font = pg.font.Font('freesansbold.ttf', 20)
textX = 10
textY = 10

def show_score(x, y):
    score = font.render("Score : " + str(player_score), True, (255, 0, 0))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerShip, (x, y))

def enemy1(x, y, i):
    screen.blit(alien1[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x + 16, y + 10))

def is_Collision(enemyX, enemyY, bulletX, bulletY):    
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True

# Game Loop
running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    screen.blit(moon, (550, 80))
 
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # Check for left/right keystroke
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                playerX_change = -5
            if event.key == pg.K_RIGHT:
                playerX_change = 5
            if event.key == pg.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        ##### Allows player to move up/down
        # if event.type == pg.KEYDOWN:
        #     if event.key == pg.K_UP:
        #         playerY_change = -5
        # if event.type == pg.KEYDOWN:
        #     if event.key == pg.K_DOWN:
        #         playerY_change = 5
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                playerX_change = 0

        ##### Makes player border for top and bottom, not needed since player cannot move up/down
        # if event.type == pg.KEYUP:
        #     if event.key == pg.K_UP or event.key == pg.K_DOWN:
        #         playerY_change = 0

    playerX += playerX_change
    playerY += playerY_change
    # alien1X += alien1X_change
    # alien1Y += alien1Y_change

    # Player boundary for left and right side of screen
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536
    
    # Enemy movement
    for i in range(num_enemies):
        alien1X[i] += alien1X_change[i]
        if alien1X[i] <= 0:
            alien1X_change[i] = 3
            alien1Y[i] += alien1Y_change[i]
        elif alien1X[i] >= 736:
            alien1X_change[i] = -3
            alien1Y[i] += alien1Y_change[i]
        # Collision
        collision = is_Collision(alien1X[i], alien1Y[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('hit.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            player_score += 100
            alien1X[i] = random.randint(0, 736)
            alien1Y[i] = random.randint(50, 200)

        enemy1(alien1X[i], alien1Y[i], i)

    if bulletY <= 10:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change  
    
    player(playerX, playerY)
    show_score(textX, textY)
    pg.display.update()