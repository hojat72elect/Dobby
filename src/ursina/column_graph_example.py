from ursina import *
import random

if __name__ == '__main__':

    app = Ursina()

    color.text_color = color.dark_text

    names = ['Amy', 'Ruby', 'Tara', 'Ann', 'Samantha', 'Gary', 'Lee', 'Frank', 'Joe', 'Thomas']

    random.seed(0)
    data = dict()
    for name in names:
        data[name] = random.randint(0, 100)

    sliders = list()

    for i, (name, value) in enumerate(data.items()):

        # In fact, each column is just an Ursina Button
        _column = Button(
            parent=scene,
            name=name,
            model='cube',
            x=i - (len(names) / 2),
            scale=(.5, value / 50, .5),
            color=color.hsv(30 * i, 1, .7),
            origin_y=-.5,
            text=name,
            tooltip=Tooltip('00', color=color.light_text)  # to ensure uniform width of columns
        )
        _column.tooltip.text = str(value)
        _column.text_entity.scale *= .4
        _column.text_entity.world_y = _column.world_y - .2
        _column.text_entity.z = -.5
        _column.text_entity.world_parent = scene
        _column.text_entity.color = _column.color.tint(-.5)

        _thin_slider = ThinSlider(
            text=name,
            min=0,
            max=100,
            default=value,
            x=-.65,
            y=(-i * .04 * .75) - .15,
            step=1,
            dynamic=True
        )
        _thin_slider.scale *= .75
        sliders.append(_thin_slider)


        def on_slider_changed(slider=_thin_slider, column=_column):
            column.scale_y = slider.value / 50
            column.tooltip.text = str(slider.value)


        _thin_slider.on_value_changed = on_slider_changed

    randomize_button = Button(
        position=(-.66, -.45),
        origin=(-.5, .5),
        color=color.dark_gray,
        text='<white>Randomize!',
        scale=(.25, .05)
    )
    randomize_button.scale *= .75


    def randomize():
        for slider in sliders:
            slider.value = random.randint(0, 100)
            slider.on_value_changed()


    randomize_button.on_click = randomize

    window.color = color.light_gray.tint(.1)
    window.fps_counter.enabled = False
    window.exit_button.visible = False
    camera.orthographic = True
    camera.fov = 8
    EditorCamera()

    app.run()
