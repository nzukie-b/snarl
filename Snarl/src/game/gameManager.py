import sys, os
from common import adversary, player
from common.actorUpdate import ActorUpdate
from coord import Coord
currentdir = os.path.dirname(os.path.realpath(__file__))
snarl_dir = os.path.dirname(currentdir)
game_dir = snarl_dir + '/src'
sys.path.append(game_dir)
from constants import INFO, MAX_PLAYERS, VALID_MOVE
from common.player import Player
from player.localPlayer import LocalPlayer
from model.player import PlayerActor
from model.adversary import AdversaryActor
from model.gamestate import GameState, create_initial_game_state
from game.ruleChecker import RuleChecker
from utilities import create_local_player, update_players
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
        return [player.name for player in self.players]

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

    def get_adversary_actor(self, name):
        adversary = next(adv for adv in self.gamestate.adversaries if adv.name == name)
        return adversary

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

    def start_game(self, level):
        if self.players:
            gs_info = create_initial_game_state(level, self.players, self.adversaries)
            self.gamestate = GameState(level, gs_info[0], gs_info[1])
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
            if self.rc.validate_player_movement(self.players[i].pos, new_players_locs[i], self.gamestate.level):
                self.gamestate = GameState(self.gamestate.level, self.players, self.adversaries, self.gamestate.exit_locked)
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
            player_move = self.rc.validate_player_movement(player.pos, new_pos, self.gamestate.level)
            #TODO: MAKE RC CHECK IF PLAYER POS == ADVERSARY POS TO EJECT THEM FROM THE STATE
            if player_move[VALID_MOVE] and player_move[INFO].traversable:
                self.players.remove(player)

                if is_client:
                    other_players = [player.player_obj for player in self.players]
                    player.player_obj.pos = new_pos
                    other_players.append(player.player_obj)
                    updated_players = other_players
                else:
                    other_players = [player for player in self.players]
                    player.pos = new_pos
                    other_players.append(player)
                    update_players = other_players

                self.players.append(player)
                self.gamestate = GameState(self.gamestate.level, other_players, self.gamestate.adversaries, self.gamestate.exit_locked)
                self.player_turns.remove(player.name)
                update_players(player, other_players)
            return player_move
            
        return False

    def request_adversary_move(self, name, new_pos):
        if len(self.player_turns) == 0:
            if name in self.adv_turns:
                adversary = next(adversary for adversary in self.adversaries if adversary.name == name)
                p_coords = self.get_player_coords()
                adv_coords = self.get_adversary_coords()
                adv_move = self.rc.validate_adversary_movement(adversary, new_pos, self.gamestate.level, p_coords, adv_coords)

            if adv_move:
                self.adversaries.remove(adversary)

                is_client = isinstance(adversary, AdversaryActor)
                if is_client:
                    other_advs = [adv.adversary_obj for adv in self.adversaries]
                    adversary.adversary_obj.pos = new_pos
                    other_advs.append(adversary.adversary_obj)
                    updated_advs = other_advs
                else:
                    other_advs = [adv for adv in self.adversaries]
                    adversary.pos = new_pos
                    other_advs.append(adversary)
                    updated_advs = other_advs


                self.adversaries.append(adversary)
                #TODO: MAKE RC CHECK IF PLAYER POS == ADVERSARY POS TO EJECT THEM FROM THE STATE
                self.gamestate = GameState(self.gamestate.level, self.gamestate.players, updated_advs, self.gamestate.exit_locked)
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

        for room in state.level.rooms:
            if item in room.items:
                room.items.remove(item)
                for p in self.players:
                    if p.name == player.name:
                        p.inventory.append(item)

        if self.rc.validate_item_interaction(player, item, state):
            #TODO: Check if item was key to unlock exit
            self.gamestate = GameState(state.level, self.players,
                                       self.adversaries, self.gamestate.exit_locked)
        else:
            self.players = self.gamestate.players