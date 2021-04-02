import sys, os
currentdir = os.path.dirname(os.path.realpath(__file__))
snarl_dir = os.path.dirname(currentdir)
game_dir = snarl_dir + '/src'
sys.path.append(game_dir)
from constants import EJECT, INFO, MAX_PLAYERS, VALID_MOVE, ZOMBIE
from coord import Coord
from common.player import Player
from player.localPlayer import LocalPlayer
from common.adversary import Adversary
from common.actorUpdate import ActorUpdate
from model.player import PlayerActor
from model.adversary import AdversaryActor
from model.gamestate import GameState, create_initial_game_state
from game.ruleChecker import RuleChecker
from utilities import create_local_player, update_players, create_local_adversary
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

    def __reset_player_turns(self):
        ejected_players = self.gamestate.ejected_players
        return [player.name for player in self.players if player.name not in ejected_players]

    def __reset_adversary_turns(self):
        return [adversary.name for adversary in self.adversaries]

    def reset_turns(self):
        self.player_turns = self.__reset_player_turns()
        self.adv_turns = self.__reset_adversary_turns()


    def register_players(self, players):
        '''Create list of players from provided list of players'''
        if 1 < len(players) <= MAX_PLAYERS:
            for player in players:
                self.players.append(player)
        else:
            print('Invalid number of players to register please register between 1 and {} people'.format(MAX_PLAYERS))

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
                

    def get_player_actor(self, name):
        '''Returns the PlayerActor object associated with the provided name'''
        player = next(player for player in self.gamestate.players if player.name == name)
        return player

    def get_player_actors(self):
        players = [self.get_player_actor(p.name) for p in self.players]
        return players

    def get_player_coords(self):
        players = self.get_player_actors()
        player_coords = [player.pos for player in players]
        return player_coords

    def get_adversary_actor(self, name):
        adversary = next(adv for adv in self.gamestate.adversaries if adv.name == name)
        return adversary
    
    def get_adversary_actors(self):
        advs = [self.get_adversary_actor(adv.name) for adv in self.adversaries]
        return advs

    def get_adversary_coords(self):
        advs = self.get_adversary_actors()
        adv_coords = [adversary.pos for adversary in advs]
        return adv_coords

    

    def register_player(self, player_client):
        if len(self.players) <= MAX_PLAYERS:
            if (isinstance(player_client, Player)):
                self.players.append(player_client)
            else:
                self.players.append(create_local_player(player_client))

    def register_adversaries(self, adversaries):
        '''Create list adversary objects from provided list of adversaries'''
        for adv in adversaries:
            self.adversaries.append(adv)

    def register_adversary_names(self, adversary_ids):
        """Create list of adversary objects using list of adversary ids."""
        for id_ in adversary_ids:
            self.adversaries.append(AdversaryActor(id_))

    def register_adversary(self, adversary_client, actor_type=ZOMBIE):
        if isinstance(adversary_client, Adversary):
            self.adversaries.append(adversary_client)
        else:
             self.adversaries.append(create_local_adversary(adversary_client, actor_type))

    def start_game(self, levels, start_level=0):
        is_list = isinstance(levels, list)
        level = levels[start_level]
        levels.remove(level)
        if self.players:
            player_objs = [p.player_obj for p in self.players]
            adv_objs = [a.adversary_obj for a in self.adversaries]
            gs_info = create_initial_game_state(level, player_objs, adv_objs)
            self.gamestate = GameState(levels, gs_info[0], gs_info[1], current_level=level)
            self.reset_turns()
        else:
            print("Please register at least one player and adversary to start the game.")

    """Players are in gamestate in our implementation and inherently have access to updated gamestate info.
        Therefore updating the gmaestate with the game manager fulfills the requirement to have the game manager update
        the players with any changes in the gamestate."""


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
        # if len(self.player_turns) == 0: self.player_turns = self.__reset_player_turns()

        if len(self.player_turns) == len(self.adv_turns) == 0: self.reset_turns()

        player = next(player for player in self.players if player.name == name)
        is_client = isinstance(player, Player)
        if is_client:
            player.pos = player.player_obj.pos

        if player.name in self.player_turns:
            p_coords = self.get_player_coords()
            a_coords = self.get_adversary_coords()
            player_move = self.rc.validate_player_movement(player, new_pos, self.gamestate.current_level, p_coords, a_coords)
            if player_move[VALID_MOVE] and player_move[INFO].traversable:
                if player_move[EJECT]:
                    # Skip this players turn until the list of ejected players is reset i.e. in a level change
                    self.gamestate.ejected_players.add(name)
                
                self.players.remove(player)
                updated_players = self.get_player_actors()
                adversaries = self.get_adversary_actors()

                if is_client:
                    player.player_obj.pos = new_pos
                    updated_players.append(player.player_obj)
                else:
                    player.pos = new_pos
                    updated_players.append(player)

                self.players.append(player)
                self.gamestate = GameState(self.gamestate.current_level, updated_players, adversaries, self.gamestate.exit_locked)
                self.player_turns.remove(player.name)
                update_players(player, self.players)
            return player_move
            
        return False

    def request_adversary_move(self, name, new_pos):
        if len(self.player_turns) == 0:
            if name in self.adv_turns:
                adversary = next(adversary for adversary in self.adversaries if adversary.name == name)
                is_client = isinstance(adversary, AdversaryActor)
                p_coords = self.get_player_coords()
                adv_coords = self.get_adversary_coords()
                adv_move = self.rc.validate_adversary_movement(adversary, new_pos, self.gamestate.current_level, p_coords, adv_coords)

            if adv_move[VALID_MOVE]:
                self.adversaries.remove(adversary)
                players = self.get_player_actors()
                updated_advs = self.get_adversary_actors()

                if adv_move[EJECT]:
                    player = next(player for player in players if player.pos == new_pos)
                    self.gamestate.ejected_players.add(player.name)

                if is_client:
                    adversary.adversary_obj.pos = new_pos
                    updated_advs.append(adversary.adversary_obj)
                else:
                    adversary.pos = new_pos
                    updated_advs.append(adversary)

                self.adversaries.append(adversary)
                self.gamestate = GameState(self.gamestate.current_level, players, updated_advs, self.gamestate.exit_locked)
                self.adv_turns.remove(adversary.name)
            return adv_move
        else:
         return False

    def apply_player_item_interaction(self, player, item):
        """
        Updates player info based on player move.
        :param new_players_locs: [Coord]
        :param new_players_healths: [int]
        :return:
        """

        state = self.gamestate

        for room in state.current_level.rooms:
            if item in room.items:
                room.items.remove(item)
                for p in self.players:
                    if p.name == player.name:
                        p.inventory.append(item)

        if self.rc.validate_item_interaction(player, item, state):
            #TODO: Check if item was key to unlock exit
            self.gamestate = GameState(state.current_level, self.players,
                                       self.adversaries, self.gamestate.exit_locked)
        else:
            self.players = self.gamestate.players