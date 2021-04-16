import sys, os
from typing import List
currentdir = os.path.dirname(os.path.realpath(__file__))
snarl_dir = os.path.dirname(currentdir)
game_dir = snarl_dir + '/src'
sys.path.append(game_dir)
from constants import EJECT, HALLWAY, INFO, KEY, MAX_PLAYERS, ORIGIN, P_WIN, ROOM, STATUS, TYPE, VALID_MOVE, ZOMBIE
from adversary.remoteAdversary import RemoteAdversary
from player.remotePlayer import RemotePlayer
from coord import Coord
from common.player import Player
from player.localPlayer import LocalPlayer
from common.adversary import Adversary
from adversary.localAdversary import LocalAdversary
from model.player import PlayerActor
from model.adversary import AdversaryActor
from model.gamestate import GameState, create_initial_game_state
from game.ruleChecker import RuleChecker
from utilities import update_adversary_levels, update_adversary_players, check_position, find_room_by_origin, find_hallway_by_origin
class GameManager:
    def __init__(self):
        #List of player clients
        self.players = []
        #List of adversary clients
        self.adversaries = []
        self.gamestate = None
        self.rc = RuleChecker()
        self.player_turns = []
        # Names of players that need to go during this turn
        self.adv_turns = []
        self.start_level = 0
        self.next_level_indx = 0
        

    def __reset_player_turns(self):
        try:
            out_players = self.gamestate.out_players
        except AttributeError:
            out_players = []
        return [player.name for player in self.players if player.name not in out_players]

    def __reset_adversary_turns(self):
        return [adversary.name for adversary in self.adversaries]

    def __reset_turns(self):
        self.player_turns = self.__reset_player_turns()
        self.adv_turns = self.__reset_adversary_turns()

    def get_player_actor(self, name) -> PlayerActor:
        '''Returns the PlayerActor object associated with the provided name'''
        player = next(player for player in self.gamestate.players if player.name == name)
        return player

    def get_player_actors(self):
        players = [self.get_player_actor(p.name) for p in self.players]
        return players

    def get_player_coords(self, name=None) -> List[Coord]:
        '''Returns a list of player coords excluding any player with the optionally provided name'''
        players = self.get_player_actors()
        player_coords = [player.pos for player in players if player.name != name]
        return player_coords

    def get_adversary_actor(self, name) -> AdversaryActor:
        adversary = next(adv for adv in self.gamestate.adversaries if adv.name == name)
        return adversary
    
    def get_adversary_actors(self):
        advs = [self.get_adversary_actor(adv.name) for adv in self.adversaries]
        return advs

    def get_adversary_coords(self, name=None) -> List[Coord]:
        advs = self.get_adversary_actors()
        adv_coords = [adversary.pos for adversary in advs if adversary.name != name]
        return adv_coords

    def register_player(self, player_client, connection=None):
        if len(self.players) <= MAX_PLAYERS:
            registered_players = [p.name for p in self.players]
            if player_client not in registered_players:
                if (isinstance(player_client, Player)):
                    self.players.append(player_client)
                elif connection:
                    self.players.append(self.__create_remote_player(player_client, connection))
                else:
                    self.players.append(self.__create_local_player(player_client))


    def register_adversary(self, adversary_client, actor_type=ZOMBIE, remote=False):
        if isinstance(adversary_client, Adversary):
            self.adversaries.append(adversary_client)
        elif remote:
            # There isn't really a difference between remote and local adversaries at this point
             self.adversaries.append(self.__create_remote_adversary(adversary_client, actor_type))
        else:
             self.adversaries.append(self.__create_local_adversary(adversary_client, actor_type))

    def __create_remote_player(self, name, conn) -> Player:
        player_obj = PlayerActor(name)
        return RemotePlayer(socket=conn, name=name, player_obj=player_obj)

    def __create_local_player(self, name) -> Player:
        '''Helper for instantiating a localPlayer'''
        player_obj = PlayerActor(name)
        return LocalPlayer(name, player_obj=player_obj)

    def __create_local_adversary(self, name, type_) -> Adversary:
        adv_obj = AdversaryActor(name, type_=type_)
        return LocalAdversary(name, type_=type_, adversary_obj=adv_obj)

    def __create_remote_adversary(self, name, type_) -> Adversary:
        adv_obj = AdversaryActor(name, type_=type_)
        return RemoteAdversary(name, type_=type_, adversary_obj=adv_obj)

    def __init_state(self, levels, start_level=0) -> GameState:
        '''Create and return a GameState from list of levels.'''
        try:
            level = levels[start_level]
            player_objs = self.get_player_actors()
            adv_objs = self.get_adversary_actors()
        except ValueError:
            print('Invalid Starting level')
            return self.gamestate
        except TypeError:
            # Single level case
            level = levels
            player_objs = self.players
            adv_objs = self.adversaries
        except AttributeError:
            adv_objs = [a.adversary_obj for a in self.adversaries]
            player_objs = [a.player_obj for a in self.players]

        gs_info = create_initial_game_state(level, player_objs, adv_objs)
        update_adversary_levels(self.adversaries, level)

        return GameState(levels, gs_info[0], gs_info[1], current_level=level)

    def start_game(self, levels, start_level=0):
        if self.players:
            self.gamestate = self.__init_state(levels, start_level)
            self.__reset_turns()
            self.start_level = start_level
            self.next_level_indx = (start_level + 1) % len(levels) if isinstance(levels, list) else start_level
        else:
            print("Please register at least one player and adversary to start the game.")

    def __next_level(self):
        '''Initializes the gamestate with the next level, and updates adversaries current level'''
        if self.start_level != self.next_level_indx:
            old_state = self.gamestate
            new_state = self.__init_state(old_state.levels, self.next_level_indx)
            cur_level = new_state.current_level
            for adv in self.adversaries:
                adv.update_current_level(cur_level)
            level_indx = (self.next_level_indx + 1) % len(new_state.levels)
            self.gamestate = new_state
            self.next_level_indx = level_indx
            return new_state.levels.index(cur_level)
    
    def request_player_moves(self, new_players_locs):
        """
        Updates player info based on player move.
        :param new_players_locs: [Coord]
        :param new_players_healths: [int]
        :return:
        """

        for i in range(len(new_players_locs)):
            if self.rc.validate_player_movement(self.players[i].pos, new_players_locs[i], self.gamestate.current_level):
                self.gamestate = GameState(self.gamestate.current_level, self.players, self.adversaries, self.gamestate.exit_locked)
        else:
            self.players = self.gamestate.players

    def request_player_move(self, name, new_pos):
        '''Request a move from a player. If the move is invalid then returns false, otherwise it returns a dictionary with information of the move'''
        if len(self.player_turns) == len(self.adv_turns) == 0: self.__reset_turns()

        player = next(player for player in self.players if player.name == name)
        is_client = isinstance(player, Player)
        if is_client:
            player.pos = player.player_obj.pos

        if player.name in self.player_turns:
            p_coords = self.get_player_coords(player.name)
            a_coords = self.get_adversary_coords()
            player_move = self.rc.validate_player_movement(self.get_player_actor(player.name), new_pos, self.gamestate.current_level, p_coords, a_coords)
            if player_move[VALID_MOVE] and player_move[INFO].traversable:
                if player_move[EJECT]:
                    # Skip this players turn until the list of ejected players is reset i.e. in a level change
                    self.gamestate.out_players.append(name)
                self.players.remove(player)
                updated_players = self.get_player_actors()
                adversaries = self.get_adversary_actors()
                # If the new position is a door/waypoint, then move the player to the corresponding location.
                door_pos = self.__handle_door_traversal(new_pos, self.gamestate.current_level)
                if door_pos: new_pos = door_pos

                if is_client:
                    player.player_obj.pos = new_pos
                    updated_players.append(player.player_obj)
                else:
                    player.pos = new_pos
                    updated_players.append(player)

                self.players.append(player)
                self.gamestate = GameState(levels=self.gamestate.levels, current_level=self.gamestate.current_level, players=updated_players, 
                    adversaries=adversaries, exit_locked=self.gamestate.exit_locked, out_players=self.gamestate.out_players)
                self.player_turns.remove(player.name)

                # If all players have gone update adversaries for their moves
            if len(self.player_turns) == 0: update_adversary_players(self.adversaries, self.get_player_coords())
            return player_move
            
        return False

    def request_adversary_move(self, name, new_pos):
        if len(self.player_turns) == 0:
            if name in self.adv_turns:
                adv = next(adv for adv in self.adversaries if adv.name == name)
                is_client = isinstance(adv, Adversary)
                p_coords = self.get_player_coords()
                a_coords = self.get_adversary_coords(name)
                adv_move = self.rc.validate_adversary_movement(self.get_adversary_actor(name), new_pos, self.gamestate.current_level, p_coords, a_coords)
                if adv_move[VALID_MOVE]:
                    self.adversaries.remove(adv)
                    updated_advs = self.get_adversary_actors()
                    players = self.get_player_actors()

                    if adv_move[EJECT]:
                        player = next(p for p in players if p.pos == new_pos)
                        self.gamestate.out_players.append(player.name)
                    
                    if is_client:
                        adv.adversary_obj.pos = new_pos
                        updated_advs.append(adv.adversary_obj)
                    else:
                        adv.pos = new_pos
                        updated_advs.append(adv)

                    self.adversaries.append(adv)
                    self.gamestate = GameState(levels=self.gamestate.levels, current_level=self.gamestate.current_level, players=players, 
                        adversaries=updated_advs, exit_locked=self.gamestate.exit_locked, out_players=self.gamestate.out_players)

                self.adv_turns.remove(name)
                if len(self.adv_turns) == 0: self.__reset_turns()
                return adv_move
            else:
                print('name not in adv turns')
                print(self.adv_turns)
                print(name)
                return False
        else:
            print('player turns not empty')
            print(self.player_turns)
            return False


    def apply_player_item_interaction(self, player, item_pos):
        state = self.gamestate
        exit_locked = state.exit_locked
        for room in state.current_level.rooms:
            room_items = [item.pos for item in room.items]
            if item_pos in room_items:
                item = next(item for item in room.items if item.pos == item_pos)
                if item.type == KEY:
                    exit_locked = False
                room.items.remove(item)
                for p in self.players:
                    if p.name == player.name:
                        p.inventory.append(item)
        res = self.rc.validate_item_interaction(player, item_pos, state)
        if res:
            players = self.get_player_actors()
            adversaries = self.get_adversary_actors()
            self.gamestate = GameState(levels=state.levels, players=players, adversaries=adversaries, exit_locked=exit_locked, current_level=state.current_level, out_players=state.out_players)
        return res

    def handle_level_over(self):
        state = self.gamestate
        level_over = self.rc.is_level_over(state)
        if level_over[STATUS] == P_WIN:
            self.__next_level()
        return level_over

    def handle_game_over(self):
        state = self.gamestate
        game_over = self.rc.is_game_over(self.start_level, self.next_level_indx, state)
        return game_over

    def register_players(self, players):
        '''Create list of players from provided list of players'''
        if 1 < len(players) <= MAX_PLAYERS:
            for player in players:
                self.players.append(player)
        else:
            print('Invalid number of players to register please register between 1 and {} people'.format(MAX_PLAYERS))

    def register_adversaries(self, adversaries):
        '''Create list adversary objects from provided list of adversaries'''
        for adv in adversaries:
            self.adversaries.append(adv)

    def register_adversary_names(self, adversary_ids):
        """Create list of adversary objects using list of adversary ids."""
        for id_ in adversary_ids:
            self.adversaries.append(AdversaryActor(id_))


    def register_player_names(self, player_names):
        """Create list of player objects using list of player names."""
        temp_names = [name for name in set(player_names)]
        if len(temp_names) != len(player_names): 
            print('Duplicate player names.') 
            return False

        if 1 < len(player_names) <= MAX_PLAYERS:
            for name in player_names:
                p = PlayerActor(name)
                self.players.append(p)
        else:
            print("Too few or too many players to register, please register between 1 and 4 players.")

    def __handle_door_traversal(self, pos, level) -> Coord:
        '''Handles changing position for when an actor is traversing through a door/waypoint. Returns the coordinate of the corresponding door/waypoint'''
        new_pos = None
        pos_info = check_position(pos, level)
        if pos_info[TYPE] == ROOM:
            room = find_room_by_origin(pos_info[ORIGIN], level)
            for door in room.doors:
                if door == pos:
                    for hall in level.hallways:
                        for ii in range(2):
                            if pos == hall.doors[ii]:
                                # other_door_indx = (ii + 1) % 2
                                new_pos = hall.waypoints[ii]

        elif pos_info[TYPE] == HALLWAY:
            hall = find_hallway_by_origin(pos_info[ORIGIN], level)
            for ii in range(2):
                if pos == hall.waypoints[ii]:
                    new_pos = hall.doors[ii]

        return new_pos

                                


