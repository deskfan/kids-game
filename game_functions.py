#shake method
#https://github.com/kidscancode/gamedev/blob/master/tutorials/examples/shake.py



import math
from itertools import repeat
import pygame

player_img = 'img/unicorn.png'
background_img = 'img/background.jpg'
icon_img = 'img/ufo.png'
gems = ['img/gem.png','img/gem_orange.png']
monster_img = 'img/monster.png'
FPS = 120 # frames per second setting


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


def display_score(player,screen):
    score_font = pygame.font.Font(None,32)
    score_rect = pygame.Rect(700,600,140,32)
    pygame.draw.rect(screen,pygame.Color('purple'),score_rect,4)
    score_surface = score_font.render(f'Score is: {player.score}',True,(102,51,153))
    screen.blit(score_surface,(score_rect.x+5,score_rect.y+5))
    score_rect.w = max(200,score_surface.get_width()+ 10)    


def make_coordinate(value):
    if value < -0.25:
        return -1
    elif value > 0.25:
        return 1
    else:
        return 0
