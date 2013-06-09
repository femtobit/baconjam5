#!/usr/bin/env python2
#-*- encoding: utf-8 -*-
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

#BUS_IMAGE = sf.Image.from_file("bus.png")

class Overlay(sf.Drawable):
    def __init__(self, actor):
        self.actor = actor

        self.texture = sf.Texture.from_file("overlay.png")
        self.sprite = sf.Sprite(self.texture)

    def draw(self, target, states):
        center = (self.actor.position.x + self.actor.size.x / 2,
                  self.actor.position.y + self.actor.size.y / 2)
        self.sprite.position = center - self.texture.size / 2
        target.draw(self.sprite)

class PointDisplay(sf.Drawable):
    def __init__(self, rect, max_points, color):
        self.rect = rect
        self.max_points = max_points
        self.points = max_points
        self.color = color

    def draw(self, target, states):
        dx = self.rect.width / self.max_points
        width = self.rect.width / (self.max_points + 1)
        for i in range(0, self.points):
            shape = sf.RectangleShape((width, self.rect.height))
            shape.fill_color = self.color
            shape.position = (self.rect.position.y + i * dx,
                                    self.rect.position.y)
            target.draw(shape, states)

def player_movement_vector(player):
    delta = sf.Vector2()
    if sf.Keyboard.is_key_pressed(sf.Keyboard.LEFT) \
            and player.position.x > 0:
                delta += (-1,0)
    elif sf.Keyboard.is_key_pressed(sf.Keyboard.RIGHT) \
            and player.position.x + player.size.x < MAP_WIDTH:
                delta += (1,0)
    if sf.Keyboard.is_key_pressed(sf.Keyboard.UP) \
            and player.position.y > 0:
                delta += (0,-1)
    elif sf.Keyboard.is_key_pressed(sf.Keyboard.DOWN) \
            and player.position.y + player.size.y < MAP_HEIGHT:
                delta += (0,1)
    delta = normalize(delta)

    if sf.Keyboard.is_key_pressed(sf.Keyboard.L_SHIFT):
        delta *= 8
    else:
        delta *= 2

    return delta

def main():
    random.seed(datetime.datetime.now())

    PERIOD_OF_TIME = 0
    CAUGHT_A_BUS = False
    busses = []
    creatures = []
    lives = []
    window = sf.RenderWindow(sf.VideoMode(WIDTH, HEIGHT), "A Walk In The Dark")
    
    def end_game():
        window.close()

    player = Player(WIDTH / 2, HEIGHT / 2)
        
    for i in range (0, NUMBER_OF_GRUES):
        while True:
            point = (random.randrange(0, MAP_WIDTH), random.randrange(0, MAP_HEIGHT))
            if dist(point, player.position) > 250:
                break
        creature = Grue(*point)
        print("New Grue at (%s)" % (creature.position))
        creatures.append(creature)

    for i in range(0, 5):
        heal = Lives(random.randrange(0, MAP_WIDTH), random.randrange(0, MAP_HEIGHT))
        lives.append(heal)
    
    background = sf.Sprite(sf.Texture.from_file("map2.png"))

    view = sf.View()
    view.reset(sf.Rectangle((0, 0), (WIDTH, HEIGHT)))
    window.view = view

    overlay = Overlay(player)

    life_point_display = PointDisplay(sf.Rectangle((WIDTH - 100, 10), (100, 10)),
            player.health, sf.Color.RED)

    step_timer = sf.Clock()
    boss_time = sf.Clock()

    while window.is_open:
        debug = []

        dt = step_timer.elapsed_time.milliseconds / 16.0
        step_timer.restart()
        debug.append("(dt=%i/16 ms)" % dt) 
        if boss_time.elapsed_time == sf.seconds(30):
            boss = Boss(random.randrange(0, MAP_WIDTH), random.randrange(0, MAP_HEIGHT))
            creatures.append(boss)
        if boss_time.elapsed_time == sf.seconds(45):
            creatures.remove(boss)
            boss_time.restart()

        for c in creatures:
            if c.collides_with(player):
                creatures.remove(c)
                c.bite(player)
                if player.health <= 0:
                    print("You loose, sorry")
                    window.close()

        for h in lives:
            if h.collides_with(player):
                lives.remove(h)
                player.health += 1

        for event in window.events:
            if type(event) is sf.CloseEvent:
                window.close()

        debug.append("Pos: %s" % player.position)
        debug.append("Period: %i" % PERIOD_OF_TIME)

        delta = player_movement_vector(player)

        view_delta = sf.Vector2()
        if player.position.x > WIDTH / 2 \
                and player.position.x < MAP_WIDTH - WIDTH / 2:
            view_delta += (delta.x, 0)
        if player.position.y > HEIGHT / 2 \
                and player.position.y < MAP_HEIGHT - HEIGHT / 2:
            view_delta += (0, delta.y)

        debug.append("dr: %s" % delta)
        player.move(delta, dt)
        sf.Listener.set_position((player.position.x, player.position.y, 0))
        view.move(view_delta.x * dt, view_delta.y * dt)

        debug.append("Pos: %s" % player.sprite.position)
        debug.append("Period: %i" % PERIOD_OF_TIME)

        #Monster movement
        for creature in creatures:
            creature.step(player, dt)
            creature.sound_tick()
             
        window.clear()
        window.draw(background)
        window.draw(player)
        for creature in creatures:
            window.draw(creature)
        for heal in lives:
            window.draw(heal)
        window.draw(overlay)

        window.view = window.default_view

        debug_text = sf.Text(", ".join(debug))
        debug_text.color = sf.Color.RED
        debug_text.position = (0, HEIGHT - 20)
        debug_text.character_size = 12
        window.draw(debug_text)
        life_point_display.points = player.health
        window.draw(life_point_display)

        window.display()


if __name__ == "__main__":
    main()
