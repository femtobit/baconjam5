#!/usr/bin/env python2
import sfml as sf
import random
import math

WIDTH = 640
HEIGHT = 480

MAP_WIDTH = 960
MAP_HEIGHT = 1280

PERIOD_OF_TIME = 0
COUGHT_A_BUS = False
busses = []
creatures = []
COLLIDE = False
BUS_IMAGE = sf.Image.from_file("bus.png")
# create the main window
window = sf.RenderWindow(sf.VideoMode(WIDTH, HEIGHT), "pySFML Window")

#helper functions
def dist(p,q):
    return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)

def radius_for_collision(object):
    return object.sprite.size.x / 2

def end_game():
    timer.restart()
    timer2.restart()
    busses = []
    creatures = []
    PERIOD_OF_TIME = 0
    window.close()

class Actor(sf.Drawable):
    def __init__(self):
        sf.Drawable.__init__(self)

        self.velocity = 1

    def move(self, dx, dy):
        self.sprite.position += (dx, dy) * self.velocity

    def draw(self, target, states):
        target.draw(self.sprite, states)
    def is_collide(self, object):
        if dist(self.sprite.position, object.sprite.position)<= radius_for_collision(self) + radius_for_collision(object)-3:
            COLLIDE = True
        else:
            COLLIDE = False
        return COLLIDE

class Player(Actor):
    def __init__(self):
        Actor.__init__(self)

        self.sprite = sf.RectangleShape()
        self.sprite.size = (30, 30)
        self.sprite.fill_color = sf.Color.RED
        self.sprite.position = (WIDTH / 2, HEIGHT / 2)

    def draw(self, target, states):
        target.draw(self.sprite, states)

    def got_bus(self, Bus):
        return COUGHT_A_BUS 
        
player = Player()

class Bus(Actor):
    def __init__(self, start_number):
        Actor.__init__(self)
            
        self.sprite = sf.RectangleShape()
        self.sprite.size = (50, 50)
        self.sprite.outline_color = sf.Color.BLUE
        self.sprite.outline_thickness = 2
        self.sprite.position = (342, MAP_HEIGHT)
        
    def draw(self, target, states):
        target.draw(self.sprite)

    def get_number(self):
        return self.start_number

class Creature(Actor):
    def __init__(self):
        Actor.__init__(self)
        self.sprite = sf.RectangleShape()
        self.sprite.size = (5, 5)
        self.sprite.fill_color = sf.Color.BLUE
        self.sprite.position = (random.randrange(0, MAP_WIDTH), random.randrange(0, MAP_HEIGHT))
    def draw(self, target, states):
        target.draw(self.sprite)
    
    
for i in range (0, 20):
        creature = Creature()
        creatures.append(creature)
    
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

background_texture = sf.Texture.from_file("map1.png")
background = sf.Sprite(background_texture)

view = sf.View()
view.reset(sf.Rectangle((0, 0), (WIDTH, HEIGHT)))
window.view = view

overlay = Overlay(player)

timer = sf.Clock()
timer2 = sf.Clock()
# start the game loop
while window.is_open:
    if timer.elapsed_time >= sf.seconds(10):
        PERIOD_OF_TIME += 1
        timer.restart()
        bus = Bus(PERIOD_OF_TIME)
        busses.append(bus)
    for c in creatures:
        if c.is_collide(player):
            print("You were eaten, sorry(((")
            end_game()
    for b in busses:
        if b.is_collide(player):
            print("You were knpcked down by the bus, sorry(((")
            end_game()
    for c in creatures:
        for b in busses:
            if b.is_collide(c):
                creatures.remove(c)
        
    
# process events
    for event in window.events:
        if type(event) is sf.CloseEvent:
            end_game()

    delta = sf.Vector2()
    if sf.Keyboard.is_key_pressed(sf.Keyboard.LEFT) and player.sprite.position.x > 0:
        delta += (-1,0)
    elif sf.Keyboard.is_key_pressed(sf.Keyboard.RIGHT) and player.sprite.position.x + player.sprite.size.x < MAP_WIDTH:
        delta += (1,0)
    if sf.Keyboard.is_key_pressed(sf.Keyboard.UP) and player.sprite.position.y > 0:
        delta += (0,-1)
    elif sf.Keyboard.is_key_pressed(sf.Keyboard.DOWN) and player.sprite.position.y + player.sprite.size.y < MAP_HEIGHT:
        delta += (0,1)
        
    elif sf.Keyboard.is_key_pressed(sf.Keyboard.ESCAPE):
        window.close()

    if sf.Keyboard.is_key_pressed(sf.Keyboard.L_SHIFT):
        player.velocity = 8
    else:
        player.velocity = 1
    
    view_delta = sf.Vector2()
    if player.sprite.position.x > WIDTH / 2 and player.sprite.position.x < MAP_WIDTH - WIDTH / 2:
        view_delta += (delta.x, 0)
    if player.sprite.position.y > HEIGHT / 2 and player.sprite.position.y < MAP_HEIGHT - HEIGHT / 2:
        view_delta += (0, delta.y)

    #print(delta)
    player.move(delta.x, delta.y)
    view.move(view_delta.x, view_delta.y)    

    for bus in busses:
        if bus.sprite.position.y > 0:
            bus.move(0, -1)
        else:
            busses.remove(bus)
        
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
            else:
                print("nope,waiting")
                
        timer2.restart()
           
    window.clear() # clear screen
    window.draw(background)
    window.draw(player) # draw the sprite
    for bus in busses:
        window.draw(bus)
    for creature in creatures:
        window.draw(creature)
    window.draw(overlay)
    window.view = window.default_view
    debug_text = sf.Text("Pos: %s, Period: %i" % (player.sprite.position, PERIOD_OF_TIME))
    debug_text.color = sf.Color.RED
    debug_text.position = (0, HEIGHT - 20)
    debug_text.character_size = 12
    window.draw(debug_text)


    window.display() # update the window

