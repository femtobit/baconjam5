import sfml as sf

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

