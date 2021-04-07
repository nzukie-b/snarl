import sys, os, json
import pygame

current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)
from utilities import check_position
from coord import Coord
from model.room import Room
from model.hallway import Hallway
from model.level import Level
from model.gamestate import GameState, create_initial_game_state
from controller.controller import parse_state
from constants import BLACK, WHITE, YELLOW, GREY, RED, BLUE, GREEN, PURPLE, HEIGTH, WIDTH, SIZE


SCREEN = pygame.display.set_mode((WIDTH, HEIGTH), 0, 32)
SCREEN.fill(GREY)
pygame.display.set_caption('Snarl')


class Tile:
    def __init__(self, row, col, wall=True, item=None):
        self.x = col * SIZE
        self.y = row * SIZE
        self.wall = wall 
        self.item = item

    def __str__(self):
        return json.dumps(self.__dict__)        


def render_hallway(hallway, orientation):
    '''Renders tiles for the provided hallway based on the hallway's orientaion, and returns the list of the created tiles.'''
    try :
        row_start = hallway.origin.row
        col_start = hallway.origin.col
        row_end = hallway.origin.row + hallway.dimensions.row
        col_end = hallway.origin.col + hallway.dimensions.col
        tiles = []
        for ii in range(row_start, row_end + 1):
            for jj in range(col_start, col_end + 1):
                coord = Coord(ii, jj)
                if hallway.in_hallway(coord):
                    tile = Tile(ii, jj)
                    tiles.append(tile)
                    pygame.draw.rect(SCREEN, WHITE, render_square(tile))
                    # Walls aren't defined from the dimensions we assume the provided dimensions are all walkable
                    # if orientation == False:
                        # Vertical path hallway case
                    left_wall = Tile(row_start - 1, jj)
                    right_wall = Tile(row_end + 1, jj)
                    top_wall = Tile(ii, col_start - 1)
                    bot_wall = Tile(ii, col_end + 1 )
                    pygame.draw.rect(SCREEN, BLACK, render_square(top_wall))
                    pygame.draw.rect(SCREEN, BLACK, render_square(bot_wall))
                    pygame.draw.rect(SCREEN, BLACK, render_square(left_wall))
                    pygame.draw.rect(SCREEN, BLACK, render_square(right_wall))
                    # elif orientation == True:
                    #     # Horizontal path hallway
                    #     upper_wall = Tile(ii, col_start - 1)
                    #     lower_wall = Tile(ii, col_end + 1)
                    #     pygame.draw.rect(SCREEN, BLACK, render_square(upper_wall))
                    #     pygame.draw.rect(SCREEN, BLACK, render_square(lower_wall))
        for waypoint in hallway.waypoints:
            tile = Tile(waypoint.row, waypoint.col)
            pygame.draw.rect(SCREEN, PURPLE, render_square(tile))
        for door in hallway.doors:
            tile = Tile(door.row, door.col)
            pygame.draw.rect(SCREEN, GREY, render_square(tile))
        return tiles
    except Exception as err :
        print('Error: Attempting to render invalid hallway. Object: ', err)


def render_level(level):
    for hall in level.hallways:
        render_hallway(hall, hall.check_orientation())
    for room in level.rooms:
        render_room(room)
    for e in level.exits:
        pos = e.pos
        tile = Tile(pos.row, pos.col)
        pygame.draw.rect(SCREEN, GREEN, render_square(tile) )

def render_square(tile):
    '''Returns a rectangle for the provided Tile to be rendered on the view'''
    return pygame.Rect(tile.x, tile.y, SIZE, SIZE)

def render_circle(tile):
    return (tile.x + SIZE / 2, tile.y + SIZE / 2)

def render_room(room):
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
                pygame.draw.rect(SCREEN, GREY, render_square(tile))
            elif coord in room.tiles:
                pygame.draw.rect(SCREEN, WHITE, render_square(tile))
            elif coord in item_coords:
                pygame.draw.circle(SCREEN, YELLOW, render_circle(tile), SIZE / 2)
            else:
                pygame.draw.rect(SCREEN, BLACK, render_square(tile))
    return tiles


def render_players(players):
    for player in players:
        tile = Tile(player.pos.row, player.pos.col)
        pygame.draw.circle(SCREEN, BLUE, render_circle(tile), SIZE / 2)


def render_adversaries(adversaries):
    for adversary in adversaries:
        tile = Tile(adversary.pos.row, adversary.pos.col)
        pygame.draw.circle(SCREEN, RED, render_circle(tile), SIZE / 2)


def main(state: GameState):
    pygame.init()
    pygame.display.flip()
    while True:
        render_level(state.current_level)
        render_players(state.players)
        render_adversaries(state.adversaries)
        pygame.display.update()
        #gamestate = update_game_state([], [], [], [], False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

if __name__ == '__main__':
    state_input = sys.stdin.read().strip()
    parsed_input = parse_state(state_input)
    state = parsed_input['state']
    name = parsed_input['name']
    coord = parsed_input['coord']
    # gs_info =state.create_initial_game_state
    main(state)

    main()
