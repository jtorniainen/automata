from blessings import Terminal
from contextlib import nested
import time
from sys import stdout
import random
import numpy as np
import scipy.ndimage as scn


class organism():

    def __init__(self, term, color, seed_x=None, seed_y=None):
        self.cells = np.zeros((term.height-1, term.width-1))
        self.life = np.zeros((term.height-1, term.width-1))

        self.width = term.width
        self.height = term.height
        if seed_x:
            x = seed_x
        else:
            x = random.randint(1, term.width-2)
        if seed_y:
            y = seed_y
        else:
            y = random.randint(1, term.height-2)

        self.cells[y, x] = 1
        self.life[y, x] = random.random() * 10
        self.grow_chance = random.random() * 0.5 + 0.1
        self.attack = random.random()
        self.term = term
        self.color = color
        self.last_update = time.time()


def draw2(organisms, term):
    """ Draws all organisms. """
    for organism in organisms:
        #for cell in np.transpose(get_boundary_cells(organism, term).nonzero()):
        for cell in np.transpose(organism.cells.nonzero()):
            with term.location(cell[1], cell[0]):
                print organism.color(" ")


def get_all_cells(organisms, term):
    cells = np.zeros((term.height - 1, term.width - 1))
    for organism in organisms:
        cells += organism.cells
    return cells


def get_boundary_cells(organisms, term):
    if type(organisms) == list:
        cells = np.zeros((term.height - 1, term.width - 1))
        for organism in organisms:
            cells += get_boundary_cells(organism, term)
        cells = cells > 0
    else:
        cells = organisms.cells
    return cells - scn.morphology.binary_erosion(cells > 0)


def fight(organisms, term):
    targets = get_boundary_cells(organism)
    return targets


def kill_cell(organisms, y, x):
    for organism in organisms:
        organism.cells[y, x] = 0


def attack(organisms, term):
    all_cells = get_all_cells(organisms, term)
    for organism in organisms:
        #cells = all_cells - organism.boundary
        #cells = all_cells - get_boundary_cells(organisms, term)
        cells = all_cells - organism.cells
        #for cell in np.transpose(organism.boundary.nonzero()):
        for cell in np.transpose(get_boundary_cells(organism, term).nonzero()):
            neighbour = get_neighbours(cells < 1, cell[0], cell[1])
            if neighbour and random.random() < organism.attack:
                kill_cell(organisms, neighbour[0], neighbour[1])
                organism.cells[neighbour[0], neighbour[1]] = 1


def die(organisms):
    for organism in organisms:
        organism.life[organism.life > 0] -= time.time() - organism.last_update
        organism.cells[organism.life < 0] = 0
        organism.life[organism.life < 0] = 0


def update(organisms, term):
    """ Updates each organism (procreate, kill, decay). """
    cells = get_all_cells(organisms, term)

    for organism in organisms:
        for cell in np.transpose(get_boundary_cells(organism, term).nonzero()):
            neighbours = get_neighbours(cells, cell[0], cell[1])
            if neighbours and random.random() < organism.grow_chance:
                organism.cells[neighbours[0], neighbours[1]] = 1
                # organism.life[neighbours[0], neighbours[1]] = random.random() + 1
                cells[neighbours[0], neighbours[1]] = 1
                organism.last_update = time.time()


def get_neighbours(cells, y, x):
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


def main():
    term = Terminal()
    specimens = []
    N = 7
    colors = [term.on_green, term.on_red, term.on_blue, term.on_yellow, term.on_white, term.on_magenta, term.on_cyan]
    for idx in range(N):
        color = random.choice(range(len(colors)))
        specimens.append(organism(term, colors[color]))
        del colors[color]
    with nested(term.fullscreen(), term.hidden_cursor()):
        while True:
            update(specimens, term)
            draw2(specimens, term)
            # die(specimens)
            attack(specimens, term)
            stdout.flush()
            time.sleep(0.5)
            clear(term, term.height)


def clear(term, height):
    """Clear the droppings of the given board."""
    for y in xrange(height):
        print term.move(y, 0) + term.clear_eol,

if __name__ == "__main__":
    main()
