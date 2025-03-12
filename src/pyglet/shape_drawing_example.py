import pyglet
import math


class ShapesDrawer(pyglet.window.Window):

    def __init__(self, width, height):
        super().__init__(width, height, "Shapes Example")
        self.time = 0
        self.batch = pyglet.graphics.Batch()

        self.circle = pyglet.shapes.Circle(360, 240, 75, color=(255, 225, 255, 127), batch=self.batch)

        # A rectangle with center as anchor
        self.square = pyglet.shapes.BorderedRectangle(360, 240, 100, 100, border=5, color=(55, 55, 255),
                                                      border_color=(25, 25, 25), batch=self.batch)
        self.square.anchor_position = 50, 50

        # A large and transparent rectangle
        self.rectangle = pyglet.shapes.Rectangle(100, 190, 500, 100, color=(255, 22, 20, 64), batch=self.batch)

        self.line = pyglet.shapes.Line(0, 0, 0, 480, thickness=4, color=(200, 20, 20), batch=self.batch)

        self.triangle = pyglet.shapes.Triangle(10, 10, 190, 10, 100, 150, color=(55, 255, 255, 175), batch=self.batch)

        septagon_step = math.pi * 2 / 7
        self.fading_septagon = pyglet.shapes.Polygon(
            *[[50 + 40 * math.sin(i * septagon_step), 200 + 40 * math.cos(i * septagon_step)] for i in range(7)],
            batch=self.batch)

        self.arc = pyglet.shapes.Arc(50, 300, radius=40, segments=25, angle=270.0, color=(255, 255, 255),
                                     batch=self.batch)

        self.star = pyglet.shapes.Star(600, 375, 50, 30, 5, color=(255, 255, 0), batch=self.batch)

        self.ellipse = pyglet.shapes.Ellipse(650, 150, a=50, b=30, color=(55, 255, 55), batch=self.batch)

        self.sector = pyglet.shapes.Sector(125, 400, 60, angle=0.45 * 360, color=(55, 255, 55), batch=self.batch)

        self.polygon = pyglet.shapes.Polygon([400, 100], [500, 10], [600, 100], [550, 175], [450, 150],
                                             batch=self.batch)

        self.box = pyglet.shapes.Box(60, 40, 200, 100, thickness=2, color=(244, 55, 55), batch=self.batch)

        coordinates = [[450, 400], [475, 450], [525, 450], [550, 400]]
        self.multiLine = pyglet.shapes.MultiLine(*coordinates, closed=True, batch=self.batch)

    def on_draw(self):
        """Clear the screen and draw shapes"""
        self.clear()
        self.batch.draw()

    def update(self, delta_time):
        """Animate the shapes"""
        self.time += delta_time
        self.square.rotation = self.time * 15
        self.rectangle.y = 200 + math.sin(self.time) * 190
        self.circle.radius = 75 + math.sin(self.time * 1.17) * 25
        self.triangle.rotation = self.time * 15

        self.line.x = 360 + math.sin(self.time * 0.81) * 360
        self.line.x2 = 360 + math.sin(self.time * 1.34) * 360

        self.arc.rotation = self.time * 30

        self.fading_septagon.opacity = int(255 * (0.5 + (0.5 * math.cos(self.time))))

        self.star.rotation = self.time * 50
        self.polygon.rotation = self.time * 45

        self.ellipse.b = abs(math.sin(self.time) * 100)
        self.sector.angle = (self.time * 30) % 360.0

        self.multiLine.rotation = self.time * -15

        self.multiLine.rotation = self.time * -15


if __name__ == '__main__':
    demo_game = ShapesDrawer(720, 480)
    pyglet.clock.schedule_interval(demo_game.update, 1 / 60)
    pyglet.app.run()
