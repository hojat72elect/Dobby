from . import pygpen as pp

class Item(pp.Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        
        if pp.utils.game_math.distance(self.center, self.e['Game'].player.center) < 16:
            if self.type not in self.e['HUD'].inventory:
                if 0 < self.e['Game'].player.digging < 0.5:
                    self.e['HUD'].inventory.append(self.type)
                    self.e['HUD'].item_timer = 4
                    self.e['Sounds'].play('collect')
                    self.e['HUD'].found_item = True
                    return True
            if (not self.e['HUD'].found_item) and (self.type in self.e['HUD'].maps):
                button_img = 'down_button' if (self.e['Window'].time % 1 < 0.65) else 'down_button_2'
                self.e['Renderer'].blit(self.e['Assets'].images['misc'][button_img], (self.e['Game'].player.center[0] - 4 - self.e['Game'].camera[0], self.e['Game'].player.pos[1] - 20 - self.e['Game'].camera[1]), z=50, group='ui')
    
    def renderz(self, *args, **kwargs):
        pass