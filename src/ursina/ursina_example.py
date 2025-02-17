from ursina import Ursina


def input(key):
    print(key)


if __name__ == '__main__':
    app = Ursina(development_mode=True, use_ingame_console=True)
    app.run()
