import sys
from math import floor
from direct.showbase.ShowBase import ShowBase
from panda3d.core import OrthographicLens, TextNode, CardMaker, Vec3


base = ShowBase()
base.accept("escape", sys.exit)
base.win.set_clear_color((0.1,0.1,0.1,1))

lens = OrthographicLens()
lens.set_film_size(32,20)
base.cam.node().set_lens(lens)

base.info = base.a2dTopLeft.attach_new_node(TextNode("info"))
base.info.set_scale(0.04)
base.info.node().text = """\nSimple Sidescroller Example.
\nArrows to move. \nSpace to jump.\nEscape to exit.
"""

cardmaker = CardMaker('quad')
def quad(parent, frame=(0,1,0,1), color=(0.8,0.8,0.8,1)):
    cardmaker.set_frame(frame)
    cardmaker.set_color(color)
    quad = parent.attach_new_node(cardmaker.generate())
    quad.set_two_sided(True)
    return quad

level = [
    "##################################################",
    "#                                                #",
    "#                 e                              #",
    "#           #########      e                     #",
    "#               #       #######   ##             #",
    "#         ##    #    ---      #    ##            #",
    "#               ##           ##    ###           #",
    "# s     ##      #   ----      #    ####--   --#  #",
    "#               #           ###    ####       # f#",
    "#   ####  e    ####        ####    ####^^^^^^^####",
    "###############################^^^^###############"
]


class Player:
    def __init__(self, pos):
        self.spawn_pos = pos
        self.path = render.attach_new_node("player")
        self.path.set_pos(pos)
        self.width = 0.18
        quad(self.path, frame=(-self.width,self.width,-0.5,0.5), color=(0,1,1,1))
        self.velocity = Vec3()
        self.jump = 8
        base.task_mgr.add(self.update)

    def update(self, task):
        button = base.mouseWatcherNode.is_button_down
        self.velocity += (int(button("arrow_right"))-int(button("arrow_left")),0,-1)
        slide = self.width if self.velocity.x > 0 else -self.width
        h_tile, v_tile = int(self.path.get_x()), int(self.path.get_z()+0.5)
        next_h_tile = floor(self.path.get_x()+slide+(self.velocity.x*base.clock.dt))
        next_v_tile = floor(self.path.get_z()+ 0.5 +(self.velocity.z*base.clock.dt))
        if self.velocity.z < -8:
            self.jump = 0
        if level[next_v_tile][h_tile] in "#-": # On floor
            self.jump = 10
            self.velocity.z = 0
            self.path.set_z(next_v_tile+0.5)
        elif level[next_v_tile+1][h_tile] == "#": # Bump ceiling
            self.velocity.z = 0
            self.path.set_z(next_v_tile-0.5)
        if level[v_tile+1][h_tile] == "#": # Touch ceiling
            self.jump = 0
        if level[v_tile][next_h_tile] == "#": # Bump wall
            self.velocity.x = 0
        if self.jump: # Jumping
            if button("space"):
                self.jump -= 1
                self.velocity.z += self.jump/2.4
            elif self.jump < 10:
                self.jump = 0

        # Hitting special tiles
        touching_tile = level[next_v_tile+1][next_h_tile]
        if touching_tile == "^": # Death by spikes.
            self.path.set_pos(self.spawn_pos)
        elif touching_tile == "f": # Win.
            print("You won, congratulations!"); sys.exit()
        # Apply velocity.
        self.path.set_pos(self.path, self.velocity*base.clock.dt)
        self.velocity.x *= 0.001**base.clock.dt
        base.cam.set_pos(self.path.get_pos()+(0,-1,0))

        return task.cont

# Build level geometry
level.reverse() # Iterate over level upside down (Z+ is up in Panda3D)
for y, row in enumerate(level):
    level_geometry = render.attach_new_node("level")
    for x, t in enumerate(row):
        if t == "#":
            quad(level_geometry, (x,x+1,y,y-1))
        elif t == "-":
            quad(level_geometry, (x,x+1,y,y-0.5), color=(0.2,0.2,0.2, 1))
        elif t == "^":
            quad(level_geometry, (x+0.2,x+0.3,y+0.0,y-1), color=(1,0.2,0.2,1))
            quad(level_geometry, (x+0.5,x+0.6,y+0.5,y-1), color=(1,0.2,0.2,1))
            quad(level_geometry, (x+0.8,x+0.9,y+0.2,y-1), color=(1,0.2,0.2,1))
        elif t == "f":
            quad(level_geometry, (x,x+1,y,y-1), color=(1,0,1,1))
        elif t == "s":
            Player((x+0.5,0,y+0.5))
    level_geometry.flatten_strong()

base.run()
