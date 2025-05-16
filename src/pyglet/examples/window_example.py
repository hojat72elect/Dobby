import pyglet

if __name__ == '__main__':
    window = pyglet.window.Window(width=1_920, height=1_080, caption="Hello Pyglet!")
    window.set_location(1920 // 2, 1080 // 2)
    pyglet.app.run()
