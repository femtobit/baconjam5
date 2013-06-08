import sfml as sf

class Actor(sf.Drawable):
    def __init__(self):
        sf.Drawable.__init__(self)

        self.sprite = sf.CircleShape()

    def move(self, dx, dy):
        self.position += (dx, dy)

    def draw(self, target, states):
        target.draw(self.sprite, states)

    @property
    def position(self):
        return self.sprite.position

    @position.setter
    def position(self, pos):
        self.sprite.position = pos

class Player(Actor):
    def __init__(self, x, y):
        Actor.__init__(self)

        self.sprite = sf.RectangleShape()
        self.sprite.size = (30, 30)
        self.sprite.fill_color = sf.Color.RED
        self.position = (x, y)

    def draw(self, target, states):
        target.draw(self.sprite, states)

class Bus(Actor):
    def __init__(self, start_number):
        Actor.__init__(self)

        self.start_number = start_number

        self.sprite = sf.RectangleShape()
        self.sprite.size = (50, 50)
        self.sprite.outline_color = sf.Color.BLUE
        self.sprite.outline_thickness = 2
        self.sprite.position = (342, 100)

    def draw(self, target, states):
        target.draw(self.sprite, states)

    def move(self):
        if (self.position.x > 342 and self.position.y > 0):
            super(self, Bus).move(0, 1)
        else:
            self.disappear()

    def get_number(self):
        return self.start_number

    def disappear(self):
        del self

def Monster(Actor):
    def __init__(self):
        self.speed = 1

    def hunt_player(self, player):
        player_direction = player.position - self.position
        delta = (player_direction / vector.norm(player_direction)) * self.speed

        self.move(delta.x, delta.y)

def Grue(Monster):
    def __init__(self, x, y):
        Monster.__init__(self)

        self.sprite = sf.CircleShape()
        self.sprite.size = (30,30)
        self.sprite.color = sf.Color.GREEN
        self.position = (x,y)

        self.speed = 1.5
