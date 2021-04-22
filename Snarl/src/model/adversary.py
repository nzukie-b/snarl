from constants import GHOST, G_ATK, Z_ATK
from constants import ZOMBIE
from model.actor import Actor

class AdversaryActor(Actor):
    def __init__(self, name, type_=ZOMBIE, pos=None, health=100, non_walkable_tiles=["Wall"], move_speed=1):
        atk_power = self.__get_attack_power(type_)
        super().__init__(name=name, pos=pos, health=health, move_speed=move_speed, atk_power=atk_power)
        self.type = type_
        self.non_walkable_tiles = non_walkable_tiles if type_ == ZOMBIE else None
    
    def __str__(self):
        return super().__str__(self)

    def __repr__(self):
        return super().__repr__(self)

    def __get_attack_power(self, type_):
        if type_ == GHOST:
            return G_ATK
        elif type_ == ZOMBIE:
            return G_ATK
