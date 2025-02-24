import sys
from math import sin
from random import randint, choice

from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath, CardMaker, TextNode, Fog
from panda3d.core import LColor, Vec3
from panda3d.core import (
    CollideMask,
    CollisionNode,
    CollisionSegment,
    CollisionSphere,
    CollisionHandlerQueue,
    CollisionHandlerPusher,
    CollisionTraverser
)



base = ShowBase()
base.accept("escape", sys.exit)
base.disable_mouse()
base.cTrav = CollisionTraverser()


fog = Fog('fog')
fog.set_color((0.1,0.1,0.1,1))
base.win.set_clear_color((0.1,0.1,0.1,1))
render.set_fog(fog)

base.info = base.a2dTopLeft.attach_new_node(TextNode("info"))
base.info.set_scale(0.04)
base.info.node().text = """\nSimple Third Person Platformer Example.
\nAWSD to move \nShift to run \n Space to jump.\nEscape to exit.
"""

cardmaker = CardMaker('quad')
def quad(parent, frame, color=(1,1,1,1), hpr=(0,0,0)):
    cardmaker.set_frame(frame)
    cardmaker.set_color(color)
    quad = parent.attach_new_node(cardmaker.generate())
    quad.set_transparency(True)
    quad.set_hpr(hpr)
    return quad

def box(parent, pos=(0,0,0), hpr=(0,0,0), scale=(1,1,1), color=(1,1,1,1)):
    box = parent.attach_new_node("box")
    w = 0.5
    quad(box,(-w,w,-w,w),hpr=(  0,0,0)).set_y(-w) # Front
    quad(box,(-w,w,-w,w),hpr=(180,0,0)).set_y( w) # Back
    quad(box,(-w,w,-w,w),hpr=(-90,0,0)).set_x(-w) # Left
    quad(box,(-w,w,-w,w),hpr=( 90,0,0)).set_x( w) # Right
    quad(box,(-w,w,-w,w),hpr=( 0,90,0)).set_z(-w) # Top
    quad(box,(-w,w,-w,w),hpr=(0,-90,0)).set_z( w) # Bottom
    box.flatten_strong()
    box.set_color(color, 1)
    box.set_pos_hpr_scale(*pos, *hpr, *scale)
    return box

def ray_queue(parent, ray_from=(0,0,1.5), ray_to=(0,0,0)):
    path = parent.attach_new_node(CollisionNode("ground"))
    ray = CollisionSegment(ray_from,ray_to)
    path.node().add_solid(ray)
    path.node().set_from_collide_mask(1)
    path.node().set_into_collide_mask(CollideMask.all_off())
    queue = CollisionHandlerQueue()
    base.cTrav.add_collider(path, queue)
    return ray, queue


class CameraBird:
    def __init__(self, target):
        self.target = target
        self.dest = self.target.attach_new_node("cam dest")
        self.dest.set_pos(0,-16,16)
        self.ray, self.queue = ray_queue(self.target)
        base.task_mgr.add(self.update)

    def check_wall(self):
        self.ray.point_b = base.camera.get_pos(self.target)+(0,0,2)
        if len(self.queue.entries) > 0:
            self.queue.sort_entries()
            point = self.queue.entries[0].get_surface_point(render)
            max_height = self.target.get_z()+20
            point.z = max_height if point.z > max_height else point.z
            base.camera.set_pos(render, point)

    def update(self, task):
        self.check_wall()
        base.camera.look_at(self.dest)
        if base.camera.get_distance(self.dest) > 0.1:
            base.camera.set_y(base.camera, base.clock.dt*16)
        base.cam.look_at(self.target, (0,0,2))
        base.camera.set_r(render, 0); base.cam.set_r(render, 0)
        return task.cont


