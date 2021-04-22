from constants import P_ATK
from model.actor import Actor


class PlayerActor(Actor):
    def __init__(self, name, pos=None, health=100, inventory=None, non_walkable_tiles=["Wall"], move_speed=2):
        super().__init__(name=name, pos=pos, health=health, non_walkable_tiles=non_walkable_tiles, move_speed=move_speed, atk_power=P_ATK)
        self.inventory = inventory if inventory else []


    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()
