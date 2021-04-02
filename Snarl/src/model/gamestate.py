import copy
from constants import STATE
from coord import Coord
from utilities import to_point, to_coord
from model.room import Room
from model.adversary import AdversaryActor
from model.player import PlayerActor

class StateObj:
    def __init__(self, level, players, adversaries, exit_locked):
        self.type = STATE
        self.level = level
        self.players = players
        self.adversaries = adversaries
        self.exit_locked = exit_locked

    def __str__(self):
        return '{{"type": {}, "level": {}, "players": {}, "adversaries": {}, "exit-locked": {}'.format(self.type, self.level, self.players, self.adversaries, self.exit_locked)
    
    def __repr__(self):
        return str(self)


class GameState:
    def __init__(self, levels, players, adversaries, exit_locked=True):
        multi_levels = isinstance(levels, list)
        if multi_levels:
            next_level = next(l for l in levels)
            self.current_level = levels.remove(next_level)
            self.levels = levels
        else:
            self.current_level = levels
            levels = []
        self.players = players
        self.adversaries = adversaries
        self.exit_locked = exit_locked
        self.game_status = None
        self.ejected_players = set()
    
    def __str__(self):
        level_str = str(self.current_level)
        players_str = [str(player) for player in self.players]
        adversaries_str = [str(adversary) for adversary in self.adversaries]
        return '{{"level": {}, "players": {}, "adversaries": {}, "exit_locked": {}}}'.format(level_str, players_str, adversaries_str, self.exit_locked)

    def __repr__(self):
        return str(self)

def remove_doors_and_items_from_rooms(first):
    '''Remove doors and items from walkable tiles. Used to determine initial placement of entities'''
    first_rm = copy.deepcopy(first)
    first_rm_removed = []
    for tile in first_rm.tiles:
        if tile not in first.doors and tile not in first.items:
            first_rm_removed.append(tile)
    return Room(first_rm.origin, first_rm.dimensions, first_rm_removed, first_rm.doors, first_rm.items)


def create_initial_game_state(level, players, adversaries):
    '''Creates the initial gamestate. Places entities on their provided position. If not provided then, places players on walkable tiles in the first room. Places adversaries on walkables tiles in the last room.'''
    player_placements = []
    adversary_placements = []

    last_room = remove_doors_and_items_from_rooms(level.rooms[-1])
    first_room = remove_doors_and_items_from_rooms(level.rooms[0])

    for i in range(len(players)):
        player = players[i]
        if player.pos is None:
            cur_tile = first_room.tiles[i]
            player.pos = Coord(cur_tile.row, cur_tile.col)
        player_placements.append(player)

    for i in range(len(adversaries)):
        adversary = adversaries[i]
        if adversary.pos is None:
            cur_adversary_tile = last_room.tiles[i]
            adversary.pos = Coord(cur_adversary_tile.row, cur_adversary_tile.col)
        adversary_placements.append(adversary)

    return [player_placements, adversary_placements]



def update_game_state(new_players, new_adversaries, exit_locked):
    """
    Replaces the current gamestate with a new gamestate made up of the updated values for all of the game attributes.
    :param new_players_locs: [Coord]
    :param new_adversary_locs: [Coord]
    :param new_players_healths: [int]
    :param new_adversary_healths: [int]
    :param exit_locked: boolean
    :return:
    """
    players = []
    adversaries = []

    for i in range(len(new_players)):
        players.append(PlayerActor(new_players[i].pos, new_players[i].name, new_players[i].health, new_players[i].inventory, new_players[i].non_walkable_tiles, new_players[i].move_speed))

    for i in range(len(new_adversaries)):
        adversaries.append(AdversaryActor(new_adversaries[i].pos, new_adversaries[i].name, new_adversaries[i].health, new_adversaries[i].inventory, new_adversaries[i].non_walkable_tiles, new_adversaries[i].move_speed))

    return GameState(players, adversaries, exit_locked=exit_locked)