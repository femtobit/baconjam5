import random

import sfml as sf

from constants import *
from helpers import *

class Actor(sf.Drawable):
    def __init__(self):
        sf.Drawable.__init__(self)

        self.sprite = sf.CircleShape()

    def move(self, dr, dt):
        #print("Move actor by %s" % str(dr))
        #print(self.sprite.position)
        self.sprite.position += dr * dt
        #print(self.sprite.position)

    def draw(self, target, states):
        target.draw(self.sprite, states)

    @property
    def position(self):
        return self.sprite.position

    @position.setter
    def position(self, pos):
        self.sprite.position = pos

    @property
    def size(self):
        try:
            return self.sprite.size
        except AttributeError:
            return self.sprite.texture.size

    def collides_with(self, object):
        r1 = collision_rectangle(self)
        r2 = collision_rectangle(object)
        if ((r1.right < r2.left) or (r2.right < r1.left) or (r1.bottom < r2.top) or (r2.bottom < r1.top)):
            return False
        else:
            return True
class Player(Actor):
    def __init__(self, x, y):
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
        self.position = (x, y)
        
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

        self.direction = random_unit_vector()
        self.direction_timer = sf.Clock()

    def step(self, dt):
        if self.direction_timer.elapsed_time > sf.seconds(5) \
                or not MAP_RECT.contains(self.position + (self.direction * self.speed * 10)):
            self.direction = random_unit_vector()
            self.direction_timer.restart()

        self.move(self.direction * self.speed, dt)

    def hunt_player(self, player):
        player_direction = player.position - self.position
        delta = (player_direction / norm(player_direction)) * self.speed

        self.move(delta)

    def bite(self, player):
        if self.collides_with(player):
            player.health -= self.damage
            if player.health <= 0:
                window.close()

class Grue(Monster):
    def __init__(self, x, y):
        Monster.__init__(self)
        small_monster = sf.Texture.from_file("small_monster.png")
        self.sprite = sf.Sprite(small_monster)
        '''self.sprite = sf.RectangleShape()
        self.sprite.size = (5, 5)
        self.sprite.fill_color = sf.Color.BLUE'''
        self.sprite.position = (x, y)

        self.speed = 2
        self.damage = 1

        
        
