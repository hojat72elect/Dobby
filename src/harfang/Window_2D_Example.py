import os

import harfang.bin
import harfangui

if __name__ == '__main__':

    harfang.bin.assetc(os.path.join(harfangui.get_assets_path(), 'assets'), 'assets_compiled', '-quiet')

    harfang.InputInit()
    harfang.WindowSystemInit()

    width, height = 1280, 720
    window = harfang.RenderInit(
        'Harfang GUI - 2D window',
        width,
        height,
        harfang.RF_VSync | harfang.RF_MSAA4X | harfang.RF_MaxAnisotropy
    )

    harfang.AddAssetsFolder("assets_compiled")

    harfangui.HarfangUI.init(["roboto-light.ttf"], [20], width, height)

    keyboard = harfang.Keyboard()
    mouse = harfang.Mouse()

    flag_check_box0 = False

    while not harfang.ReadKeyboard().Key(harfang.K_Escape) and harfang.IsWindowOpen(window):

        _, width, height = harfang.RenderResetToWindow(window, width, height, harfang.RF_VSync | harfang.RF_MSAA4X | harfang.RF_MaxAnisotropy)

        dt = harfang.TickClock()
        keyboard.Update()
        mouse.Update()
        view_id = 0

        if harfangui.HarfangUI.begin_frame(dt, mouse, keyboard, window):

            if harfangui.HarfangUI.begin_window_2D("My window", harfang.Vec2(50, 50), harfang.Vec2(500, 300), 1):

                harfangui.HarfangUI.info_text("info1", "Simple Window2D")

                f_pressed, f_down = harfangui.HarfangUI.button("Button")
                if f_pressed:
                    print("Click btn")

                _, flag_check_box0 = harfangui.HarfangUI.check_box("Check box", flag_check_box0)

                harfangui.HarfangUI.end_window()

            harfangui.HarfangUI.end_frame(view_id)

        harfang.Frame()

        harfang.UpdateWindow(window)

    harfang.RenderShutdown()
    harfang.DestroyWindow(window)
