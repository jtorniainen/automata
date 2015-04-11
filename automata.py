import time
from random import random
import numpy as np
import scipy.ndimage as scn


class Organism():

    """ Organism class. """

    def __init__(self, width, height, color, seed):
        """ Initialize organism. """
        self.cells = np.zeros((height, width), dtype=bool)
        self.width = width
        self.height = height
        x = seed[0]
        y = seed[1]

        self.cells[y, x] = 1
        self.grow = random() * 0.5 + 0.1
        self.attack = random()
        self.color = color
        self.boundary = self.get_boundary()

    def get_boundary(self):
        """ Utility function for calcualting organism borders. """
        return self.cells - scn.morphology.binary_erosion(self.cells > 0)

def get_all_cells2(organisms, width, height):
    """ Get a matrix containing cells from all organisms. """
    cells = np.zeros((height - 1, width - 1), dtype=bool)
    for organism in organisms:
        cells = np.bitwise_and(organism.cells, cells)
    return cells


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


def kill_cell2(organisms, kill_list):
    for organism in organisms:
        organism.cells[kill_list] = 0


def attack(organisms, all_cells):
    """ This is supposed to be a faster attack routine (with scipy). """
    for organism in organisms:
        attack_zone = scn.binary_dilation(organism.cells) - organism.cells
        for cell in np.transpose(attack_zone.nonzero()):
            if all_cells[cell[0], cell[1]] and random() < organism.attack:
                kill_cell(organisms, cell[0], cell[1])
                organism.cells[cell[0], cell[1]] = 1


def attack2(organisms, all_cells):
    """ Thought this would be faster but its not, use attack"""
    all_cells = all_cells > 0
    for organism in organisms:
        attack_zone = scn.binary_dilation(organism.cells) - organism.cells
        attack_zone = np.bitwise_and(attack_zone, all_cells)
        attack_chance = np.zeros(np.shape(attack_zone)) + 2
        attack_chance[attack_zone] = np.random.random(np.sum(attack_zone))
        attacks = attack_chance < organism.attack
        kill_cell2(organisms, attacks)
        organism.cells[attacks] = 1


def die(organisms):
    """ Check for expired cells (currently not in use). """
    for organism in organisms:
        organism.life[organism.life > 0] -= time.time() - organism.last_update
        organism.cells[organism.life < 0] = 0
        organism.life[organism.life < 0] = 0


def check_extinction(organisms):
    """ Remove dead organisms. """
    survivors = []
    for idx in range(len(organisms)):
        if np.sum(organisms[idx].cells):
            survivors.append(organisms[idx])
    return survivors


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


def grow2(organisms, all_cells, template):
    """ Trying to optimize this too. """
    for organism in organisms:
        grow_zone = np.bitwise_and(scn.binary_dilation(organism.cells) -
            organism.cells, template)
        for cell in np.transpose(grow_zone.nonzero()):
            if not all_cells[cell[0], cell[1]] and random() < organism.grow:
                organism.cells[cell[0], cell[1]] = 1
                all_cells[cell[0], cell[1]] = 1
        organism.boundary = organism.get_boundary()
    return all_cells