class Player:
    def __init__(self, pos):
        self.path = render.attach_new_node("player")
        self.path.set_pos(pos)

        self.model = self.path.attach_new_node("player model")
        self.torso = box(self.model, pos=( 0.0,0.0,1.5), scale=(1.0,0.3,1.0))
        self.head  = box(self.torso, pos=( 0.0,0.0,0.7), scale=(0.3,1.0,0.3))
        self.l_leg = box(self.model, pos=(-0.2,0.0,0.5), scale=(0.2,0.2,1.0))
        self.r_leg = box(self.model, pos=( 0.2,0.0,0.5), scale=(0.2,0.2,1.0))

        pushing = self.path.attach_new_node(CollisionNode("bump"))
        pushing.node().add_solid(CollisionSphere((0,0,1), 1))
        pushing.node().set_from_collide_mask(1)
        pushing.node().set_into_collide_mask(CollideMask.all_off())
        pusher = CollisionHandlerPusher()
        pusher.horizontal = True
        pusher.add_collider(pushing, self.path)
        base.cTrav.add_collider(pushing, pusher)

        self.velocity = Vec3()
        self.ground_ray, self.ground_queue = ray_queue(self.path)
        self.camera_bird = CameraBird(self.model)
        base.task_mgr.add(self.update)

    def leg_waggle(self):
        speed = Vec3(*self.velocity.xy,0).length()*90
        self.l_leg.set_p( sin(base.clock.real_time*20)*speed)
        self.r_leg.set_p(-sin(base.clock.real_time*20)*speed)

    def leg_spread(self):
        self.l_leg.set_p( 45)
        self.r_leg.set_p(-45)

    def update(self, task):
        button = base.mouseWatcherNode.is_button_down
        intention = Vec3(int(button("d"))-int(button("a")),
            int(button("w"))-int(button("s")),0).normalized()
        intention *= 1+(int(button("shift")))
        acceleration = self.path.get_relative_vector(base.cam, intention)
        self.velocity += Vec3(*acceleration.xy,0)*base.clock.dt
        self.velocity.z -= base.clock.dt
        if len(self.ground_queue.entries) > 0: # Is on ground.
            self.ground_queue.sort_entries()
            floor_z = self.ground_queue.entries[0].get_surface_point(render).z
            self.path.set_z(floor_z)
            self.velocity.z = 0
            self.leg_waggle()
            if button("space"):
                self.velocity.z = 0.5
        elif self.velocity.z > 0:
            self.leg_spread()
        self.torso.set_p(self.velocity.length()*32)
        self.model.look_at(self.path, Vec3(*self.velocity.xy, 0))
        self.path.set_pos(self.path, self.velocity)
        self.velocity.x *= 0.01**base.clock.dt
        self.velocity.y *= 0.01**base.clock.dt
        return task.cont


LEVEL = [ # Topdown view of map, numbers are box height, S is spawn
    " 77777 6  6 5 44 ",
    "               4 ",
    "               4 ",
    " 8  911111876  4 ",
    " 8  9     9 5  4 ",
    " 8      22  4  4 ",
    " 7  S   22  3333 ",
    " 6 5 4 322  3333 ",
]

def build_level(size=8, height=4):
    level = render.attach_new_node("level")
    for y, row in enumerate(LEVEL):
        for x, c in enumerate(row):
            color = ((0.2,0.2,0.2,1),(0.6,0.6,0.6,1))[(x+y)%2]
            if c == " ": # Make a floor
                segment = quad(level, (x,x+1,y, y+1), color, (0,-90,0))
            elif c == "S": # Player spawn
                Player(pos=(x*size+(size/2), y*size+(size/2), 0.5))
                segment = quad(level, (x,x+1,y, y+1), color, (0,-90,0))
            else: # Make a block
                box(level, pos=(x+0.5,y+0.5,int(c)/2), scale=(1,1,(int(c))), color=LColor(color)*1.3)
    level.flatten_strong()
    level.set_scale(size, size, height)
    level.set_collide_mask(1)
    return level

build_level()
base.run()
