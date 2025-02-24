import sys
from random import randint, uniform

from direct.showbase.ShowBase import ShowBase
from panda3d.core import TextNode, CardMaker, Fog
from panda3d.core import (
    CollisionNode,
    CollisionRay,
    CollisionHandlerQueue,
    CollisionTraverser
)

base = ShowBase()
base.accept("escape", sys.exit)

fog = Fog('fog')
fog.set_color((0.1,0.1,0.1,1))
fog.set_exp_density(0.004)
base.win.set_clear_color((0.1,0.1,0.1,1))
base.cTrav = CollisionTraverser()
render.set_fog(fog)

base.info = base.a2dTopLeft.attach_new_node(TextNode("info"))
base.info.set_scale(0.04)
base.info.node().text = """\nSimple Racing Example.
\nArrows to drive \nEscape to exit.
"""

base.cam.set_z(6)
cardmaker = CardMaker("quad")
def quad(parent, frame, color=(1,1,1,1), hpr=(0,0,0)):
    cardmaker.set_frame(*frame)
    cardmaker.set_color(color)
    quad = parent.attach_new_node(cardmaker.generate())
    quad.set_two_sided(True)
    quad.set_hpr(hpr)
    return quad

def racetrack():
    racetrack = render.attach_new_node("racetrack")
    w,l,c = 10, 20, render.attach_new_node("road cursor")
    relative = racetrack.get_relative_point
    prev_points = [relative(c, (-w,0,0)), relative(c, ( w,0,0))]
    bend = pitch = 0
    for i in range(1024):
        next_points = [relative(c, ( w,l,0)),relative(c, (-w,l,0))]
        color = ((0.75,0.75,0.75,1),(0.8,0.8,0.8,1))[i%2]
        quad(racetrack, [*prev_points, *next_points], color)
        prev_points = reversed(next_points)
        c.set_pos_hpr(c, (0,l,0),(bend, pitch, 0))
        bend = uniform(-1,1) if not randint(0,32) else bend
        pitch = uniform(-1,1) if not randint(0,32) else pitch
        c.set_hpr(c.get_h(), max(-30, min(c.get_p(), 30)), 0)
    racetrack.flatten_strong()
    racetrack.set_collide_mask(1)
    return racetrack
racetrack()


class Player:
    def __init__(self):
        self.acceleration = 0
        self.path = render.attach_new_node("player")
        back  = quad(self.path, [-1,1,0,1], color=(0.6,0.6,1.0,1), hpr=(0,-40,0))
        front = quad(self.path, [-1,1,0,2], color=(0.3,0.3,0.5,1), hpr=(0, 70,0))
        front.set_y(2.3)

        base.cam.reparent_to(self.path)
        base.cam.set_pos((0,-32,4))
        base.cam.look_at(self.path)

        ray = self.path.attach_new_node(CollisionNode('floor'))
        ray.node().add_solid(CollisionRay((0,0,20),(0,0,-1)))
        ray.node().set_collide_mask(1)
        self.queue = CollisionHandlerQueue()
        base.cTrav.add_collider(ray, self.queue)

        base.task_mgr.add(self.update)

    def update(self, task):
        if len(self.queue.entries) > 0:
            self.queue.sort_entries()
            point = self.queue.entries[0].get_surface_point(render)
            normal= self.queue.entries[0].get_surface_normal(render)
            h = self.path.get_h()
            self.path.set_pos(point)
            self.path.heads_up(self.path, point, normal)
            self.path.set_hpr(h,self.path.get_p(),0)
        else: # Reset game
            self.path.set_pos_hpr(0,0,0,0,0,0)
            self.acceleration = 0
        button = base.mouseWatcherNode.is_button_down
        self.acceleration += button("arrow_up")*base.clock.dt
        self.path.set_h(self.path, (int(button("arrow_left"))-int(button("arrow_right")))*(self.acceleration*0.1))
        self.path.set_y(self.path, self.acceleration)
        self.acceleration *= 0.8**base.clock.dt
        return task.cont

Player()
base.run()
