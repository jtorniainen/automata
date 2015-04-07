import time
from random import random, randint
import numpy as np
import scipy.ndimage as scn


class Organism():
    """ Organism class. """

    def __init__(self, width, height, color, seed_x=None, seed_y=None):
        """ Initialize organism. """
        self.cells = np.zeros((height, width))
        self.width = width
        self.height = height
        if seed_x:
            x = seed_x
        else:
            x = randint(1, width - 1)
        if seed_y:
            y = seed_y
        else:
            y = randint(1, height - 1)

        self.cells[y, x] = 1
        self.grow = random() * 0.5 + 0.1
        self.attack = random()
        self.color = color
        self.boundary = self.get_boundary()

    def get_boundary(self):
        """ Utility function for calcualting organism borders. """
        return self.cells - scn.morphology.binary_erosion(self.cells > 0)


def get_all_cells(organisms, width, height):
    """ Get a matrix containing cells from all organisms. """
    cells = np.zeros((height - 1, width - 1))
    for organism in organisms:
        cells += organism.cells
    return cells


def get_all_boundary_cells(organisms, width, height):
    """ Get matrix of boundary cells of all organisms. """
    boundary_cells = np.zeros((height - 1, width - 1))
    for organism in organisms:
        boundary_cells += organism.boundary


def kill_cell(organisms, y, x):
    """ Purge specified cell. """
    for organism in organisms:
        organism.cells[y, x] = 0


def attack(organisms, all_cells):
    """ This is supposed to be a faster attack routine (with scipy). """
    for organism in organisms:
        attack_zone = scn.binary_dilation(organism.cells) - organism.cells
        for cell in np.transpose(attack_zone.nonzero()):
            if all_cells[cell[0], cell[1]] and random() < organism.attack:
                kill_cell(organisms, cell[0], cell[1])
                organism.cells[cell[0], cell[1]] = 1


def die(organisms):
    """ Check for expired cells (currently not in use). """
    for organism in organisms:
        organism.life[organism.life > 0] -= time.time() - organism.last_update
        organism.cells[organism.life < 0] = 0
        organism.life[organism.life < 0] = 0


def grow(organisms, all_cells):
    """ Trying to optimize this too. """
    for organism in organisms:
        grow_zone = scn.binary_dilation(organism.cells) - organism.cells
        for cell in np.transpose(grow_zone.nonzero()):
            if not all_cells[cell[0], cell[1]] and random() < organism.grow:
                organism.cells[cell[0], cell[1]] = 1
                all_cells[cell[0], cell[1]] = 1
        organism.boundary = organism.get_boundary()
    return all_cells
