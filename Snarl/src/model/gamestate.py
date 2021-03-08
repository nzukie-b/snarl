import copy
from coord import Coord
from model.room import Room
from model.adversary import Adversary
from model.player import Player


class GameState:
    def __init__(self, level, players, adversaries, exit_locked=False):
        self.level = level
        self.players = players
        self.adversaries = adversaries
        self.exit_locked = exit_locked


def remove_doors_and_items_from_rooms(first):
    first_rm = copy.deepcopy(first)
    first_rm_removed = []

    print("1 " + str(len(first.tiles)))
    print("2 " + str(len(first_rm.tiles)))

    for tile in first_rm.tiles:
        print(str(tile.row) + " " + str(tile.col) + " in doors " + str(tile in first.doors))
        print(str(tile.row) + " " + str(tile.col) + " in items " + str(tile in first.items))
        if tile not in first.doors and tile not in first.items:
            print("ADD TO LIST: " + str(tile.row) + " " + str(tile.col))
            first_rm_removed.append(tile)

    print("3 " + str(len(first.tiles)))
    print("4 " + str(len(first_rm.tiles)))

    return Room(first_rm.origin, first_rm.dimensions, first_rm_removed, first_rm.doors, first_rm.items)



def create_initial_game_state(level, num_players, num_adversaries):
    players = []
    adversaries = []

    last_room = remove_doors_and_items_from_rooms(level.rooms[len(level.rooms) - 1])
    first_room = remove_doors_and_items_from_rooms(level.rooms[0])

    for i in range(num_players):
        cur_tile = first_room.tiles[i]
        print("ADDP: " + str(cur_tile.row) + " " + str(cur_tile.col))
        players.append(Player(Coord(cur_tile.row, cur_tile.col), "Bruh " + str(i), 3))

    for i in range(num_adversaries):
        cur_adversary_tile = last_room.tiles[i]
        print("ADDA: " + str(cur_adversary_tile.row) + " " + str(cur_adversary_tile.col))
        adversaries.append(Adversary(Coord(cur_adversary_tile.row, cur_adversary_tile.col), "Evil Bruh " + str(i), 3))

    #print(str(adversaries))

    return [players, adversaries]


def update_game_state(new_players_locs, new_adversary_locs, new_players_healths, new_adversary_healths, level_exit_status):
    """
    Replaces the current gamestate with a new gamestate made up of the updated values for all of the game attributes.
    :param new_players_locs: [Coord]
    :param new_adversary_locs: [Coord]
    :param new_players_healths: [int]
    :param new_adversary_healths: [int]
    :param level_exit_status: boolean
    :return:
    """
    players = []
    adversaries = []

    for i in range(len(new_players_locs)):
        players.append(Player(new_adversary_locs[i], "Bruh " + str(i), new_players_healths[i]))

    for i in range(len(new_adversary_locs)):
        adversaries.append(Adversary(new_adversary_locs[i], "Evil Bruh " + str(i), new_adversary_healths[i]))

    return GameState(players, adversaries)