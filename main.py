#!/usr/bin/env python2
import datetime
import math
import random
import sys

import sfml as sf

from actors import *
from constants import *
from helpers import *

WIDTH = 640
HEIGHT = 480

BUS_IMAGE = sf.Image.from_file("bus.png")

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
    random.seed(datetime.datetime.now())

    PERIOD_OF_TIME = 0
    CAUGHT_A_BUS = False
    busses = []
    creatures = []

    window = sf.RenderWindow(sf.VideoMode(WIDTH, HEIGHT), "A Walk In The Dark")
    
    def end_game():
        window.close()

    player = Player(WIDTH / 2, HEIGHT / 2)
    
    for i in range (0, NUMBER_OF_GRUES):
        creature = Grue(random.randrange(0, MAP_WIDTH),
                random.randrange(0, MAP_HEIGHT))
        print("New Grue at (%s)" % (creature.position))
        creatures.append(creature)

    background = sf.Sprite(sf.Texture.from_file("map2.png"))

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
            '''bus = Bus(PERIOD_OF_TIME)
            busses.append(bus)'''

        for c in creatures:
            debug.append("Grues: ")
            if c.collides_with(player):
                print("You were eaten, sorry(((")
                window.close()

        '''for b in busses:
            if b.collides_with(player):
                print("You were knocked down by the bus, sorry(((")
                window.close()

        for c in creatures:
            for b in busses:
                if b.collides_with(c):
                    creatures.remove(c)'''

        for event in window.events:
            if type(event) is sf.CloseEvent:
                window.close()

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
        player.move(delta)
        view.move(view_delta.x, view_delta.y)    

        debug.append("Pos: %s" % player.sprite.position)
        debug.append("Period: %i" % PERIOD_OF_TIME)


        '''for bus in busses:
            if bus.sprite.position.y > 0:
                bus.move(0, -1)
            else:
                busses.remove(bus)
            for bus in busses:
                bus.move()'''

        #Monster movement
        for creature in creatures:
            creature.step()
             
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
