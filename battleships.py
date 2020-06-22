import math
import random
import pygame
from pygame import mixer

# Intialize the pygame by calling __init__()

pygame.init()

# create the screen

screen = pygame.display.set_mode((800, 600))

# Background Image

background = pygame.image.load('other_assets/space.png')

# Background Sound

mixer.music.load('sounds/background.wav')
mixer.music.play(-1)

# Set Title

pygame.display.set_caption('battle ships @ankush_singh_gandhi)')

# Icon of the Game

icon = pygame.image.load('assets/ship.png')
pygame.display.set_icon(icon)

# Battleship

battleshipImg = pygame.image.load('assets/battleship.png')
battle_ship_x = 370
battle_ship_y = 500
battle_ship_x_change = 0

# destroy_ship
golden_battle_ship = False
destroy_shipImg = []
destroy_shipX = []
destroy_shipY = []
destroy_shipX_change = []
destroy_shipY_change = []
ships = []
num_of_destroyships = 6

for i in range(num_of_destroyships):
    ship = random.choice(['assets/destroy_ship.png', 'assets/destroy_ship.png',
                      'assets/destroy_ship.png', 'assets/destroy_ship2.png'])
    ships.append(ship)
    destroy_shipImg.append(pygame.image.load(ship))
    destroy_shipX.append(random.randint(0, 736))
    destroy_shipY.append(random.randint(50, 150))
    destroy_shipX_change.append(4)
    destroy_shipY_change.append(40)
    
# Ready - You can't see the fire on the screen
# Fire - The fire is currently moving

fireImg = pygame.image.load('assets/fire.png')
fireX = 0
fireY = 480
fireX_change = 0
fireY_change = 10
fire_state = 'ready'

# Scores..

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over Baby..

over_font = pygame.font.Font('freesansbold.ttf', 64)
extra_points_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render('Score : ' + str(score_value), True, (255, 255,
                        255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def battleship(x, y):
    screen.blit(battleshipImg, (x, y))


def destroy_ship(x, y, i):
    screen.blit(destroy_shipImg[i], (x, y))


def fire_fire(x, y):
    global fire_state
    fire_state = 'fire'
    screen.blit(fireImg, (x + 16, y + 10))


def blast(
    destroy_shipX,
    destroy_shipY,
    fireX,
    fireY,
    ):
    distance = math.sqrt(math.pow(destroy_shipX - fireX, 2)
                         + math.pow(destroy_shipY - fireY, 2))
    if distance < 27:
        return True
    else:
        return False


# Main Game Loop

running = True
while running:

    # Screen Window Background

    screen.fill((0, 0, 0))

    # Background Image

    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # check keystroke is right or left

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                battle_ship_x_change = -5
            if event.key == pygame.K_RIGHT:
                battle_ship_x_change = 5
            if event.key == pygame.K_SPACE:
                if fire_state is 'ready':
                    fireSound = mixer.Sound('sounds/laser1.wav')
                    fireSound.play()

                    # Get the current x cordinate of the battleship

                    fireX = battle_ship_x
                    fire_fire(fireX, fireY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key \
                == pygame.K_RIGHT:
                battle_ship_x_change = 0


    battle_ship_x += battle_ship_x_change
    if battle_ship_x <= 0:
        battle_ship_x = 0
    elif battle_ship_x >= 736:
        battle_ship_x = 736

    # destroy_ship Movement

    for i in range(num_of_destroyships):

        # Game Over

        if destroy_shipY[i] > 440:
            for j in range(num_of_destroyships):
                destroy_shipY[j] = 2000
            game_over_text()
            break

        destroy_shipX[i] += destroy_shipX_change[i]
        if destroy_shipX[i] <= 0:
            destroy_shipX_change[i] = 4
            destroy_shipY[i] += destroy_shipY_change[i]
        elif destroy_shipX[i] >= 736:
            destroy_shipX_change[i] = -4
            destroy_shipY[i] += destroy_shipY_change[i]

        # Blast

        boom = blast(destroy_shipX[i], destroy_shipY[i],
                                fireX, fireY)
        if boom:
            if ships[i] == ('assets/destroy_ship.png'):
                if golden_battle_ship == True:
                    explosionSound = mixer.Sound('sounds/Explosion.wav')
                    explosionSound.play()
                    fireY = 480
                    fire_state = 'ready'
                    score_value += 3
                    destroy_shipX[i] = random.randint(0, 736)
                    destroy_shipY[i] = random.randint(50, 150)
                else:
                    explosionSound = mixer.Sound('sounds/Explosion.wav')
                    explosionSound.play()
                    fireY = 480
                    fire_state = 'ready'
                    score_value += 1
                    destroy_shipX[i] = random.randint(0, 736)
                    destroy_shipY[i] = random.randint(50, 150)
                    
            else:
                explosionSound = mixer.Sound('sounds/Explosion.wav')
                explosionSound.play()
                fireY = 480
                fire_state = 'ready'
                score_value += 50
                destroy_shipX[i] = random.randint(0, 736)
                destroy_shipY[i] = random.randint(50, 150)
                battleshipImg = pygame.image.load('assets/battleship2.png')
                golden_battle_ship = True
            

        destroy_ship(destroy_shipX[i], destroy_shipY[i], i)

    # fire Movement

    if fireY <= 0:
        fireY = 480
        fire_state = 'ready'

    if fire_state is 'fire':
        fire_fire(fireX, fireY)
        fireY -= fireY_change

    battleship(battle_ship_x, battle_ship_y)
    show_score(textX, testY)
    pygame.display.update()
