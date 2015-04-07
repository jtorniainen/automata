import numpy as np
import pygame
import automata
from random import randint


class Grid(object):

    def __init__(self, width, height, num_x, num_y, screen):
        self.screen = screen
        self.cell_w = width / num_x
        self.cell_h = height / num_y
        self.num_x = num_x
        self.num_y = num_y

    def draw_cell(self, x, y, color):
        x = x * self.cell_w
        y = y * self.cell_h
        pygame.draw.rect(
            self.screen, color, [
                x, y, self.cell_w, self.cell_h])

    def display(self):
        for x in range(self.num_x):
            for y in range(self.num_y):
                self.draw_cell(x, y)


def draw(grid, organism):
    for cell in np.transpose(organism.boundary.nonzero()):
        grid.draw_cell(cell[1], cell[0], organism.color)


def check_extinction(organisms):
    survivors = []
    for idx in range(len(organisms)):
        if np.sum(organisms[idx].cells):
            survivors.append(organisms[idx])
    return survivors


def main():
    # Initialize pygame and grid-object
    width = 800
    height = 600
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    done = False
    finished = False
    n_x = 100
    n_y = 100
    grid = Grid(width, height, n_x, n_y, screen)
    specimens = []
    N = 3
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
        all_cells = automata.update(specimens, all_cells)
        automata.attack(specimens, all_cells)
        for specimen in specimens:
            draw(grid, specimen)
        specimens = check_extinction(specimens)
        if len(specimens) == 1:
            finished = True

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
