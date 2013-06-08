#!/usr/bin/env python2
import sfml as sf


WIDTH = 640
HEIGHT = 480

MAP_WIDTH = 960
MAP_HEIGHT = 1280

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
        self.sprite.fill_color = sf.Color.RED
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
        self.sprite.outline_thickness = 2
        self.sprite.position = (342, 100)

    def draw(self, target, states):
        target.draw(self.sprite, states)

    def bus_move(self):
        if (self.position.x > 342 and self.position.y > 0):
            self.move(self.position.x, self.position.y)
        else:
            self.dissapear()

    def get_number(self):
        return self.start_number

    def dessapear(self):
        busses.pop(len(0))

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
# start the game loop
while window.is_open:
    if timer.elapsed_time >= sf.seconds(15):
        PERIOD_OF_TIME += 1
        timer.restart()
        print("Period: " + str(PERIOD_OF_TIME))
        bus = Bus(PERIOD_OF_TIME)
        print("Bus's numbers are: " + str(bus.get_number()))
        busses.append(bus)
        
# process events
    for event in window.events:
        if type(event) is sf.CloseEvent:
            timer.restart()
            PERIOD_OF_TIME = 0
            busses = []
            window.close()

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
        player.velocity = 2
    
    view_delta = sf.Vector2()
    if player.sprite.position.x > WIDTH / 2 and player.sprite.position.x < MAP_WIDTH - WIDTH / 2:
        view_delta += (delta.x, 0)
    if player.sprite.position.y > HEIGHT / 2 and player.sprite.position.y < MAP_HEIGHT - HEIGHT / 2:
        view_delta += (0, delta.y)

    print(delta)
    player.move(delta.x, delta.y)
    view.move(view_delta.x, view_delta.y)    

    window.clear() # clear screen
    window.draw(background)
    window.draw(player) # draw the sprite
    for bus in busses:
        window.draw(bus)
    window.draw(overlay)

    window.view = window.default_view
    debug_text = sf.Text("Pos: %s, Period: %i" % (player.sprite.position, PERIOD_OF_TIME))
    debug_text.color = sf.Color.RED
    debug_text.position = (0, HEIGHT - 20)
    debug_text.character_size = 12
    window.draw(debug_text)


    window.display() # update the window

