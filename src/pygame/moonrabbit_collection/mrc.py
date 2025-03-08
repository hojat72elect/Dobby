import sys
import time
import math
import random

import pygame
from pygame.locals import *

import scripts.pygpen as pp

import scripts.particles
from scripts.hud import HUD
from scripts.player import Player
from scripts.spawn_hook import gen_hook

class Game(pp.PygpenGame):
    def load(self):
        pp.init(
            (960, 630),
            entity_path='data/images/entities',
            sounds_path='data/sfx',
            spritesheet_path='data/images/spritesheets',
            caption='Moonrabbit Collection',
            input_path='data/config/key_mappings.json',
            font_path='data/fonts',
            opengl=True,
            frag_path='data/shaders/frag.frag'
        )
        
        self.display = pygame.Surface((320, 210))
        self.ui_surf = pygame.Surface((320, 210), pygame.SRCALPHA)
        
        HUD()
        
        self.e['Assets'].enable('foliage')
        self.e['Assets'].load_folder('data/images/background', colorkey=(0, 0, 0))
        self.e['Assets'].load_folder('data/images/misc', colorkey=(0, 0, 0))
        self.e['Assets'].load_folder('data/images/maps', colorkey=(0, 0, 0))
        self.e['Assets'].load_folder('data/images/items', colorkey=(0, 0, 0))
        self.e['Assets'].load_folder('data/images/portraits', colorkey=(0, 0, 0))
        self.e['Renderer'].set_groups(['default', 'ui'])
        
        self.noise_tex = self.e['MGL'].pg2tx(self.e['Assets'].images['misc']['noise'])
        self.glow_img = pygame.Surface((255, 255))
        self.glow_img.fill((174 * 0.2, 226 * 0.2, 255 * 0.3))
        self.glow_img.blit(self.e['Assets'].images['misc']['light'], (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        self.gm = pp.vfx.GrassManager('data/images/grass', tile_size=14)
        
        self.talked_to = set()
            
        self.tilemap = pp.Tilemap(tile_size=(16, 16))
        self.tilemap.load('data/maps/map.pmap', spawn_hook=gen_hook())
        
        self.player = Player('player', (390, 170))
        self.e['EntityGroups'].add(self.player, 'entities')
        
        self.camera = pp.Camera(self.display.get_size(), slowness=0.5, tilemap_lock=self.tilemap)
        self.camera.set_target(self.player)
        
        self.background_items = []
        for i in range(40):
            img = random.choice(list(self.e['Assets'].images['background'].values()))
            if img == self.e['Assets'].images['background']['moon']:
                img = random.choice(list(self.e['Assets'].images['background'].values()))
            self.background_items.append(([random.random() * self.display.get_width(), random.random() * self.display.get_height()], img, random.random()))
            
        self.fireflies = []
        for i in range(20):
            self.fireflies.append([[random.random() * self.display.get_width(), random.random() * self.display.get_height()], random.random() * math.pi * 2, random.random() * 10 + 10, random.random() * 4 * random.choice([-1, 1])])
        self.firefly_img = pygame.Surface((1, 1))
        self.firefly_img.fill((255, 255, 255))
        
        pygame.mixer.music.load('data/music.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
        self.e['Sounds'].play('ambience', times=-1, volume=0.5)
        
    def render_background(self):
        for item in self.background_items:
            self.e['Renderer'].blit(item[1], ((item[0][0] - self.camera[0] * item[2] * 0.1) % self.display.get_width(), (item[0][1] - self.camera[1] * item[2] * 0.1) % self.display.get_height()), z=-100)
            
        for firefly in self.fireflies:
            firefly[0] = pp.utils.game_math.advance(firefly[0], firefly[1], firefly[2] * self.e['Window'].dt)
            firefly[1] += firefly[3] * self.e['Window'].dt
            if random.random() * 4 < self.e['Window'].dt:
                firefly[3] = random.random() * 4 * random.choice([-1, 1])
                firefly[2] = random.random() * 10 + 10

            wpos = (int((firefly[0][0] - self.camera[0] * 1.2) % self.display.get_width()), int((firefly[0][1] - self.camera[1] * 1.2) % self.display.get_height()))
            self.e['Renderer'].blit(self.firefly_img, wpos, z=11)
            diameter = math.sin(firefly[2] * 0.2 + self.e['Window'].time) * 8 + 25
            glow_img = pygame.transform.scale(self.glow_img, (diameter, diameter))
            self.e['Renderer'].blit(glow_img, (wpos[0] - glow_img.get_width() // 2, wpos[1] - glow_img.get_height() // 2), z=107)
            
    def update(self):
        self.display.fill((0, 0, 0))
        self.ui_surf.fill((0, 0, 0, 0))
        
        self.camera.update()
        
        self.tilemap.renderz(pygame.Rect(self.camera[0] - 14, self.camera[1] - 14, self.display.get_width() + 14, self.display.get_height() + 14), offset=self.camera)
        
        self.e['Window'].screen.fill((100, 0, 0))
        
        self.e['EntityGroups'].update()
        self.e['EntityGroups'].renderz(offset=self.camera)
        
        self.e['HUD'].render()
        
        self.render_background()
        
        self.e['Renderer'].renderf(self.gm.update_render, self.e['Window'].dt, offset=self.camera, rot_function=lambda x, y: int((math.sin(x / 100 + time.time() * 1.5) - 0.7) * 30) / 10, z=-5)
            
        self.e['Renderer'].cycle({'default': self.display, 'ui': self.ui_surf})
        
        if self.e['Input'].pressed('quit'):
            pygame.quit()
            sys.exit()

        self.e['Window'].cycle({'surface': self.display, 'ui_surf': self.ui_surf, 'noise_tex': self.noise_tex, 'time': int((self.e['Window'].time - self.e['Window'].start_time) * 100), 'camera': tuple(list(self.camera))})
        
Game().run()