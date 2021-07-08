# for player and program
#<div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>


#for background
#<a href='https://www.freepik.com/vectors/house'>House vector created by pikisuperstar - www.freepik.com</a>


import random
import pygame
import math
from random import randint
from itertools import repeat
from pygame.constants import JOYBUTTONDOWN
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from characters import Player, Villain, Gem,SCREEN_HEIGHT,SCREEN_WIDTH
from game_functions import * 

dir = r'C:\\Users\\murph\\VSCode_workspace\\kids-game\\'

player_img = dir + 'img\\unicorn.png'
background_img = dir +  'img\\background.jpg'
icon_img =  dir + 'img\\ufo.png'
gems = [ dir + 'img\\gem.png', dir + 'img\\gem_orange.png']
monster_img =  dir + 'img\\monster.png'

PLAYER_SPEED = 5

########################################

pygame.init()

fpsClock = pygame.time.Clock()
#programIcon = pygame.image.load(icon_img)
background = pygame.transform.scale(pygame.image.load(background_img),(990,660))
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Zoe Town")
#pygame.display.set_icon(programIcon)
#loot_sound = pygame.mixer.Sound("crash.wav")



# score
base_font = pygame.font.Font(None,32)
color = pygame.Color('orange')



# Initializing sprites and loot
player = Player(player_img)
gem1 = Gem(gems[0],screen)
gem2 = Gem(gems[1],screen)
villain = Villain(monster_img)


# Initializing joystick
try:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
except:
    print("no joystick")


# setting up game loop
running = True

while running:



    ################ HANDLE INPUT EVENTS ###############################
    # loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        if event.type == QUIT:
            running = False

    screen.blit(background,(0,0)) #SCENE
    display_score(player,screen) #SCORE


    ############### HANDLE PLAYER MOVEMENT ###############################
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
 
    try:
        axis_x = joystick.get_axis(2)
        axis_y = joystick.get_axis(3)

        x_change = make_coordinate(axis_x)
        y_change = make_coordinate(axis_y)

        slow_button = joystick.get_button(4)
        fast_button = joystick.get_button(5)
        player.speed = PLAYER_SPEED + fast_button * 10 - slow_button * 2
        player.rect.move_ip(x_change*player.speed,y_change*player.speed)

    except:
        player.speed = PLAYER_SPEED

    ############### HANDLE COLLISIONS ###############################
    player_gets_gem1 = isCollision(player.rect.x,player.rect.y,gem1.rect.x,gem1.rect.y)
    player_gets_gem2 = isCollision(player.rect.x,player.rect.y,gem2.rect.x,gem2.rect.y)
#    player_hit_villain = isCollision(player.rect.x,player.rect.y,villain.rect.x,villain.rect.y,80)
    villain_hit_gem1 = isCollision(gem1.rect.x,gem1.rect.y,villain.rect.x,villain.rect.y,100)
    villain_hit_gem2 = isCollision(gem2.rect.x,gem2.rect.y,villain.rect.x,villain.rect.y,100)

    if player_gets_gem1 and gem1.collected == False:
        gem1.collected = True
        gem1.last_collision = (gem1.rect.x,gem1.rect.y)
        gem1.circle.position = gem1.last_collision
        player.score += 1
        
    gem1.check_if_collected()

    if player_gets_gem2 and gem2.collected == False:
        gem2.collected = True
        gem2.last_collision = (gem2.rect.x,gem2.rect.y)
        gem2.circle.position = gem2.last_collision
        player.score += 1

    gem2.check_if_collected()

#    if player_hit_villain:
#        offset = shake()
#        player.rect.x = 0
#        player.rect.y = 0
#        player.score -= 50

    if villain_hit_gem1 and gem1.collected == False:
        gem1.collected = True
        gem1.last_collision = (gem1.rect.x,gem1.rect.y)
        gem1.circle.position = gem1.last_collision
        player.score -= 1
    gem1.check_if_villain_collected()


    if villain_hit_gem2 and gem2.collected == False:
        gem2.collected = True
        gem2.last_collision = (gem2.rect.x,gem2.rect.y)
        gem2.circle.position = gem2.last_collision
        player.score -= 1
    gem2.check_if_villain_collected()



    villain.move_around()


    ############### DRAW SCENE, SPRITES AND LOOT #########################
    screen.blit(player.surf,player.rect) #PLAYER
    screen.blit(gem1.surf,gem1.rect)
    screen.blit(gem2.surf,gem2.rect)
    screen.blit(villain.surf,villain.rect)
    screen.blit(screen, next(offset)) #CHECK FOR SHAKE


    pygame.display.flip()
    fpsClock.tick(FPS)