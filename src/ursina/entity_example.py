from ursina import Ursina, Entity, color, held_keys


class Player(Entity):
    """
    A simple example of class that inherits Entity class.
    """
    def __init__(self, **kwargs):
        super().__init__()
        self.model = 'cube'
        self.color = color.red
        self.scale_y=2

        for key, value in kwargs.items():
            setattr(self, key, value)

    def input(self, key):
        if key == 'space':
            self.animate_x(2, duration=1)

    def update(self):
        self.x += held_keys['d'] * time.dt * 10
        self.x -= held_keys['a'] * time.dt * 10


if __name__ == '__main__':
    app = Ursina()
    _entity = Entity(model = 'quad', color = color.orange, position = (0,0,1), scale=1.5, rotation=(0,0,45), texture = 'brick')
    player = Player(x=-1)

