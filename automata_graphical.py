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
        self.cell_w = int(round(float(width) / float(num_x)))
        self.cell_h = int(round(float(height) / float(num_y)))
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


def generate_template(width, height, r):
    template = np.ones((height, width), dtype=bool)
    for cell in np.transpose(template.nonzero()):
        r_tmp = r + randint(-2,2)
        if np.sqrt(pow(cell[0]-height / 2.0, 2) + pow(cell[1] - width / 2.0, 2)) > r_tmp:
            template[cell[0], cell[1]] = False
    return template


def main(N=10):
    """ Main-loop. """
    width = 1360
    height = 768
    pygame.init()

    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    done = False
    #n_x = 100
    #n_y = 100
    n_x = 200
    n_y = 200
    grid = Grid(width, height, n_x, n_y, screen)
    specimens = []
    template = generate_template(n_x - 1, n_y - 1, 80)
    for x in range(N):
        color = (randint(10, 255), randint(10, 255), randint(10, 255))
        seed = choice(np.transpose(template.nonzero()))
        specimens.append(automata.Organism(n_x - 1, n_y - 1, color, seed_xy=seed))
    all_cells = automata.get_all_cells(specimens, n_x, n_y)
    while not done:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
        screen.fill((10, 0, 0))
        all_cells = automata.grow2(specimens, all_cells, template)
        automata.attack(specimens, all_cells)
        #automata.attack2(specimens, all_cells)
        for specimen in specimens:
            draw(grid, specimen)
        specimens = check_extinction(specimens)
        if len(specimens) == 1:
            pass

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(N=int(sys.argv[1]))
    else:
        main()
