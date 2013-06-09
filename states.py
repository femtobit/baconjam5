import sfml as sf

from actors import *
from drawables import *
from constants import *

class State:
    def __init__(self, window):
        self.has_ended = False
        self.window = window

class IntroState(State):
    def __init__(self, window):
        State.__init__(self, window)
        self.sprite = sf.Sprite(sf.Texture.from_file("greeting.png"))
        self.view = sf.View()
        self.view.reset(sf.Rectangle((0, 0), (WIDTH, HEIGHT)))

    def step(self, dt):
        for event in self.window.events:
            if type(event) == sf.KeyEvent and event.pressed:
                self.has_ended = True
                self.next_state = GameState

    def draw(self):
        self.window.view = self.view
        self.window.draw(self.sprite)

class GameOverState(State):
    def __init__(self, window):
        State.__init__(self, window)
        self.sprite = sf.Sprite(sf.Texture.from_file("endtext.png"))
        self.view = sf.View()
        self.view.reset(sf.Rectangle((0, 0), (WIDTH, HEIGHT)))

    def step(self, dt):
        for event in self.window.events:
            if type(event) == sf.KeyEvent and event.pressed:
                if event.code == sf.Keyboard.ESCAPE:
                    self.has_ended = True
                    self.next_state = None
                elif event.code == sf.Keyboard.RETURN:
                    self.has_ended = True
                    self.next_state = GameState

    def draw(self):
        self.window.view = self.view
        self.window.draw(self.sprite)

class GameState(State):
    def __init__(self, window):
        State.__init__(self, window)

        self.debug = []

        self.busses = []
        self.creatures = []
        self.lives = []

        self.player = Player(WIDTH / 2, HEIGHT / 2)

        for i in range (0, NUMBER_OF_GRUES):
            while True:
                point = (random.randrange(0, MAP_WIDTH),
                        random.randrange(0, MAP_HEIGHT))
                if dist(point, self.player.position) > 250:
                    break
            creature = Grue(*point)
            print("New Grue at (%s)" % (creature.position))
            self.creatures.append(creature)

        for i in range(0, 5):
            heal = Lives(random.randrange(0, MAP_WIDTH),
                    random.randrange(0, MAP_HEIGHT))
            self.lives.append(heal)

        self.background = sf.Sprite(sf.Texture.from_file("map2.png"))

        self.view = sf.View()
        self.view.reset(sf.Rectangle((0, 0), (WIDTH, HEIGHT)))
        self.window.view = self.view

        self.overlay = Overlay(self.player)

        self.life_point_display = PointDisplay(sf.Rectangle((WIDTH - 100, 10), (100, 10)),
                self.player.health, sf.Color.RED)

        self.boss_time = sf.Clock()
        self.run_timer = sf.Clock()

        self.is_running = False

    def step(self, dt):
        self.debug = []

        self.debug.append("(dt=%i/16 ms)" % dt) 

        if self.boss_time.elapsed_time == sf.seconds(30):
            boss = Boss(random.randrange(0, MAP_WIDTH), random.randrange(0, MAP_HEIGHT))
            self.creatures.append(boss)
        if self.boss_time.elapsed_time == sf.seconds(45):
            self.creatures.remove(boss)
            self.boss_time.restart()

        for c in self.creatures:
            if c.collides_with(self.player):
                self.creatures.remove(c)
                c.bite(self.player)
                if self.player.health <= 0:
                    self.has_ended = True
                    self.next_state = GameOverState

        for h in self.lives:
            if h.collides_with(self.player):
                self.lives.remove(h)
                h.heal(self.player)

        for event in self.window.events:
            if type(event) is sf.CloseEvent:
                self.window.close()
            elif type(event) is sf.KeyEvent and event.code == sf.Keyboard.L_SHIFT:
                if event.pressed and not self.is_running:
                    self.is_running = True
                    self.run_timer.restart()
                elif event.released and self.is_running:
                    self.is_running = False
                    self.player.stamina -= 1

        if self.is_running and self.run_timer.elapsed_time >= sf.seconds(1):
            self.is_running = False
            self.player.stamina -= 1

        if self.is_running:
            self.debug.append("sprint (" + str(self.run_timer.elapsed_time.seconds) + ")")

        if self.player.stamina > 0:
            delta = self.player_movement_vector(self.player)
        else:
            delta = sf.Vector2()

        view_delta = sf.Vector2()
        if self.player.position.x > WIDTH / 2 \
                and self.player.position.x < MAP_WIDTH - WIDTH / 2:
            view_delta += (delta.x, 0)
        if self.player.position.y > HEIGHT / 2 \
                and self.player.position.y < MAP_HEIGHT - HEIGHT / 2:
            view_delta += (0, delta.y)

        self.debug.append("dr: %s" % delta)
        self.player.move(delta, dt)

        sf.Listener.set_position((self.player.position.x,
            self.player.position.y, 0))
        self.view.move(view_delta.x * dt, view_delta.y * dt)

        self.debug.append("Pos: %s" %
                self.player.position)

        #Monster movement
        for creature in self.creatures:
            creature.step(self.player, dt)
            creature.sound_tick()

        self.life_point_display.points = self.player.health

    def draw(self):
        self.window.view = self.view

        self.window.draw(self.background)
        self.window.draw(self.player)
        for creature in self.creatures:
            self.window.draw(creature)
        for heal in self.lives:
            self.window.draw(heal)
        self.window.draw(self.overlay)

        self.window.view = self.window.default_view

        debug_text = sf.Text(", ".join(self.debug))
        debug_text.color = sf.Color.RED
        debug_text.position = (0, HEIGHT - 20)
        debug_text.character_size = 12

        self.window.draw(debug_text)
        self.window.draw(self.life_point_display)

    def player_movement_vector(self, player):
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

        if self.is_running:
            delta *= 8
        else:
            delta *= 2

        return delta

