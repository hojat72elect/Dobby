from . import pygpen as pp

ITEM_MAP = {'chungu': 'Pickaxe', 'luna': 'Hat', 'hatrick': 'Pocket Watch'}
HARD_CONSONANTS = ['q', 't', 'p', 'd', 'g', 'j', 'k', 'x', 'c', 'b']
SOFT_CONSONANTS = ['w', 'r', 'y', 's', 'f', 'h', 'l', 'z', 'v', 'n', 'm']

class HUD(pp.ElementSingleton):
    def __init__(self):
        super().__init__()
        
        self.talking = False
        self.talking_text = []
        self.talking_target = 'george'
        self.text_progress = 0
        
        self.maps = []
        self.ever_opened_maps = False
        self.inventory = []
        
        self.show_maps = False
        self.maps_pos = 0
        
        self.item_notification_pos = 0
        self.item_timer = 0
        
        self.last_shown_chars = 0
        
        self.tutorial = True
        self.found_item = False
        
    def render(self):
        self.item_timer = max(0, self.item_timer - self.e['Window'].dt)
        item_pos = 150 if self.item_timer else 0
        self.item_notification_pos += (item_pos - self.item_notification_pos) * min(1, self.e['Window'].dt * 6)
        if len(self.inventory):
            self.e['Renderer'].blit(self.e['Assets'].images['items'][self.inventory[-1]], (self.e['Game'].display.get_width() // 2 - 10, 230 - self.item_notification_pos), z=100, group='ui')
            self.e['Text']['small_font'].renderz(ITEM_MAP[self.inventory[-1]] + ' Acquired!', (self.e['Game'].display.get_width() // 2 - self.e['Text']['small_font'].width(ITEM_MAP[self.inventory[-1]] + ' Acquired!') // 2, 253 - self.item_notification_pos), color=(255, 255, 255), z=101, group='ui')
            self.e['Text']['small_font'].renderz(ITEM_MAP[self.inventory[-1]] + ' Acquired!', (self.e['Game'].display.get_width() // 2 - self.e['Text']['small_font'].width(ITEM_MAP[self.inventory[-1]] + ' Acquired!') // 2 + 1, 254 - self.item_notification_pos), color=(0, 0, 1), z=100, group='ui')
        
        for i, item in enumerate(self.inventory):
            self.e['Renderer'].blit(self.e['Assets'].images['items'][item], (5 + 24 * i, 5), z=100, group='ui')
        
        mtarget = 200 if self.show_maps else 0
        self.maps_pos += (mtarget - self.maps_pos) * min(1, self.e['Window'].dt * 6)
        for i, map in enumerate(self.maps):
            spread = [20, 223]
            map_r = i / (len(self.maps) - 1) if len(self.maps) > 1 else 0.5
            map_x = spread[0] + map_r * (spread[1] - spread[0])
            self.e['Renderer'].blit(self.e['Assets'].images['maps']['map_' + map], (map_x, 230 - self.maps_pos), z=100, group='ui')
            
        if self.tutorial:
            button_img = 'tutorial' if (self.e['Window'].time % 1 < 0.65) else 'tutorial_2'
            self.e['Renderer'].blit(self.e['Assets'].images['misc'][button_img], (self.e['Game'].player.center[0] - 16 - self.e['Game'].camera[0], self.e['Game'].player.pos[1] - 30 - self.e['Game'].camera[1]), z=99, group='ui')
        
        if self.talking:
            self.text_progress += self.e['Window'].dt * 25
            if self.text_progress < 10:
                self.text_progress += self.e['Window'].dt * 25
            name = self.talking_target[0].upper() + self.talking_target[1:]
            
            self.e['Renderer'].blit(self.e['Assets'].images['portraits'][self.talking_target], (17, 145), z=90, group='ui')
            self.e['Renderer'].blit(self.e['Assets'].images['misc']['portrait_overlay'], (15, 143), z=91, group='ui')
            self.e['Text']['small_font'].renderz(name[:int(self.text_progress)], (70, 156), color=(0, 0, 1), z=91, group='ui')
            self.e['Text']['small_font'].renderz(name[:int(self.text_progress)], (71, 155), color=(255, 255, 255), z=92, group='ui')
            if len(self.talking_text):
                shown_chars = min(max(0, int(self.text_progress) - 10), len(self.talking_text[0]))
                if shown_chars != self.last_shown_chars:
                    if self.talking_text[0][min(max(0, int(self.text_progress) - 10), len(self.talking_text[0]) - 1)] in HARD_CONSONANTS:
                        self.e['Sounds'].play(self.talking_target, volume=0.5)
                    if self.talking_text[0][min(max(0, int(self.text_progress) - 10), len(self.talking_text[0]) - 1)] in SOFT_CONSONANTS:
                        self.e['Sounds'].play(self.talking_target, volume=0.3)
                self.last_shown_chars = shown_chars
                self.e['Text']['small_font'].renderz(self.talking_text[0][:max(0, int(self.text_progress) - 10)], (70, 165), color=(255, 255, 255), line_width=200, z=92, group='ui')
                self.e['Text']['small_font'].renderz(self.talking_text[0][:max(0, int(self.text_progress) - 10)], (71, 166), color=(0, 0, 1), line_width=200, z=91, group='ui')
            if self.text_progress > len(self.talking_text[0]) + 10:
                button_img = 'x_button' if (self.e['Window'].time % 1 < 0.65) else 'x_button_2'
                self.e['Renderer'].blit(self.e['Assets'].images['misc'][button_img], (290, 180), z=99, group='ui')
            if self.e['Input'].pressed('interact'):
                if self.text_progress < len(self.talking_text[0]) + 10:
                    self.text_progress = len(self.talking_text[0]) + 10
                else:
                    self.talking_text.pop(0)
                    self.e['Sounds'].play('interact', volume=0.5)
                    self.text_progress = 10
                    if not len(self.talking_text):
                        self.talking = False
        else:
            if self.e['Input'].pressed('maps'):
                if len(self.maps):
                    self.show_maps = not self.show_maps
                    self.ever_opened_maps = True
                    if self.show_maps:
                        self.e['Sounds'].play('open_maps')
                    else:
                        self.e['Sounds'].play('close_maps')
        