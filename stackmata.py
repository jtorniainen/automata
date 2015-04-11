import numpy as np
import scipy.ndimage as nd
import random


class Culture():
    """ This is like a container for multiple organisms. Uses a stack instead
        of multiple objects. Maybe faster who knows.
    """
    def __init__(self, width, height):
        self.cells = []
        self.width = width
        self.height = height
        self.grow = []
        self.attack = []
        self.color = []
        self.empty = True

    def add_organism(self, seed):
        """ Add new organism to the stack """
        new_cells = np.zeros((self.height, self.width), dtype=bool)
        new_cells[seed[1], seed[0]] = True

        if self.empty:
            self.cells = new_cells
            self.empty = False
        else:
            self.cells = np.dstack((self.cells, new_cells))

        self.grow.append(random.random())
        self.attack.append(random.random())
        self.color.append((random.random(), random.random(), random.random()))
