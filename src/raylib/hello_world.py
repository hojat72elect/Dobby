from pyray import init_window, window_should_close, clear_background, begin_drawing, WHITE, VIOLET, draw_text, \
    end_drawing, close_window

init_window(800, 450, "Hello world")
while not window_should_close():
    begin_drawing()
    clear_background(WHITE)
    draw_text("Hello World", 190, 200, 20, VIOLET)
    end_drawing()

close_window()
