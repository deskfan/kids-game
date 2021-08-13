# for gems
# Images licensed under Creative Commons Attribution 3.0. https://creativecommons.org/licenses/by/3.0/us/
# gem.png <div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>

import random
from os import path

import pygame
from pygame.locals import K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, KEYDOWN, QUIT

SCREEN_WIDTH = 990
SCREEN_HEIGHT = 660


class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        super(Player, self).__init__()
        self.surf_image = pygame.image.load(image).convert()
        self.surf_going_right = self.surf_image
        self.surf_going_left = pygame.transform.flip(self.surf_image, True, False)

        self.surf_going_right.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        self.surf_going_left.set_colorkey((255, 255, 255), pygame.RLEACCEL)

        self.surf = self.surf_going_right
        self.rect = self.surf.get_rect()
        self.score = 0
        self.speed = 5
        self.going_left = False

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
            self.going_left = True
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
            self.going_left = False
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.going_left == True:
            self.surf = self.surf_going_left
        if self.going_left == False:
            self.surf = self.surf_going_right

    def update_js(self, axis, joy_buttons):
        if axis == "x":
            for b in joy_buttons:
                self.rect.move_ip(b, 0)
        else:
            for b in joy_buttons:
                self.rect.move_ip(0, b)

    def update_js_all(self, joy_buttons):
        for b in joy_buttons:
            move = joy_buttons.pop()
            self.rect.move_ip(move[0], move[1])


class Gem:
    def __init__(self, image, screen):
        self.screen = screen
        self.image = image
        self.angle = 0
        self.display = pygame.image.load(image)
        self.surf = pygame.transform.rotate(self.display, self.angle)
        self.surf.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        self.rect = self.surf.get_rect()
        self.randomize()
        self.collected = False
        self.last_collision = ()
        self.circle = Circle((self.rect.x, self.rect.y))

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
        self.rect.left = random.randint(50, 900)
        self.rect.top = random.randint(50, 600)

    def check_if_collected(self):
        if self.collected:
            self.rect.y -= 5
            self.circle.draw_circle(self.screen)
        else:
            self.circle.radius = 30
            self.circle.px = 30

        if self.rect.y <= -50:
            self.collected = False
            self.randomize()

    def check_if_villain_collected(self):
        if self.collected:
            self.rect.y += 7
            self.circle.draw_circle(self.screen, villain=True)

        if self.rect.y >= SCREEN_HEIGHT + 50:
            self.collected = False
            self.randomize()


class Villain:
    def __init__(self, image):
        self.surf = pygame.image.load(image).convert()
        self.surf.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        self.rect = self.surf.get_rect()
        self.randomize()
        self.x_change = 3
        self.y_change = 3

    def move_around(self):
        self.rect.x = self.rect.x + self.x_change
        self.rect.y = self.rect.y + self.y_change

        if self.rect.left <= 0:
            self.x_change = 1
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.x_change = -1
        if self.rect.top <= 0:
            self.y_change = 1
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.y_change = -1

    def randomize(self):
        self.rect.left = random.randint(75, 850)
        self.rect.top = random.randint(75, 550)


class Circle:
    def __init__(self, position):
        self.color = (255, 255, 255)
        self.position = position
        self.radius = 30
        self.px = 30

    def get_color(self, villain=False):
        if villain == False:
            options = [(253, 7, 237), (155, 7, 253), (255, 255, 255), (7, 237, 253)]
        else:
            optiosn = [(0, 0, 0)]
        return random.choice(options)

    def draw_circle(self, screen, villain=False):
        if self.radius <= SCREEN_WIDTH / 2:
            self.radius = self.radius + 2
            if self.px <= 1:
                self.px = 1
            else:
                self.px = self.px - 1
            pygame.draw.circle(
                screen,
                self.get_color(villain=False),
                self.position,
                self.radius,
                self.px,
            )
