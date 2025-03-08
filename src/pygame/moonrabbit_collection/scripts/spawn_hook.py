from . import pygpen as pp

from .npc import NPC
from .item import Item

entity_map = {(0, 0): ('player', NPC), (0, 1): ('chungu', NPC), (0, 2): ('hatrick', NPC), (0, 3): ('luna', NPC), (0, 4): ('george', NPC)}
item_map = {(0, 0): ('chungu', Item), (0, 1): ('hatrick', Item), (0, 2): ('luna', Item)}

def gen_hook():
    default_grass = pp.elems['Game'].gm.basic_pmap_hook('grass_e', tile_id=(0, 0), density_range=[4, 6], grass_options=[0, 1, 2, 3, 4, 5, 6])
    wheat_grass = pp.elems['Game'].gm.basic_pmap_hook('grass_e', tile_id=(0, 1), density_range=[4, 6], grass_options=[7, 8])
    def hook(tile_data, ongrid):
        if not default_grass(tile_data, ongrid):
            return False
        
        if not wheat_grass(tile_data, ongrid):
            return False
        
        wpos = tile_data['pos']
        if ongrid:
            wpos = (wpos[0] * 14, wpos[1] * 14)
        
        if tile_data['group'] == 'entities':
            if tuple(tile_data['tile_id']) in entity_map:
                entity_info = entity_map[tuple(tile_data['tile_id'])]
                entity = entity_info[1](entity_info[0], wpos)
                pp.elems['EntityGroups'].add(entity, 'entities')
                return False
            
        if tile_data['group'] == 'items':
            if tuple(tile_data['tile_id']) in entity_map:
                entity_info = item_map[tuple(tile_data['tile_id'])]
                entity = entity_info[1](entity_info[0], wpos)
                pp.elems['EntityGroups'].add(entity, 'entities')
                return False
        
        return True
    
    return hook