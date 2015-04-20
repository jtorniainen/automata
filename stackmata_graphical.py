import numpy as np
import pygame
from random import randint
import sys
import stackmata


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


def draw(grid, culture):
    """ Draw organisms. """
    for c in range(culture.boundary.shape[-1]):
        for cell in np.transpose(culture.boundary[..., c].nonzero()):
            grid.fill_cell(cell[1], cell[0], culture.color[c])


def main(N=10):
    """ Main-loop. """
    # Initialize pygame
    width = 768
    height = 768
    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    done = False

    # Initialize drawing area
    SIZE = 4
    grid = Grid(width, height, SIZE, SIZE, screen)

    culture = stackmata.Culture(SIZE, SIZE)
    for x in range(N):
        culture.add_organism((randint(0, SIZE - 1), randint(0, SIZE - 1)))

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
        screen.fill((0, 0, 0))

        # Update specimens
        culture.growth()
        culture.fight()
        culture.decay()
        # Draw cells
        draw(grid, culture)

        pygame.display.flip()
        clock.tick(1)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(N=int(sys.argv[1]))
    else:
        main()
