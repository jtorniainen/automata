import numpy as np
import pygame
import automata
from random import randint
import sys


class Grid(object):

    """ Grid-object for drawing cells. """

    def __init__(self, width, height, num_x, num_y, screen):
        """ Grid initializer. """
        self.screen = screen
        self.cell_w = width / num_x
        self.cell_h = height / num_y
        self.num_x = num_x
        self.num_y = num_y

    def fill_cell(self, x, y, color):
        """ Draw cell at x,y with specified color. """
        x = x * self.cell_w
        y = y * self.cell_h
        self.screen.fill(color, rect=(x, y, self.cell_w, self.cell_h))


def draw(grid, organism):
    """ Draw organisms. """
    for cell in np.transpose(organism.boundary.nonzero()):
        grid.fill_cell(cell[1], cell[0], organism.color)


def check_extinction(organisms):
    """ Remove dead organisms. """
    survivors = []
    for idx in range(len(organisms)):
        if np.sum(organisms[idx].cells):
            survivors.append(organisms[idx])
    return survivors


def main(N=10):
    """ Main-loop. """
    width = 800
    height = 600
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    done = False
    n_x = 100
    n_y = 100
    grid = Grid(width, height, n_x, n_y, screen)
    specimens = []
    for x in range(N):
        color = (randint(10, 255), randint(10, 255), randint(10, 255))
        specimens.append(automata.Organism(n_x - 1, n_y - 1, color))
    all_cells = automata.get_all_cells(specimens, n_x, n_y)
    while not done:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                done = True
        screen.fill((0, 0, 0))
        all_cells = automata.grow(specimens, all_cells)
        automata.attack(specimens, all_cells)
        for specimen in specimens:
            draw(grid, specimen)
        specimens = check_extinction(specimens)
        if len(specimens) == 1:
            pass

        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(N=int(sys.argv[1]))
    else:
        main()
