from blessings import Terminal
from contextlib import nested
import time
import sys
import random
import numpy as np
import scipy.ndimage as scn


class Organism():

    def __init__(self, width, height, color, seed_x=None, seed_y=None):
        self.cells = np.zeros((height, width))
        self.width = width
        self.height = height
        if seed_x:
            x = seed_x
        else:
            x = random.randint(1, width - 1)
        if seed_y:
            y = seed_y
        else:
            y = random.randint(1, height - 1)

        self.cells[y, x] = 1
        self.grow_chance = random.random() * 0.5 + 0.1
        self.attack = random.random()
        self.color = color
        self.boundary = self.get_boundary()

    def get_boundary(self):
        """ Utility function for calcualting organism borders. """
        return self.cells - scn.morphology.binary_erosion(self.cells > 0)


def draw(organisms, term):
    """ Draws all organisms. """
    for organism in organisms:
        for cell in np.transpose(organism.boundary.nonzero()):
            with term.location(cell[1], cell[0]):
                print organism.color(" ")


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
    """ Remove specified cell. """
    for organism in organisms:
        organism.cells[y, x] = 0


def attack(organisms, all_cells):
    """ All boundary cells attempt to attack one enemy cell (if in range). """
    for organism in organisms:
        cells = all_cells - organism.cells
        for cell in np.transpose(organism.boundary.nonzero()):
            neighbour = get_neighbours(cells < 1, cell[0], cell[1])
            if neighbour and random.random() < organism.attack:
                kill_cell(organisms, neighbour[0], neighbour[1])
                organism.cells[neighbour[0], neighbour[1]] = 1


def attack2(organisms, all_cells):
    """ This is supposed to be a faster attack routine (with scipy). """
    for organism in organisms:
        attack_zone = scn.binary_dilation(organism.cells) - organism.cells
        for cell in np.transpose(attack_zone.nonzero()):
            if all_cells[cell[0], cell[1]] and random.random() < organism.attack:
                kill_cell(organisms, cell[0], cell[1])
                organism.cells[cell[0], cell[1]] = 1

        #organism.boundary = organism.get_boundary()

def die(organisms):
    """ Check for expired cells (currently not in use). """
    for organism in organisms:
        organism.life[organism.life > 0] -= time.time() - organism.last_update
        organism.cells[organism.life < 0] = 0
        organism.life[organism.life < 0] = 0


def update(organisms, all_cells):
    """ Updates each organism (procreate, kill, decay). """

    for organism in organisms:
        for cell in np.transpose(organism.boundary.nonzero()):
            neighbours = get_neighbours(all_cells, cell[0], cell[1])
            if neighbours and random.random() < organism.grow_chance:
                organism.cells[neighbours[0], neighbours[1]] = 1
                all_cells[neighbours[0], neighbours[1]] = 1
        organism.boundary = organism.get_boundary()
    return all_cells


def get_neighbours(cells, y, x):
    """ Utility function for getting neighbouring cells. """
    neighbours = []
    if x > 1 and cells[y, x - 1] == 0:
        neighbours.append((y, x - 1))
    if x < cells.shape[1] - 1 and cells[y, x + 1] == 0:
        neighbours.append((y, x + 1))
    if y > 1 and cells[y - 1, x] == 0:
        neighbours.append((y - 1, x))
    if y < cells.shape[0] - 1 and cells[y + 1, x] == 0:
        neighbours.append(((y + 1, x)))

    if neighbours:
        return random.choice(neighbours)
    else:
        return neighbours


def clear(term, height):
    """Clear the droppings of the given board."""
    for y in xrange(height):
        print term.move(y, 0) + term.clear_eol,


def main(N=4):
    """ Main program loop. """
    term = Terminal()
    specimens = []
    width = term.width
    height = term.height
    colors = [
        term.on_green,
        term.on_red,
        term.on_blue,
        term.on_yellow,
        term.on_white,
        term.on_magenta,
        term.on_cyan]
    for idx in range(N):
        color = random.choice(range(len(colors)))
        specimens.append(
            Organism(
                term.width -
                1,
                term.height -
                1,
                colors[color]))

    all_cells = get_all_cells(specimens, width, height)
    with nested(term.fullscreen(), term.hidden_cursor()):
        while True:
            all_cells = update(specimens, all_cells)
            attack(specimens, all_cells)
            draw(specimens, term)
            sys.stdout.flush()
            clear(term, term.height)
            # die(specimens)
            time.sleep(0.05)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(int(sys.argv[1]))
    else:
        main()
