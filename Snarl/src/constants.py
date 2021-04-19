#!/usr/bin/env python

### VIEW CONSTANTS ###
WHITE = (255,255,255)
BLACK = (0, 0, 0)
GREY = (125, 125, 125)
YELLOW = (255, 225, 125)
GREEN = (225, 255, 125)
PURPLE = (225, 125, 225)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WIDTH = 700
HEIGTH = 500
SIZE = 25

### GAME CONSTANTS ###
MAX_PLAYERS = 4


### NAME CONSTANTS ##
ITEM = 'item'
KEY = 'key'
EXIT = 'exit'
WELCOME = 'welcome'
START_LVL = 'start-level'
CONN = 'connection'
OK = 'ok'


COORD = 'coord'
ROOM = "room"
HALLWAY = "hallway"
LEVEL = 'level'
STATE = 'state'
MANAGER = 'manager'
MAX_TURNS = 'max-turns'
MOVES = 'moves'
INFO = 'info'
VALID_MOVE = 'valid-move'
P_UPDATE = 'player-update'
P_SCORE = 'player-score'
GAME_END = 'game-end'
LEVEL_END = 'level-end'
STATUS = 'game-status'
INVALID = 'invalid'
END_LEVEL = 'end-level'
END_GAME = 'end-game'
RES = 'result'
EJECT = 'eject'

### ADVERSARY TYPES ###
GHOST = 'ghost'
ZOMBIE = 'zombie'
G_ATK = 34
Z_ATK = 50
P_ATK = 50
# How far they can see, i.e. must move to player if in range
Z_RNG = 5
G_RNG = 9


### TYPES OF GAME STATE ##
START = 'game-start'
P_WIN = 'player-win'
A_WIN = 'adversary-win'


### JSON KEYS ###
EXIT_LOCKED = 'exit-locked'
PLAYER = 'player'
PLAYERS = 'players'
ADVERSARIES = 'adversaries'
ORIGIN = 'origin'
LAYOUT = 'layout'
TYPE = 'type'
POS = 'position'
NAME = 'name'
FROM = 'from'
TO = 'to'

ROOMS = 'rooms'
HALLWAYS = 'hallways'
WAYPOINTS = 'waypoints'
OBJECTS = 'objects'
BOUNDS = 'bounds'
ROWS = 'rows'
COLS = 'columns'
