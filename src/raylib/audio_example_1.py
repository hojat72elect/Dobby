import dataclasses
import pyray
import raylib

@dataclasses.dataclass
class ColoredCircle:
    """
    Each one of the colored circles we make in the background.
    """
    position: pyray.Vector2
    radius: float
    alpha: float
    speed: float
    color: pyray.Color

if __name__ == '__main__':
    MAX_CIRCLES = 64

    screenWidth = 800
    screenHeight = 450

    raylib.SetConfigFlags(raylib.FLAG_MSAA_4X_HINT)
    raylib.InitWindow(screenWidth, screenHeight, b"raylib [audio] example - module playing (streaming)")

    raylib.InitAudioDevice()

    # All the different colors that our circles can have
    colors = [
        pyray.ORANGE,
        pyray.RED,
        pyray.GOLD,
        pyray.LIME,
        pyray.BLUE,
        pyray.VIOLET,
        pyray.BROWN,
        pyray.LIGHTGRAY,
        pyray.PINK,
        pyray.YELLOW,
        pyray.GREEN,
        pyray.SKYBLUE,
        pyray.PURPLE,
        pyray.BEIGE
    ]

    circles = []

    for i in range(MAX_CIRCLES):
        _circle_radius = raylib.GetRandomValue(10, 40)
        _circle_position = pyray.Vector2(
            float(raylib.GetRandomValue(_circle_radius, int(screenWidth) - _circle_radius)),
            float(raylib.GetRandomValue(_circle_radius, int(screenHeight) - _circle_radius))
        )
        _circle = ColoredCircle(
            alpha=0.0,
            radius=float(_circle_radius),
            position=_circle_position,
            speed=float(raylib.GetRandomValue(1, 100)) / 2000.0,
            color=colors[raylib.GetRandomValue(0, 13)]
        )
        circles.append(_circle)

    music = raylib.LoadMusicStream(b"resources/country.mp3")
    music.looping = False
    pitch = 1.0

    raylib.PlayMusicStream(music)
    timePlayed = 0.0
    pause = False

    raylib.SetTargetFPS(60)

    while not raylib.WindowShouldClose():

        # Update music buffer with new stream data
        raylib.UpdateMusicStream(music)

        # Restart music playing if space is pressed
        if raylib.IsKeyPressed(raylib.KEY_SPACE):
            raylib.StopMusicStream(music)
            raylib.PlayMusicStream(music)
            pause = False

        # Pause/Resume music playing (by pressing P)
        if raylib.IsKeyPressed(raylib.KEY_P):
            pause = not pause
            if pause:
                raylib.PauseMusicStream(music)
            else:
                raylib.ResumeMusicStream(music)

        # Change the speed of the music playback
        if raylib.IsKeyDown(raylib.KEY_DOWN):
            pitch -= 0.01
        elif raylib.IsKeyDown(raylib.KEY_UP):
            pitch += 0.01

        raylib.SetMusicPitch(music, pitch)

        # Get timePlayed scaled to the visual bar's dimensions
        timePlayed = (raylib.GetMusicTimePlayed(music) / raylib.GetMusicTimeLength(music)) * (screenWidth - 40)

        # Color circles animation
        for i in range(MAX_CIRCLES):
            if pause:
                break

            circles[i].alpha += circles[i].speed
            circles[i].radius += circles[i].speed * 10.0

            if circles[i].alpha > 1.0:
                circles[i].speed *= -1

            if circles[i].alpha <= 0.0:
                circles[i].alpha = 0.0
                _circle_radius = raylib.GetRandomValue(10, 40)
                _circle_position = pyray.Vector2(
                    float(raylib.GetRandomValue(_circle_radius, int(screenWidth) - _circle_radius)),
                    float(raylib.GetRandomValue(_circle_radius, int(screenHeight) - _circle_radius))
                )
                circles[i].position = _circle_position
                circles[i].radius = float(_circle_radius)
                circles[i].speed = float(raylib.GetRandomValue(1, 100)) / 2000.0
                circles[i].color = colors[raylib.GetRandomValue(0, 13)]

        pyray.begin_drawing()
        pyray.clear_background(pyray.RAYWHITE)

        for i in range(MAX_CIRCLES):
            pyray.draw_circle_v(circles[i].position, circles[i].radius, pyray.fade(circles[i].color, circles[i].alpha))

        # Draw time bar
        pyray.draw_rectangle(20, screenHeight - 20 - 12, screenWidth - 40, 12, pyray.LIGHTGRAY)
        pyray.draw_rectangle(20, screenHeight - 20 - 12, int(timePlayed), 12, pyray.MAROON)
        pyray.draw_rectangle_lines(20, screenHeight - 20 - 12, screenWidth - 40, 12, pyray.GRAY)

        # Draw help instructions
        pyray.draw_rectangle(20, 20, 425, 145, pyray.RAYWHITE)
        pyray.draw_rectangle_lines(20, 20, 425, 145, pyray.GRAY)
        pyray.draw_text("PRESS SPACE TO RESTART MUSIC", 40, 40, 20, pyray.BLACK)
        pyray.draw_text("PRESS P TO PAUSE/RESUME", 40, 70, 20, pyray.BLACK)
        pyray.draw_text("PRESS UP/DOWN TO CHANGE SPEED", 40, 100, 20, pyray.BLACK)
        pyray.draw_text(f"SPEED: {pitch}", 40, 130, 20, pyray.MAROON)

        pyray.end_drawing()

    raylib.UnloadMusicStream(music)  # Unload music stream buffers
    raylib.CloseAudioDevice()  # Close audio device (music streaming is automatically stopped)
    raylib.CloseWindow()  # Close window and OpenGL context
