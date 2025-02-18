from ursina import Ursina, Button, color, Sequence, scene, Wait, Func, camera, application, Tooltip, Entity, Audio, Text


def input(key):
    if key == 'd':
        scene.clear()

    if key == 'space':
        b.text = 'updated text'


if __name__ == '__main__':
    app = Ursina()
    Button.default_color = color.red
    b = Button(
        model='quad',
        scale=.05,
        x=-.5,
        color=color.lime,
        text='text scale\ntest',
        text_size=.5,
        text_color=color.black
    )
    b.text_size = 0.5
    b.on_click = Sequence(Wait(0.5), Func(print, 'aaaaaa'), )

    Button.default_color = color.blue
    b = Button(text='hello world!', icon='sword', scale=.25, text_origin=(-.5, 0), x=.5)
    b.on_click = application.quit  # assign a function to the button.
    b.tooltip = Tooltip('exit')

    par = Entity(parent=camera.ui, scale=.2, y=-.2)
    b = Button(parent=par, text='test', scale_x=1, origin=(-.5, .5))
    b.text = 'new text'
    print(b.text_entity)

    Button(text='sound', scale=.2, position=(-.25, -.2), color=color.pink, highlight_sound='blip_1',
           pressed_sound=Audio('coin_1', autoplay=False))

    Text('Text size\nreference', x=.15)

    app.run()
