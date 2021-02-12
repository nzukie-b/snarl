#!/usr/bin/env python

import pygame
WHITE = (255,255,255)
BLACK = (0, 0, 0)
YELLOW = (255, 225, 125)
WIDTH = 700
HEIGTH = 500
SIZE = 5
class Tile:
    def __init__(self, x, y, type=None, items=None):
        self.x = x
        self.y = y
        self.type = type
        self.items = items if items is not None else []

def render_tile(tile):
    return pygame.Rect(tile.x*SIZE, tile.y*SIZE, SIZE, SIZE)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGTH))
    pygame.display.set_caption('Snarl')
    screen.fill(WHITE)
    pygame.display.flip()
    path = Tile(0, 0)
    wall = Tile(0, 1, type='WALL')
    item = Tile(0, 2, item='KEY')
    tiles = [path, wall, item]
    # Need to find out how to display graphical programs on wsl
    while True:
        for tile in tiles:
            if tile.type == 'WALL':
                pygame.draw.rect(screen, BLACK, render_tile(tile))
            else:
                pygame.draw.rect(screen, WHITE, render_tile(tile))
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.update()

if __name__ == '__main__':
    main()
