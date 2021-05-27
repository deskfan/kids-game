# for player and program
#<div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>

#for gems
#Images licensed under Creative Commons Attribution 3.0. https://creativecommons.org/licenses/by/3.0/us/
#gem.png <div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>

#for background
#<a href='https://www.freepik.com/vectors/house'>House vector created by pikisuperstar - www.freepik.com</a>

#shake method
#https://github.com/kidscancode/gamedev/blob/master/tutorials/examples/shake.py


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


player_img = 'unicorn.png'
background_img = 'background.jpg'
icon_img = 'ufo.png'


SCREEN_WIDTH = 990
SCREEN_HEIGHT = 660
FPS = 120 # frames per second setting
fpsClock = pygame.time.Clock()

gems = ['gem.png','gem_orange.png']


class Player(pygame.sprite.Sprite):
    def __init__(self,image):
        super(Player,self).__init__()
        self.surf = pygame.image.load(image).convert()
        self.surf.set_colorkey((255,255,255),pygame.RLEACCEL)
        self.rect = self.surf.get_rect()
        self.score = 0


    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Gem:
    def __init__(self,image):
        self.surf = pygame.image.load(image)
        self.surf.set_colorkey((0,0,0),pygame.RLEACCEL)
        self.rect = self.surf.get_rect()
        self.randomize()
        self.collected = False
        self.last_collision = ()
        self.circle = Circle((self.rect.x,self.rect.y))

    def move(self):
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


    def randomize(self):
        self.rect.left = random.randint(50,900)
        self.rect.top = random.randint(50,600)

    def check_if_collected(self):
        if self.collected:
            self.rect.y -= 5
            self.circle.draw_circle()
        else:
            self.circle.radius = 30
            self.circle.px = 30

        if self.rect.y <= -50:#SCREEN_HEIGHT:
            self.collected = False
            self.randomize()




class Circle:
    def __init__(self,position):
        self.color = (255,255,255)
        self.position = position
        self.radius = 30
        self.px = 30
        self.start_time = pygame.time.get_ticks()

    def draw_circle(self):
        if self.radius <= SCREEN_WIDTH/2:
            self.radius = self.radius + 2
            if self.px <= 1:
                self.px = 1
            else:
                self.px = self.px - 1
            pygame.draw.circle(screen, self.color, self.position, self.radius, self.px)


class Villain:
    def __init__(self,image):
        self.surf = pygame.image.load(image).convert()
        self.surf.set_colorkey((0,0,0),pygame.RLEACCEL)
        self.rect = self.surf.get_rect()
        self.randomize()
        self.x_change = 1
        self.y_change = 0

    def move_around(self):
        self.rect.x = self.rect.x + self.x_change

        if self.rect.left <= 0:
            self.x_change = 1
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.x_change = -1
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


    def randomize(self):
        self.rect.left = random.randint(75,850)
        self.rect.top = random.randint(75,550)

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
gem1 = Gem(random.choice(gems))
gem2 = Gem(random.choice(gems))
villain = Villain('monster.png')

#determining collisions
def isCollision(playerX,playerY,objX,objY,threshold=45):
    distance = math.sqrt(math.pow(playerX-objX,2) + math.pow(playerY-objY,2))
    if distance < threshold:
        return True
    else:
        return False

# 'offset' will be our generator that produces the offset
# in the beginning, we start with a generator that 
# yields (0, 0) forever
offset = repeat((0, 0))

# this function creates our shake-generator
# it "moves" the screen to the left and right
# three times by yielding (-5, 0), (-10, 0),
# ... (-20, 0), (-15, 0) ... (20, 0) three times,
# then keeps yieling (0, 0)
def shake():
    s = -1
    for _ in range(0, 3):
        for x in range(0, 20, 5):
            yield (x*s, 0)
        for x in range(20, 0, 5):
            yield (x*s, 0)
        s *= -1
    while True:
        yield (0, 0)


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