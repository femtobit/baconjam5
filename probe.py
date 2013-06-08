#!/usr/bin/env python2
import sfml as sf


WIDTH = 640
HEIGHT = 480

MAP_WIDTH = WIDTH * 4
MAP_HEIGHT = HEIGHT * 4

PERIOD_OF_TIME = 0
COUGHT_A_BUS = False
busses = []
# create the main window
window = sf.RenderWindow(sf.VideoMode(WIDTH, HEIGHT), "pySFML Window")

class Actor(sf.Drawable):
    def __init__(self):
        sf.Drawable.__init__(self)

        self.velocity = 1

    def move(self, dx, dy):
        self.sprite.position += (dx, dy) * self.velocity

    def draw(self, target, states):
        target.draw(self.sprite, states)

class Player(Actor):
    def __init__(self):
        Actor.__init__(self)

        self.sprite = sf.RectangleShape()
        self.sprite.size = (30, 30)
        self.sprite.outline_color = sf.Color.RED
        self.sprite.outline_thickness = 5
        self.sprite.position = (WIDTH / 2, HEIGHT / 2)

    def draw(self, target, states):
        target.draw(self.sprite, states)

    def got_bus(self, Bus):
        COUGHT_A_BUS = True
        

player = Player()


class Bus(Actor):
    def __init__(self, start_number):
        Actor.__init__(self)
        self.start_number = PERIOD_OF_TIME

        self.sprite = sf.RectangleShape()
        self.sprite.size = (50, 50)
        self.sprite.outline_color = sf.Color.BLUE
        slef.sprite.outline_thickness = 2
        self.sprite.position = (342, 100)

    def draw(self, target, states):
        target.draw(self.sprite, states)

    def bus_move(self):
        if (self.position.x > 342 and self.position.y > 0):
            self.move(self.position.x, self.position.y)
        else:
            self.dissapear()

    def dessapear(self):
        busses.pop(len(0))

        

background_texture = sf.Texture.from_file("map1.png")
background = sf.Sprite(background_texture)

view = sf.View()
view.reset(sf.Rectangle((0, 0), (WIDTH, HEIGHT)))
window.view = view

timer = sf.Clock()
# start the game loop
while window.is_open:
    if timer.elapsed_time >= sf.seconds(15):
        PERIOD_OF_TIME += 1
        timer.restart()
        print("Period: " + str(PERIOD_OF_TIME))
        bus = Bus(PERIOD_OF_TIME)
        busses.append(bus)
        
# process events
    for event in window.events:
        if type(event) is sf.CloseEvent:
            timer.restart()
            PERIOD_OF_TIME = 0
            busses = []
            window.close()

    if sf.Keyboard.is_key_pressed(sf.Keyboard.LEFT) and player.sprite.position.x > 0:
        player.sprite.position += (-1,0)
    elif sf.Keyboard.is_key_pressed(sf.Keyboard.RIGHT) and player.sprite.position.x < WIDTH:
        player.sprite.position += (1,0)

    if sf.Keyboard.is_key_pressed(sf.Keyboard.UP) and player.sprite.position.y > 0:
        player.sprite.position += (0,-1)
    elif sf.Keyboard.is_key_pressed(sf.Keyboard.DOWN) and player.sprite.position.y < HEIGHT:
        player.sprite.position += (0,1)
        
    elif sf.Keyboard.is_key_pressed(sf.Keyboard.ESCAPE):
        window.close()
    

    window.clear() # clear screen
    window.draw(background)
    window.draw(player) # draw the sprite
    for bus in busses:
        window.draw(bus)
    window.display() # update the window

