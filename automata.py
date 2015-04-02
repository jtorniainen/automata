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
        self.grow_chance = random.random() * 0.5 + 0.1
        self.term = term
        self.color = color


def draw(organisms, term):
    """ Draws all organisms. """
    cells = np.zeros((term.height - 1, term.width - 1))
    # compress cell-matrices
    for idx in range(len(organisms)):
        cells += (organisms[idx].cells * (idx + 1))

    # draw compressed matrix
    for y in range(cells.shape[0]):
        for x in range(cells.shape[1]):
            with term.location(x, y):
                if cells[y, x] and cells[y, x] < len(organisms) + 1:
                    # print int(cells[y, x])
                    print organisms[int(cells[y, x]) - 1].color(" ")
                else:
                    print term.on_black(' ')


def draw2(organisms, term):
    """ Draws all organisms. """
    cells = np.zeros((term.height - 1, term.width - 1))
    # compress cell-matrices
    for idx in range(len(organisms)):
        tmp = organisms[
            idx].cells - scn.morphology.binary_erosion(organisms[idx].cells > 0)
        cells += (tmp * (idx + 1))

    # draw compressed matrix
    for y in range(cells.shape[0]):
        for x in range(cells.shape[1]):
            with term.location(x, y):
                if cells[y, x] and cells[y, x] < len(organisms) + 1:
                    # print int(cells[y, x])
                    print organisms[int(cells[y, x]) - 1].color(" ")
                else:
                    print term.on_black(" ")


def get_all_cells(organisms, term):
    cells = np.zeros((term.height - 1, term.width - 1))
    for organism in organisms:
        cells += organism.cells
    return cells


def get_boundary_cells(organism):
    return organism.cells - scn.morphology.binary_erosion(organism.cells > 0)


def fight(organisms, term):
    targets = get_boundary_cells(organism)
    return targets

def update(organisms, term):
    """ Updates each organism (procreate, kill, decay). """
    cells = np.zeros((term.height - 1, term.width - 1))
    for organism in organisms:
        cells += organism.cells

    for organism in organisms:
        for y in range(cells.shape[0]):
            for x in range(cells.shape[1]):
                if organism.cells[y, x]:
                    neighbours = get_neighbours(cells, y, x)
                    if neighbours and random.random() < organism.grow_chance:
                        organism.cells[neighbours[0], neighbours[1]] = 1
                        cells[neighbours[0], neighbours[1]] = 1

def update2(organisms, term):
    """ Updates each organism (procreate, kill, decay). """
    cells = np.zeros((term.height - 1, term.width - 1))

    for organism in organisms:
        cells += get_boundary_cells(organism)

    for organism in organisms:
        for cell in np.transpose(get_boundary_cells(organism).nonzero()):
            neighbours = get_neighbours(cells, cell[0], cell[1])
            if neighbours:
                organism.cells[neighbours[0], neighbours[1]] = 1
                cells[neighbours[0], neighbours[1]] = 1

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
    N = 4
    colors = [term.on_green, term.on_red, term.on_blue, term.on_yellow]
    for idx in range(N):
        color = random.choice(range(len(colors)))
        specimens.append(organism(term, colors[color]))
        del colors[color]
    with nested(term.fullscreen(), term.hidden_cursor()):
        while True:
            update2(specimens, term)
            draw2(specimens, term)
            stdout.flush()
            time.sleep(0.1)
            #clear(term, height)


def clear(term, height):
    """Clear the droppings of the given board."""
    for y in xrange(height):
        print term.move(y, 0) + term.clear_eol,

if __name__ == "__main__":
    main()
