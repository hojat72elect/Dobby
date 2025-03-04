import pyray

pyray.init_window(800, 450, "Hello Pyray")
pyray.set_target_fps(60)

camera = pyray.Camera3D([18.0, 16.0, 18.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0], 45.0, 0)

while not pyray.window_should_close():
    pyray.update_camera(camera, pyray.CameraMode.CAMERA_ORBITAL)
    pyray.begin_drawing()
    pyray.clear_background(pyray.RAYWHITE)
    pyray.begin_mode_3d(camera)
    pyray.draw_grid(20, 1.0)
    pyray.end_mode_3d()
    pyray.draw_text("Hello world", 190, 200, 20, pyray.VIOLET)
    pyray.end_drawing()
pyray.close_window()
