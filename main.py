# for player and program
#<div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>


#for background
#<a href='https://www.freepik.com/vectors/house'>House vector created by pikisuperstar - www.freepik.com</a>


import random
import pygame
import math
from random import randint
from itertools import repeat

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
from game_functions import isCollision, shake, offset


player_img = 'img/unicorn.png'
background_img = 'img/background.jpg'
icon_img = 'img/ufo.png'
gems = ['img/gem.png','img/gem_orange.png']
monster_img = 'img/monster.png'



FPS = 120 # frames per second setting
fpsClock = pygame.time.Clock()


pygame.init()

########################################
pygame.display.set_caption("Zoe Town")
#programIcon = pygame.image.load(icon_img)
background = pygame.transform.scale(pygame.image.load(background_img),(990,660))
#pygame.display.set_icon(programIcon)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# User Input
base_font = pygame.font.Font(None,32)
input_rect = pygame.Rect(700,600,140,32)
color_active = pygame.Color('orange')
color_passive = pygame.Color('orange')
color = color_passive
active = False

# Score
score_rect = pygame.Rect(700,600,140,32)



# Initializing my sprites
player = Player(player_img)
gem1 = Gem(random.choice(gems),screen)
gem2 = Gem(random.choice(gems),screen)
villain = Villain(monster_img)




# setting up for my while loop
running = True

while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        if event.type == QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False

        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    player.update(pressed_keys)

    screen.fill((0,0,0))
    screen.blit(background,(0,0))

    ################ SCORE ###############################
    pygame.draw.rect(screen,pygame.Color('purple'),score_rect,4)
    score_surface = base_font.render(f'Score is: {player.score}',True,(102,51,153))
    screen.blit(score_surface,(score_rect.x+5,score_rect.y+5))
    score_rect.w = max(200,score_surface.get_width()+ 10)
    ################ SCORE ###############################


    ################ INPUT BUSINESS ###############################
#    if active:
#        color = color_active
#    else:
#        color  = color_passive

#    pygame.draw.rect(screen,color,input_rect,4)
#    text_surface = base_font.render(f'Score is: {player.score}',True,(102,51,153))
#    screen.blit(text_surface,(input_rect.x+5,input_rect.y+5))
#    input_rect.w = max(200,text_surface.get_width()+ 10)
    ################ INPUT BUSINESS ###############################


    collision1 = isCollision(player.rect.x,player.rect.y,gem1.rect.x,gem1.rect.y)
    collision2 = isCollision(player.rect.x,player.rect.y,gem2.rect.x,gem2.rect.y)
    collision3 = isCollision(player.rect.x,player.rect.y,villain.rect.x,villain.rect.y,80)

    if collision1:
        gem1.collected = True
        gem1.last_collision = (gem1.rect.x,gem1.rect.y)
        gem1.circle.position = gem1.last_collision
        player.score += 1

        
    gem1.check_if_collected()

    if collision2:
        gem2.collected = True
        gem2.last_collision = (gem2.rect.x,gem2.rect.y)
        gem2.circle.position = gem2.last_collision
        player.score += 1


    gem2.check_if_collected()

    if collision3:
        print("collision!!")
        offset = shake()
        player.rect.x = 0
        player.rect.y = 0
        player.score -= 50


    villain.move_around()

    screen.blit(player.surf,player.rect)
    screen.blit(gem1.surf,gem1.rect)
    screen.blit(gem2.surf,gem2.rect)
    screen.blit(villain.surf,villain.rect)
    screen.blit(screen, next(offset))


    pygame.display.flip()
    fpsClock.tick(FPS)