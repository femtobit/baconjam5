import random

import sfml as sf

from constants import *
from helpers import *

class Actor(sf.Drawable):
    def __init__(self):
        sf.Drawable.__init__(self)

        self.sprite = sf.CircleShape()

    def move(self, dx, dy):
        self.position += (dx, dy)

    def draw(self, target, states):
        target.draw(self.sprite, states)

    @property
    def position(self):
        return self.sprite.position

    @position.setter
    def position(self, pos):
        self.sprite.position = pos

    def collides_with(self, object):
        return dist(self.sprite.position, object.sprite.position) \
                      <= collision_radius(self) + collision_radius(object) - 3

class Player(Actor):
    def __init__(self, x, y, health):
        Actor.__init__(self)

        self.sprite = sf.RectangleShape()
        self.sprite.size = (30, 30)
        self.sprite.fill_color = sf.Color.RED
        self.position = (x, y)
        self.health = 5

    def draw(self, target, states):
        target.draw(self.sprite, states)

class Bus(Actor):
    def __init__(self, x, y, start_number):
        Actor.__init__(self)

        self.start_number = start_number

        self.sprite = sf.RectangleShape()
        self.sprite.size = (50, 50)
        self.sprite.outline_color = sf.Color.BLUE
        self.sprite.outline_thickness = 2
        self.sprite.position = (x, y)
        
    def draw(self, target, states):
        target.draw(self.sprite, states)

    def move(self):
        if (self.position.x > 342 and self.position.y > 0):
            super(self, Bus).move(0, 1)

    def get_number(self):
        return self.start_number

class Monster(Actor):
    def __init__(self):
        Actor.__init__(self)
        self.speed = 1
        self.damage = 5

    def step(self):
        while True:
            step = sf.Vector2(random.randrange(-1, 1), random.randrange(-1, 1))
            if MAP_RECT.contains(self.position + step):
                break
        self.move(step)

    def hunt_player(self, player):
        player_direction = player.position - self.position
        delta = (player_direction / vector.norm(player_direction)) * self.speed

        self.move(delta.x, delta.y)

    def bite(self, player):
        if self.collides_with(player):
            player.health -= self.damage
            if player.health <= 0:
                window.close()

class Grue(Monster):
    def __init__(self, x, y):
        Monster.__init__(self)

        self.sprite = sf.RectangleShape()
        self.sprite.size = (5, 5)
        self.sprite.fill_color = sf.Color.BLUE
        self.sprite.position = (x, y)

        self.speed = 0.5

        self.speed = 1.5
        self.damage = 1
