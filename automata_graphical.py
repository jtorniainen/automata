import numpy as np
import pygame
import automata
from random import randint, choice
import sys


class Grid(object):

    """ Grid-object for drawing cells. """

    def __init__(self, width, height, num_x, num_y, screen):
        """ Grid initializer. """
        self.screen = screen
        self.cell_w = int(np.floor(float(width) / float(num_x)))
        self.cell_h = int(np.floor(float(height) / float(num_y)))
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


def generate_template(width, height, r):
    """ Generates a circular growth area template. """
    template = np.ones((height, width), dtype=bool)
    center = np.array((height / 2.0, width / 2.0))
    for cell in np.transpose(template.nonzero()):
        dist = np.linalg.norm(cell - center)
        if dist > r:
            template[cell[0], cell[1]] = False
    return template


def main(N=10):
    """ Main-loop. """
    # Initialize pygame
    width = 1360
    height = 768
    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    # Initialize drawing area
    done = False
    n_x = 100
    n_y = 100
    grid = Grid(width, height, n_x, n_y, screen)

    # Initialize specimens
    specimens = []
    template = generate_template(n_x - 1, n_y - 1, 50)
    for x in range(N):
        color = (randint(10, 255), randint(10, 255), randint(10, 255))
        seed = choice(np.transpose(template.nonzero()))
        specimens.append(automata.Organism(n_x - 1, n_y - 1, color, seed=seed))
    all_cells = automata.get_all_cells(specimens, n_x, n_y)

    # Start main-loop
    while not done:

        # Deal with events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        # Update specimens
        all_cells = automata.grow2(specimens, all_cells, template)
        automata.attack(specimens, all_cells)
        specimens = automata.check_extinction(specimens)

        # Draw cells
        screen.fill((10, 0, 0))
        for specimen in specimens:
            draw(grid, specimen)
        if len(specimens) == 1:
            pass
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(N=int(sys.argv[1]))
    else:
        main()
