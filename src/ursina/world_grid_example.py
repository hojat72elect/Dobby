import ursina

if __name__ == '__main__':
    """
    Creates a 3D grid pattern 
    """

    app = ursina.Ursina()

    r = 8
    for i in range(1, r):
        t = i / r
        s = 4 * i
        print(s)
        grid = ursina.Entity(model=ursina.Grid(s, s), scale=s, color=ursina.color.hsv(0, 0, .8, ursina.lerp(.8, 0, t)), rotation_x=90, y=i / 1000)
        subgrid = ursina.duplicate(grid)
        subgrid.model = ursina.Grid(s * 4, s * 4)
        subgrid.color = ursina.color.hsv(0, 0, .4, ursina.lerp(.8, 0, t))
        ursina.EditorCamera() # creates a controllable camera for seeing the grid and going up and down , and zoom

    app.run()
