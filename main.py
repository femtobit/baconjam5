import sfml as sf

WIDTH = 640
HEIGHT = 480

# create the main window
window = sf.RenderWindow(sf.VideoMode(WIDTH, HEIGHT), "pySFML Window")

try:
   # load a sprite to display
    sprite = sf.RectangleShape()
    sprite.size = (30, 30)
    sprite.outline_color = sf.Color.RED
    sprite.outline_thickness = 5
    sprite.position = (WIDTH / 2, HEIGHT / 2)

# load music to play
#   music = sf.Music.from_file("nice_music.ogg")

except IOError:
    print("Error")
    exit(1)

# play the music

# start the game loop
while window.is_open:
# process events
    for event in window.events:
        if type(event) is sf.CloseEvent:
            window.close()

    if sf.Keyboard.is_key_pressed(sf.Keyboard.LEFT):
        sprite.position += (-1,0)
    elif sf.Keyboard.is_key_pressed(sf.Keyboard.RIGHT):
        sprite.position += (1,0)

    if sf.Keyboard.is_key_pressed(sf.Keyboard.UP):
        sprite.position += (0,-1)
    elif sf.Keyboard.is_key_pressed(sf.Keyboard.DOWN):
        sprite.position += (0,1)
        
    elif sf.Keyboard.is_key_pressed(sf.Keyboard.ESCAPE):
        window.close()
            
    window.clear() # clear screen
    window.draw(sprite) # draw the sprite
    window.display() # update the window

