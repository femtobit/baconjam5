#!/usr/bin/env python2
import sfml as sf

WIDTH = 640
HEIGHT = 480

# create the main window
window = sf.RenderWindow(sf.VideoMode(WIDTH, HEIGHT), "pySFML Window")

class Actor(sf.Drawable):
    def __init__(self):
        sf.Drawable.__init__(self)
        
        self.sprite = sf.RectangleShape()
        self.sprite.size = (30, 30)
        self.sprite.outline_color = sf.Color.RED
        self.sprite.outline_thickness = 5
        self.sprite.position = (WIDTH / 2, HEIGHT / 2)

    def draw(self, target, states):
        target.draw(self.sprite, states)

player = Actor()

# start the game loop
while window.is_open:
# process events
    for event in window.events:
        if type(event) is sf.CloseEvent:
            window.close()

    if sf.Keyboard.is_key_pressed(sf.Keyboard.LEFT):
        player.sprite.position += (-1,0)
    elif sf.Keyboard.is_key_pressed(sf.Keyboard.RIGHT):
        player.sprite.position += (1,0)

    if sf.Keyboard.is_key_pressed(sf.Keyboard.UP):
        player.sprite.position += (0,-1)
    elif sf.Keyboard.is_key_pressed(sf.Keyboard.DOWN):
        player.sprite.position += (0,1)
        
    elif sf.Keyboard.is_key_pressed(sf.Keyboard.ESCAPE):
        window.close()
            
    window.clear() # clear screen
    window.draw(player) # draw the sprite
    window.display() # update the window

