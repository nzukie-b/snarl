import sys, os
from typing import Mapping
currentdir = os.path.dirname(os.path.realpath(__file__))
snarl_dir = os.path.dirname(currentdir)
game_dir = snarl_dir + '/src'
sys.path.append(game_dir)
from constants import MAX_PLAYERS
from model.player import Player
from model.adversary import Adversary
from model.gamestate import GameState, create_initial_game_state, update_game_state
from game.ruleChecker import RuleChecker

class GameManager:
    def __init__(self):
        self.players = []
        self.adversaries = []
        self.gamestate = None
        self.rc = RuleChecker()
        self.player_turns = []
        # Names of players that need to go during this turn

    def reset_player_turns(self):
        return [player.name for player in self.players]

    def register_players(self, players):
        '''Create list of players from provided list of players'''
        if 1 < len(players) <= MAX_PLAYERS:
            for player in players:
                self.players.append(player)
        else:
            print('Invalid number of players to register please register between 1 and {} people'.format(MAX_PLAYERS))

    def register_player_names(self, player_names):
        """Create list of player objects using list of player names."""
        if 1 < len(player_names) <= MAX_PLAYERS:
            for name in player_names:
                self.players.append(Player(name))
        else:
            print("Too few or too many players to register, please register between 1 and 4 players.")


    def register_adversaries(self, adversaries):
        '''Create list adversary objects from provided list of adversaries'''
        for adv in adversaries:
            self.adversaries.append(adv)

    def register_adversary_names(self, adversary_ids):
        """Create list of adversary objects using list of adversary ids."""
        for id_ in adversary_ids:
            self.adversaries.append(Adversary(id_))

    def start_game(self, level):
        if self.players:
            gs_info = create_initial_game_state(level, self.players, self.adversaries)
            self.gamestate = GameState(level, gs_info[0], gs_info[1])
            self.player_turns = self.reset_player_turns()
            # self.turn_order = self.players + self.adversaries
            # self.current_turn = self.turn_order[0]
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
            # self.players[i].loc = new_players_locs[i]
            if self.rc.validate_player_movement(self.players[i].pos, new_players_locs[i], self.gamestate.level):
                self.gamestate = GameState(self.gamestate.level, self.players, self.adversaries, self.gamestate.exit_locked)
        else:
            self.players = self.gamestate.players

    def request_player_move(self, name, new_pos):
        #TODO: Add condition for adversary turns as well
        # If all players (adversaries later) have gone this turn cycle, then reset the turn order
        if len(self.player_turns) == 0: self.player_turns = self.reset_player_turns()
        player = next(player for player in self.players if player.name == name)
        if player.name in self.player_turns:
            player_move = self.rc.validate_player_movement(player.pos, new_pos, self.gamestate.level)
            
            if player_move['valid_move'] and player_move['info'].traversable:
                self.players.remove(player)
                player.pos = new_pos
                self.players.append(player)
                self.gamestate = GameState(self.gamestate.level, self.players, self.adversaries, self.gamestate.exit_locked)
                self.player_turns.remove(player.name)
            return player_move
        return None


    def apply_player_item_interaction(self, player, item):
        """
        Updates player info based on player move.
        :param new_players_locs: [Coord]
        :param new_players_healths: [int]
        :return:
        """

        new_level = self.gamestate.level

        for room in new_level.rooms:
            if item in room.items:
                room.items.remove(item)
                for p in self.players:
                    if p.name == player.name:
                        p.inventory.append(item)

        if self.rc.validate_item_interaction(player, item, new_level):
            self.gamestate = GameState(new_level, self.players,
                                       self.gamestate.adversaries, self.gamestate.exit_locked)
        else:
            self.players = self.gamestate.players