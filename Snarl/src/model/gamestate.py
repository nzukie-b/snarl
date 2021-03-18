import copy
from coord import Coord
from utilities import to_point, to_coord
from model.room import Room
from model.adversary import Adversary
from model.player import Player

class State_Obj:
    def __init__(self, level, players, adversaries, exit_locked):
        self.type = 'state'
        self.level = level
        self.players = players
        self.adversaries = adversaries
        self.exit_locked = exit_locked

    def __str__(self):
        return '{{"type": {}, "level": {}, "players": {}, "adversaries": {}, "exit-locked": {}'.format(self.type, self.level, self.players, self.adversaries, self.exit_locked)
    
    def __repr__(self):
        return str(self)


class GameState:
    def __init__(self, level, players, adversaries, exit_locked=True):
        self.level = level
        self.players = players
        self.adversaries = adversaries
        self.exit_locked = exit_locked
    
    def __str__(self):
        level_str = str(self.level)
        players_str = [str(player) for player in self.players]
        adversaries_str = [str(adversary) for adversary in self.adversaries]
        return '{{"level": {}, "players": {}, "adversaries": {}, "exit_locked": {}}}'.format(level_str, players_str, adversaries_str, self.exit_locked)

    def __repr__(self):
        return str(self)
    

def remove_doors_and_items_from_rooms(first):
    '''Remove doors and items from walkable tiles. Used to determine initial placement of entities'''
    first_rm = copy.deepcopy(first)
    first_rm_removed = []

    # print("1 " + str(len(first.tiles)))
    # print("2 " + str(len(first_rm.tiles)))

    for tile in first_rm.tiles:
        # print(str(tile.row) + " " + str(tile.col) + " in doors " + str(tile in first.doors))
        # print(str(tile.row) + " " + str(tile.col) + " in items " + str(tile in first.items))
        if tile not in first.doors and tile not in first.items:
            # print("ADD TO LIST: " + str(tile.row) + " " + str(tile.col))
            first_rm_removed.append(tile)

    # print("3 " + str(len(first.tiles)))
    # print("4 " + str(len(first_rm.tiles)))

    return Room(first_rm.origin, first_rm.dimensions, first_rm_removed, first_rm.doors, first_rm.items)


# def initialize_state(level, players, ad)

def create_initial_game_state(level, players, adversaries):
    player_placements = []
    adversary_placements = []

    last_room = remove_doors_and_items_from_rooms(level.rooms[-1])
    first_room = remove_doors_and_items_from_rooms(level.rooms[0])

    for i in range(len(players)):
        cur_tile = first_room.tiles[i]
        player = players[i]    
        player.pos = Coord(cur_tile.row, cur_tile.col)
        player_placements.append(player)

    for i in range(len(adversaries)):
        cur_adversary_tile = last_room.tiles[i]
        adversary = adversaries[i]
        adversary.pos = Coord(cur_adversary_tile.row, cur_adversary_tile.col)
        adversary_placements.append(adversary)

    return [player_placements, adversary_placements]


def update_game_state(new_players_locs, new_adversary_locs, new_players_healths, new_adversary_healths, exit_locked):
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

    for i in range(len(new_players_locs)):
        players.append(Player(new_players_locs[i], "Bruh " + str(i), new_players_healths[i]))

    for i in range(len(new_adversary_locs)):
        adversaries.append(Adversary(new_adversary_locs[i], "Evil Bruh " + str(i), new_adversary_healths[i]))

    return GameState(players, adversaries, exit_locked=exit_locked)