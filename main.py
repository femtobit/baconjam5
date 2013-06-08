#!/usr/bin/env python2
import sfml as sf


WIDTH = 640
HEIGHT = 480

MAP_WIDTH = 960
MAP_HEIGHT = 1280

PERIOD_OF_TIME = 0
# create the main window
window = sf.RenderWindow(sf.VideoMode(WIDTH, HEIGHT), "pySFML Window")

class Actor(sf.Drawable):
    def __init__(self):
        sf.Drawable.__init__(self)

        self.velocity = 1

    def move(self, delta):
        self.sprite.position += delta * self.velocity

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

class Bus(Actor):
    def __init__(self, start_number):
        Actor.__init__(self)
        self.start_number = 0

        self.sprite = sf.RectangleShape()
        self.sprite.size = (50, 50)
        self.sprite.outline_color = sf.Color.BLUE
        self.sprite.outline_thickness = 2
        self.sprite.position = (342, 100)

    def draw(self, target, states):
        target.draw(self.sprite, states)

    def get_number(self):
        self.start_number = PERIOD_OF_TIME

busses = []

player = Player()

background_texture = sf.Texture.from_file("map1.png")
background = sf.Sprite(background_texture)

view = sf.View()
view.reset(sf.Rectangle((0, 0), (WIDTH, HEIGHT)))

timer = sf.Clock()
# start the game loop
while window.is_open:

    if timer.elapsed_time >= sf.seconds(15):
        PERIOD_OF_TIME += 1
        timer.restart()
        print("Period: " + str(PERIOD_OF_TIME))

        bus = Bus(PERIOD_OF_TIME)

# process events
    for event in window.events:
        if type(event) is sf.CloseEvent:
            timer.restart()
            PERIOD_OF_TIME = 0
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
    player.move(delta)
    view.move(view_delta.x * player.velocity, view_delta.y * player.velocity)
    
    window.view = view

    window.clear() # clear screen
    window.draw(background)
    window.draw(player) # draw the sprite
    for bus in busses:
        window.draw(bus)

    window.view = window.default_view
    debug_text = sf.Text("Pos: %s, Period: %i" % (player.sprite.position, PERIOD_OF_TIME))
    debug_text.color = sf.Color.RED
    debug_text.position = (0, HEIGHT - 20)
    debug_text.character_size = 12
    window.draw(debug_text)

    window.display() # update the window

