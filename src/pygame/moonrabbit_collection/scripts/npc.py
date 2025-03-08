from . import pygpen as pp

class NPC(pp.PhysicsEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.acceleration[1] = 450
        self.speed = 70
        self.z = -4
        
        self.quest_complete = False
        self.first_talk = True
        
    def get_dialogue(self):
        if self.type == 'george':
            george_text = []
            if self.first_talk:
                george_text = [
                    'Hey there!',
                    'I\'m George!',
                    'I like to practice magic. It\'s amazing what it can do.',
                    'You seem like the type to take interest in this kind of thing.']
            else:
                george_text = ['Hello.']
            
            add_map = False
            for npc in ['chungu', 'hatrick', 'luna']:
                if (npc in self.e['Game'].talked_to) and (npc not in self.e['HUD'].maps):
                    add_map = True
                    self.e['HUD'].maps.append(npc)
            if add_map:
                george_text.append('I see you need help finding something. My magic orb can help with that.')
                george_text.append('Uuuuuooooooaaaaah oo ooo oo...')
                george_text.append('Shoes!')
                george_text.append('...')
                george_text.append('Alright, that should do it. Here\'s a map of the area the lost things might be in.')
            return george_text
        if self.type == 'chungu':
            if not self.quest_complete:
                if self.first_talk:
                    return [
                        'I was out digging for \'em rare gems a couple days ago when I suddenly passed out from exhaustion!',
                        'Seems I\'ve lost my trusty pickaxe. I\'ve looked everywhere, but I can\'t find it.',
                        'Could you help me find it? If you ask George he may be able to help out.',
                        'He has a knack for this type of thing.']
                elif self.type in self.e['HUD'].inventory:
                    self.quest_complete = True
                    self.e['HUD'].inventory.remove(self.type)
                    return ['You found my trusty pickaxe! Thanks so much for your help!', 'Now I can get back to gem hunting...']
                else:
                    return ['Ask George if he can help find my pickaxe.']
            else:
                return ['Hmm, I don\'t quite feel like going mining today...']
        if self.type == 'luna':
            if not self.quest_complete:
                if self.first_talk:
                    return [
                        'I was enjoying a picnic yesterday and my hat got blown off my head!',
                        'If it\'s not too much to ask, could you help me look for it? I can\'t seem to find it.',
                        'I think George may be able to help with this kind of thing.',
                        'I don\'t know about all the magic he does but he\'s always helpful!']
                elif self.type in self.e['HUD'].inventory:
                    self.quest_complete = True
                    self.e['HUD'].inventory.remove(self.type)
                    return ['Oh, there it is! It\'s my hat...', 'How did it get so dirty?', 'Oh well, I guess I\'ll just have to wash it.', 'Thanks for your help!']
                else:
                    return ['George should be able to help with finding my hat.']
            else:
                return ['I think I\'ll go have a picnic again tomorrow.']
        if self.type == 'hatrick':
            if not self.quest_complete:
                if self.first_talk:
                    return [
                        'Hey there lad.',
                        'It\'s wonderful weather right now innit.',
                        'Oh, you seem like the type to help me out with a problem of mine.',
                        'I\'ve had my grandfather\'s pocket watch ever since he passed. However it seems it has fallen out of my pocket!',
                        'What a horrid thing to happen! I\'ve no idea where it could be.',
                        'If you could work with George to help me get it back, that would be splendid.'
                    ]
                elif self.type in self.e['HUD'].inventory:
                    self.quest_complete = True
                    self.e['HUD'].inventory.remove(self.type)
                    return ['I see you\'ve found the pocket watch.', 'Splendid!', 'It would\'ve been an awful thing to have lost forever.']
                else:
                    return ['The chap that lives above me, George, should be able to help find my grandfather\'s pocket watch.']
            else:
                return ['I just finished my tea break. Now I\'m enjoying this wonderful weather.']
        
        return ['what']
        
    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        
        self.flip[0] = self.e['Game'].player.center[0] < self.center[0]
            
        self.physics_update(self.e['Game'].tilemap)
        
        if (not self.e['HUD'].talking) and (not self.e['HUD'].show_maps):
            if pp.utils.game_math.distance(self.center, self.e['Game'].player.center) < 22:
                button_img = 'x_button' if (self.e['Window'].time % 1 < 0.65) else 'x_button_2'
                self.e['Renderer'].blit(self.e['Assets'].images['misc'][button_img], (self.center[0] - 5 - self.e['Game'].camera[0], self.pos[1] - 26 - self.e['Game'].camera[1]), z=50, group='ui')
                if self.e['Input'].pressed('interact'):
                    self.e['Input'].input['interact'].just_pressed = False
                    self.e['HUD'].talking = True
                    self.e['HUD'].talking_target = self.type
                    self.e['HUD'].talking_text = self.get_dialogue()
                    self.first_talk = False
                    self.text_progress = 0
                    self.e['Game'].talked_to.add(self.type)
            elif self.type == 'george':
                if (not self.e['HUD'].ever_opened_maps) and (len(self.e['HUD'].maps)):
                    button_img = 'z_button' if (self.e['Window'].time % 1 < 0.65) else 'z_button_2'
                    self.e['Renderer'].blit(self.e['Assets'].images['misc'][button_img], (290, 180), z=50, group='ui')