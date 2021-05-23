# for player and program
#<div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>

#for gems
#Images licensed under Creative Commons Attribution 3.0. https://creativecommons.org/licenses/by/3.0/us/
#gem.png <div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>

#for backrgound
#<a href='https://www.freepik.com/vectors/house'>House vector created by pikisuperstar - www.freepik.com</a>


import random
import pygame
import math
import time

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


SCREEN_WIDTH = 990
SCREEN_HEIGHT = 660

FPS = 120 # frames per second setting
fpsClock = pygame.time.Clock()


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


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



running = True

c = Circle((150,150))


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

    screen.fill((0,0,0))

    
    if pygame.time.get_ticks() - c.start_time < 3000:
        c.draw_circle()



    pygame.display.flip()
    fpsClock.tick(FPS)
