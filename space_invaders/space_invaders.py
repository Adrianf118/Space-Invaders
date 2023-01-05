import pygame
from pygame import mixer
import random
import math


# to initialize the pygame
pygame.init()

# to create screen
screen = pygame.display.set_mode((800, 600))

# backround
background = pygame.image.load('map.jpg') 

# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# title/icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# player
player_img = pygame.image.load('ship.png')
player_x = 370
player_y = 480
player_x_change = 0

# enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_enemy = 6
for i in range(num_enemy):
    enemy_img.append(pygame.image.load('enemy.png'))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(0.1)
    enemy_y_change.append(40)

# bullet
bullet_img = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 5
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# gave over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (225, 225, 225))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = font.render('GAME OVER', True, (225, 225, 225))
    screen.blit(over_text, (250, 250))

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

def fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2))
    if distance < 27:
        return True
    else:
        return False

# game loop
running = True
while running:
    # rgb = red, green, blue
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # check key that is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -0.3

            if event.key == pygame.K_RIGHT:
                player_x_change = 0.3

            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bullet_x = player_x
                    fire(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # checks boundaries
    player_x += player_x_change
    if player_x <= 0:
        player_x = 0

    elif player_x >= 736:
        player_x = 736

    # enemy boundary
    for i in range(num_enemy):

        # game over
        if enemy_y[i] > 200:
            for j in range(num_enemy):
                enemy_y[j] = 2000
            game_over_text()
            break


        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 0.1
            enemy_y[i] += enemy_y_change[i]

        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -0.1
            enemy_y[i] += enemy_y_change[i]

        # colision
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bullet_y = 480
            bullet_state = 'ready'
            score_value += 1
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)
        
        enemy(enemy_x[i], enemy_y[i], i)
        
    

    # bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = 'ready'
    if bullet_state is "fire":
        fire(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
        
    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()