import sys, os, json
from typing import List
import pygame
current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)
from model.player import PlayerActor
from model.adversary import AdversaryActor
from coord import Coord
from model.room import Room
from model.hallway import Hallway
from model.level import Level
from model.gamestate import GameState
from constants import BLACK, EXIT, HALLWAY, KEY, LAYOUT, POS, ROOM, TYPE, WHITE, YELLOW, GREY, RED, BLUE, GREEN, PURPLE, HEIGTH, WIDTH, SIZE




class Tile:
    def __init__(self, row, col, wall=True, item=None):
        self.x = col * SIZE
        self.y = row * SIZE
        self.wall = wall 
        self.item = item

    def __str__(self):
        return json.dumps(self.__dict__)        


def render_hallway(hallway: Hallway, orientation, screen):
    '''Renders tiles for the provided hallway based on the hallway's orientaion, and returns the list of the created tiles.'''
    try :
        row_start = hallway.origin.row
        col_start = hallway.origin.col
        row_end = hallway.origin.row + hallway.dimensions.row
        col_end = hallway.origin.col + hallway.dimensions.col
        tiles = []
        for ii in range(row_start, row_end + 1):
            for jj in range(col_start, col_end + 1):
                tile = Tile(ii, jj)
                tiles.append(tile)
                pygame.draw.rect(screen, WHITE, render_square(tile))
                # Walls aren't defined from the dimensions we assume the provided dimensions are all walkable
                # TODO: Decide wether or not to include tile at end or walls
                # if orientation == False:
                    # Vertical path hallway case
                left_wall = Tile(row_start - 1, jj)
                right_wall = Tile(row_end + 1, jj)
                top_wall = Tile(ii, col_start - 1)
                bot_wall = Tile(ii, col_end + 1 )
                pygame.draw.rect(screen, BLACK, render_square(top_wall))
                pygame.draw.rect(screen, BLACK, render_square(bot_wall))
                pygame.draw.rect(screen, BLACK, render_square(left_wall))
                pygame.draw.rect(screen, BLACK, render_square(right_wall))
                    # elif orientation == True:
                    #     # Horizontal path hallway
                    #     upper_wall = Tile(ii, col_start - 1)
                    #     lower_wall = Tile(ii, col_end + 1)
                    #     pygame.draw.rect(SCREEN, BLACK, render_square(upper_wall))
                    #     pygame.draw.rect(SCREEN, BLACK, render_square(lower_wall))
        for waypoint in hallway.waypoints:
            tile = Tile(waypoint.row, waypoint.col)
            pygame.draw.rect(screen, PURPLE, render_square(tile))
        for door in hallway.doors:
            tile = Tile(door.row, door.col)
            pygame.draw.rect(screen, GREY, render_square(tile))
        return tiles
    except Exception as err :
        print('Error: Attempting to render invalid hallway. Object: ', err)


def render_level(level: Level, screen):
    for hall in level.hallways:
        render_hallway(hall, hall.check_orientation(), screen)
    for room in level.rooms:
        render_room(room, screen)
    for e in level.exits:
        pos = e.pos
        tile = Tile(pos.row, pos.col)
        pygame.draw.rect(screen, GREEN, render_square(tile))

def render_square(tile):
    '''Returns a rectangle for the provided Tile to be rendered on the view'''
    return pygame.Rect(tile.x, tile.y, SIZE, SIZE)

def render_circle(tile):
    return (tile.x + SIZE / 2, tile.y + SIZE / 2)

def render_room(room: Room, screen):
    '''Renders tiles for the provided Room, and returns the list of the created tiles.'''
    tiles = []
    row_start = room.origin.row
    col_start = room.origin.col
    row_end = room.origin.row + room.dimensions.row
    col_end = room.origin.col + room.dimensions.col
    item_coords = [item.pos for item in room.items]
    for ii in range(row_start, row_end + 1):
        for jj in range(col_start, col_end + 1):
            coord = Coord(ii, jj)
            tile = Tile(ii, jj)
            tiles.append(tile)
            if coord in room.doors:
                pygame.draw.rect(screen, GREY, render_square(tile))
            elif coord in room.tiles:
                pygame.draw.rect(screen, WHITE, render_square(tile))
            elif coord in item_coords:
                pygame.draw.circle(screen, YELLOW, render_circle(tile), SIZE / 2)
            else:
                pygame.draw.rect(screen, BLACK, render_square(tile))
    return tiles

def render_players(players: List[PlayerActor], screen):
    for player in players:
        tile = Tile(player.pos.row, player.pos.col)
        pygame.draw.circle(screen, BLUE, render_circle(tile), SIZE / 2)

def render_adversaries(adversaries: List[AdversaryActor], screen):
    for adversary in adversaries:
        tile = Tile(adversary.pos.row, adversary.pos.col)
        pygame.draw.circle(screen, RED, render_circle(tile), SIZE / 2)

def render_player_view(player: PlayerActor, state: GameState, screen):
    level = state.current_level
    view_distance = (2 * player.move_speed) + 1
    coords = set()
    for ii in range(view_distance):
        for jj in range(view_distance):
            coords.add(Coord(ii, jj))
    coords = list(coords)
    for coord in coords:
        tile = Tile(coord.row, coord.col)
        info = level.get_info_at_coord()
        if info.object == KEY:
            pygame.draw.circle(screen, YELLOW, render_circle(tile), SIZE / 2)
        elif info.object == EXIT:
            pygame.draw.circle(screen, GREEN, render_square(tile))
        elif info.traversable:
            pygame.draw.rect(screen, WHITE, render_square(tile))
        else:
            pygame.draw.rect(screen, BLACK, render_square(tile))

def render_state(state: GameState):
    pygame.init()
    SCREEN = pygame.display.set_mode((WIDTH, HEIGTH), 0, 32)
    SCREEN.fill(GREY)
    pygame.display.set_caption('Snarl')
    while True:
        render_level(state.current_level, screen=SCREEN)
        render_players(state.players, screen=SCREEN)
        render_adversaries(state.adversaries, screen=SCREEN)
        #gamestate = update_game_state([], [], [], [], False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.flip()
        break

