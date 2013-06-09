import sfml as sf

class Overlay(sf.Drawable):
    def __init__(self, actor, dark=False):
        self.actor = actor

        if dark:
            self.texture = sf.Texture.from_file("overlay-dark.png")
        else:
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
        for i in range(0, self.max_points):
            shape = sf.RectangleShape((width, self.rect.height))
            shape.outline_color = self.color
            shape.outline_thickness = 1
            if i < self.points:
                shape.fill_color = self.color
            else:
                shape.fill_color = sf.Color.TRANSPARENT
            shape.position = (self.rect.position.x + i * dx,
                                    self.rect.position.y)
            target.draw(shape, states)

