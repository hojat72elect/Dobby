import pyray


if __name__ == '__main__':

    pyray.init_window(800, 450, "Hello World Example")
    while not pyray.window_should_close():
        pyray.begin_drawing()
        pyray.clear_background(pyray.WHITE)
        pyray.draw_text("Hello World\nMy name is Hojat and I enjoy coding in RayLib.", 190, 200, 20, pyray.VIOLET)
        pyray.end_drawing()

    pyray.close_window()