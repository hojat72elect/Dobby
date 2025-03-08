import math
import random

from . import pygpen as pp

from .animation import Animation

class Player(pp.PhysicsEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.acceleration[1] = 450
        self.speed = 50
        self.autoflip = 1
        self.air_time = 0
        self.z = -4
        self.jumps = 2
        self.target_rot = 0
        self.digging = 0
        
    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        
        self.e['Game'].gm.apply_force(self.center, 7, 4)
        
        self.digging = max(0, self.digging - self.e['Window'].dt)
        
        if self.digging:
            if self.e['Window'].dt > random.random() * 0.1:
                angle = -math.pi * (0.5 * random.random() + 0.25)
                force = random.random() * 50 + 50
                particle = pp.vfx.Particle((self.center[0], self.center[1] + 4), 'particle', decay_rate=0.25, advance=random.random() * 0.3 + 0.3, velocity=[math.cos(angle) * force, math.sin(angle) * force], behavior='dirt', colors={(255, 255, 255): (135, 53, 85)}, physics_source=self.e['Game'].tilemap)
                self.e['EntityGroups'].add(particle, 'particles')
                self.e['Sounds'].play('dig')
        
        self.rotation = pp.utils.game_math.normalize(self.rotation, self.e['Window'].dt * 1440, self.target_rot)
        
        if (not self.e['HUD'].talking) and (not self.e['HUD'].show_maps) and not (self.digging):
            self.apply_force(((self.e['Input'].holding('right') - self.e['Input'].holding('left')) * self.speed, 0))
            
            v = -1 if self.flip[0] else 1
            if self.next_movement[0] * v < 0:
                anim = Animation('turn_anim', self.pos)
                if self.next_movement[0] < 0:
                    anim.flip[0] = True
                self.e['EntityGroups'].add(anim, 'entities')
            
            if self.e['Input'].pressed('up'):
                if self.jumps > 0:
                    self.e['HUD'].tutorial = False
                    self.e['EntityGroups'].add(Animation('jump_anim', self.pos), 'entities')
                    self.e['Sounds'].play('jump')
                    if self.jumps == 2:
                        self.velocity[1] = -160
                    if self.jumps == 1:
                        self.velocity[1] = -175
                        if self.flip[0]:
                            self.target_rot += 360
                        else:
                            self.target_rot -= 360
                    self.jumps -= 1
                    self.air_time = 0.1
                
            if self.e['Input'].holding('up') and (self.jumps == 1):
                self.acceleration[1] = 250
            else:
                self.acceleration[1] = 450
                
            if self.e['Input'].pressed('down'):
                if self.air_time < 0.1:
                    self.digging = 1.5
        
        if self.digging:
            self.set_action('dig')
        elif self.air_time > 0.1:
            self.set_action('jump')
        else:
            if self.next_movement[0] != 0:
                self.set_action('run')
            else:
                self.set_action('idle')
            
        self.physics_update(self.e['Game'].tilemap)
        
        if self.collide_directions['down']:
            if self.air_time > 0.5:
                self.e['EntityGroups'].add(Animation('land_anim', self.pos), 'entities')
                self.e['Sounds'].play('land', volume=0.5)
            self.air_time = 0
            self.jumps = 2
        else:
            self.air_time += self.e['Window'].dt