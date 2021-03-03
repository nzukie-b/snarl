import sys, os, json
import pygame
current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)
from coord import Coord
from model.room import Room
from model.hallway import Hallway
from model.level import Level, GameState, create_initial_game_state
from constants import BLACK, WHITE, YELLOW, GREY, RED, BLUE, HEIGTH, WIDTH, SIZE


SCREEN = pygame.display.set_mode((WIDTH, HEIGTH), 0, 32)
SCREEN.fill(WHITE)
pygame.display.set_caption('Snarl')


class Tile:
    def __init__(self, row, col, wall=True, item=None):
        self.row = row * SIZE
        self.col = col * SIZE
        self.wall = wall 
        self.item = item

    def __str__(self):
        return json.dumps(self.__dict__)        


def render_hallway(hallway, orientation):
    '''Renders tiles for the provided hallway based on the hallway's orientaion, and returns the list of the created tiles.'''
    try :
        x_boundary = hallway.origin.row + hallway.dimensions.row
        y_boundary = hallway.origin.col + hallway.dimensions.col
        tiles = []
        for ii in range(hallway.origin.row, x_boundary + 1):
            for jj in range(hallway.origin.col, y_boundary + 1):
                tile = Tile(ii, jj)
                tiles.append(tile)
                pygame.draw.rect(SCREEN, WHITE, render_tile(tile))
                # Walls aren't defined from the dimensions we assume the provided dimensions are all walkable
                if orientation == False:
                    # Vertical path hallway case
                    left_wall = Tile(hallway.origin.row - 1, jj)
                    right_wall = Tile(x_boundary + 1, jj)
                    pygame.draw.rect(SCREEN, BLACK, render_tile(left_wall))
                    pygame.draw.rect(SCREEN, BLACK, render_tile(right_wall))
                elif orientation == True:
                    # Horizontal path hallway
                    upper_wall = Tile(ii, hallway.origin.col - 1)
                    lower_wall = Tile(ii, y_boundary + 1)
                    pygame.draw.rect(SCREEN, BLACK, render_tile(upper_wall))
                    pygame.draw.rect(SCREEN, BLACK, render_tile(lower_wall))
        return tiles
    except Exception as err :
        print('Error: Attempting to render invalid hallway. Object: ', err)


def render_level(level):
    for hall in level.hallways:
        render_hallway(hall, hall.check_orientation())
    for room in level.rooms:
        render_room(room)

def render_tile(tile):
    '''Returns a rectangle for the provided Tile to be rendered on the view'''
    return pygame.Rect(tile.row, tile.col, SIZE, SIZE)


def render_room(room):
    '''Renders tiles for the provided Room, and returns the list of the created tiles.'''
    tiles = []
    for ii in range(room.origin.row, room.origin.row + room.dimensions.row + 1):
        for jj in range(room.origin.col, room.origin.col + room.dimensions.col + 1):
            coord = Coord(ii, jj)
            tile = Tile(ii, jj)
            tiles.append(tile)
            if coord in room.doors:
                pygame.draw.rect(SCREEN, GREY, render_tile(tile))
            elif coord in room.items:
                pygame.draw.circle(SCREEN, YELLOW, (tile.row + SIZE / 2, tile.col + SIZE / 2), SIZE / 2)
            elif coord in room.tiles:
                pygame.draw.rect(SCREEN, WHITE, render_tile(tile))
            else:
                pygame.draw.rect(SCREEN, BLACK, render_tile(tile))
    return tiles


def render_players(players):
    for player in players:
        pygame.draw.circle(SCREEN, BLUE, (player.pos.row + SIZE / 2, player.pos.col + SIZE / 2), SIZE / 2)


def render_adversaries(adversaries):
    #print(str(adversaries))
    for adversary in adversaries:
        pygame.draw.circle(SCREEN, RED, (adversary.pos.row + SIZE / 2, adversary.pos.col + SIZE / 2), SIZE / 2)


def main():
    pygame.init()
    pygame.display.flip()
    #Room 1 example
    tiles = [Coord(7, 6),Coord(7, 8),Coord(7, 9),Coord(7, 10), Coord(6, 6), Coord(6, 8), Coord(8, 9),
                 Coord(8,6), Coord(8, 7), Coord(8,8), Coord(8, 9), Coord(8, 10), Coord(9, 6), Coord(9, 7), Coord(9,8) ]
    start = Coord(5, 5)
    dimensions = Coord(5, 5)
    doors = [Coord(8,10), Coord(7, 10), Coord(6, 10)]
    items = [Coord(6, 6), Coord(7, 8)]
    room = Room(start, dimensions, tiles, doors, items)
    hall_start = Coord(6, 11)
    hall = Hallway(hall_start, Coord(2, 3), [room])
    #Room 2 example
    tiles1 = [Coord(7, 14), Coord(7, 17), Coord(7, 18), Coord(6, 17), Coord(8, 18), Coord(8, 15), 
                Coord(6, 15), Coord(7, 15), Coord(7, 15), Coord(9, 17), Coord(9, 16), Coord(9, 15), Coord(6, 16)]
    start1 = Coord(5, 14)
    dimensions1 = Coord(5, 5)
    doors1 = [Coord(8, 14), Coord(7, 14), Coord(6, 14)]
    items1 = [Coord(8, 15), Coord(7, 17)]
    room1 = Room(start1, dimensions1, tiles1, doors1, items1)

    gs_info = create_initial_game_state(Level([room, room1], [hall]), 3, 3)
    gamestate = GameState(gs_info[0], gs_info[1])



    while True:
        render_level(Level([room, room1], [hall]))
        render_players(gamestate.players)
        render_adversaries(gamestate.adversaries)
        pygame.display.update()
        #gamestate = update_game_state([], [], [], [], False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

if __name__ == '__main__':
    main()
