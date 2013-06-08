#!/usr/bin/env python2
import sfml as sf


WIDTH = 640
HEIGHT = 480
PERIOD_OF_TIME = 0
# create the main window
window = sf.RenderWindow(sf.VideoMode(WIDTH, HEIGHT), "pySFML Window")

class Actor(sf.Drawable):
    def __init__(self):
        sf.Drawable.__init__(self)

        self.velocity = 8

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
player = Player()

background = sf.RectangleShape()
background.size = (WIDTH, HEIGHT)
background.fill_color = sf.Color.GREEN

class Bus():
    def __init__(self):
        pass

    def get_number(self):
        pass



# start the game loop
while window.is_open:
timer = sf.Clock()
print timer
if timer == 5000:
    PERIOD_OF_TIME += 1 
    timer.restart()
# process events
    for event in window.events:
        if type(event) is sf.CloseEvent:
            timer.restart()
            PERIOD_OF_TIME = 0
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
    window.display() # update the window

