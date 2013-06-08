#!/usr/bin/env python2
import math
import random
import sys

import sfml as sf

from actors import *
from helpers import *

WIDTH = 640
HEIGHT = 480

MAP_WIDTH = 960
MAP_HEIGHT = 1280

BUS_IMAGE = sf.Image.from_file("bus.png")

class Creature(Actor):
    def __init__(self):
        Actor.__init__(self)
        self.sprite = sf.RectangleShape()
        self.sprite.size = (5, 5)
        self.sprite.fill_color = sf.Color.BLUE
        self.sprite.position = (random.randrange(0, MAP_WIDTH), random.randrange(0, MAP_HEIGHT))

    def draw(self, target, states):
        target.draw(self.sprite, states)

class Overlay(sf.Drawable):
    def __init__(self, actor):
        self.actor = actor

        self.texture = sf.Texture.from_file("overlay.png")
        self.sprite = sf.Sprite(self.texture)

    def draw(self, target, states):
        center = (self.actor.sprite.position.x + self.actor.sprite.size.x / 2,
                  self.actor.sprite.position.y + self.actor.sprite.size.y / 2)
        self.sprite.position = center - self.texture.size / 2
        target.draw(self.sprite)

def main():
    PERIOD_OF_TIME = 0
    CAUGHT_A_BUS = False
    busses = []
    creatures = []
    window = sf.RenderWindow(sf.VideoMode(WIDTH, HEIGHT), "A Walk In The Dark")

    def end_game():
        window.close()

    player = Player(WIDTH / 2, HEIGHT / 2)
    
    for i in range (0, 20):
        creature = Creature()
        creatures.append(creature)

    background = sf.Sprite(sf.Texture.from_file("map1.png"))

    view = sf.View()
    view.reset(sf.Rectangle((0, 0), (WIDTH, HEIGHT)))
    window.view = view

    overlay = Overlay(player)

    timer = sf.Clock()
    timer2 = sf.Clock()

    while window.is_open:
        debug = []

        if timer.elapsed_time >= sf.seconds(15):
            PERIOD_OF_TIME += 1
            timer.restart()
            bus = Bus(342, MAP_HEIGHT, PERIOD_OF_TIME)
            busses.append(bus)

        for c in creatures:
            if c.collides_with(player):
                print("You were eaten, sorry(((")
                end_game()

        for b in busses:
            if b.collides_with(player):
                print("You were knocked down by the bus, sorry(((")
                end_game()

        for c in creatures:
            for b in busses:
                if b.collides_with(c):
                    creatures.remove(c)

        for event in window.events:
            if type(event) is sf.CloseEvent:
                end_game()

        debug.append("Pos: %s" % player.position)
        debug.append("Period: %i" % PERIOD_OF_TIME)

        delta = sf.Vector2()
        if sf.Keyboard.is_key_pressed(sf.Keyboard.LEFT) \
                and player.sprite.position.x > 0:
            delta += (-1,0)
        elif sf.Keyboard.is_key_pressed(sf.Keyboard.RIGHT) \
                and player.sprite.position.x + player.sprite.size.x < MAP_WIDTH:
            delta += (1,0)
        if sf.Keyboard.is_key_pressed(sf.Keyboard.UP) \
                and player.sprite.position.y > 0:
            delta += (0,-1)
        elif sf.Keyboard.is_key_pressed(sf.Keyboard.DOWN) \
                and player.sprite.position.y + player.sprite.size.y < MAP_HEIGHT:
            delta += (0,1)

        elif sf.Keyboard.is_key_pressed(sf.Keyboard.ESCAPE):
            window.close()

        if sf.Keyboard.is_key_pressed(sf.Keyboard.L_SHIFT):
            debug.append("sprint")
            delta *= 8
        else:
            delta *= 2

        view_delta = sf.Vector2()
        if player.sprite.position.x > WIDTH / 2 \
                and player.sprite.position.x < MAP_WIDTH - WIDTH / 2:
            view_delta += (delta.x, 0)
        if player.sprite.position.y > HEIGHT / 2 \
                and player.sprite.position.y < MAP_HEIGHT - HEIGHT / 2:
            view_delta += (0, delta.y)

        debug.append("dr: %s" % delta)
        player.move(delta.x, delta.y)
        view.move(view_delta.x, view_delta.y)    

        debug.append("Pos: %s" % player.sprite.position)
        debug.append("Period: %i" % PERIOD_OF_TIME)


        for bus in busses:
            if bus.sprite.position.y > 0:
                bus.move()
            else:
                busses.remove(bus)                

        #Monster movement
        if timer2.elapsed_time >= sf.milliseconds(50):
            for c in creatures:
                step = sf.Vector2(random.randrange(-1, 1), random.randrange(-1, 1))
                if step.x == -1 and c.sprite.position.x > 0:
                    c.move(step.x, 0)
                if step.x == 1 and c.sprite.position.x < MAP_WIDTH:
                    c.move(step.x, 0)
                if step.y == -1 and c.sprite.position.y > 0:
                    c.move(0, step.y)
                if step.y == 1 and c.sprite.positiony < MAP_HEIGHT:
                    c.move(0, step.y)

            timer2.restart()
             
        window.clear()
        window.draw(background)
        window.draw(player)
        for bus in busses:
            window.draw(bus)
        for creature in creatures:
            window.draw(creature)
        window.draw(overlay)

        window.view = window.default_view

        debug_text = sf.Text(", ".join(debug))
        debug_text.color = sf.Color.RED
        debug_text.position = (0, HEIGHT - 20)
        debug_text.character_size = 12
        window.draw(debug_text)

        window.display()


if __name__ == "__main__":
    main()
