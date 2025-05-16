import pyglet

window = pyglet.window.Window(fullscreen=True)

class Timer:
    def __init__(self):

        self.label = pyglet.text.Label(
            '00:00',
            font_size=360,
            x=window.width // 2,
            y=window.height // 2,
            anchor_x='center',
            anchor_y='center'
        )
        self.reset()
        self.time = 0
        self.running = False

    def reset(self):
        self.time = 0
        self.running = False
        self.label.text = '00:00'
        self.label.color = (255, 255, 255, 255)

    def update(self, dt):
        if self.running:
            self.time += dt
            m, s = divmod(self.time, 60)
            self.label.text = f"{round(m):02}:{round(s):02}"
            if m >= 1:
                self.label.color = (180, 0, 0, 255)
            else:
                self.label.color = (0, 180, 0, 255)

        window.draw(dt)

timer = Timer()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.SPACE:
        if timer.running:
            timer.running = False
        else:
            if timer.time > 0:
                timer.reset()
            else:
                timer.running = True
    elif symbol == pyglet.window.key.ESCAPE:
        window.close()

@window.event
def on_draw():
    window.clear()
    timer.label.draw()

if __name__ == '__main__':
    # Set the FPS to 30
    pyglet.clock.schedule_interval(timer.update, 1 / 30.0)

    # Launch the application
    pyglet.app.run(None)
