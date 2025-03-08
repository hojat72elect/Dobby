import math

from . import pygpen as pp

@pp.vfx.particle_init('dirt')
def dirt_particle_init(self):
    self.acceleration[1] = 350
    self.velocity_caps[1] = 350

@pp.vfx.particle_behavior('dirt')
def dirt_particle_behave(self, dt):
    pass

@pp.vfx.particle_init('grass')
def grass_particle_init(self):
    self.time = self.e['Window'].time

@pp.vfx.particle_behavior('grass')
def grass_particle_behave(self, dt):
    self.pos[0] += math.sin(self.e['Window'].time * 2 + self.time) * dt * 30