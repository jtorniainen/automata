import numpy as np
import scipy.ndimage as nd
import random
import time


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
        self.all_cells = np.zeros((self.height, self.width), dtype=bool)
        self.life = []
        self.template = self.generate_template(64)

    def add_organism(self, seed):
        """ Add new organism to the stack """
        new_cells = np.zeros((self.height, self.width), dtype=bool)
        new_cells[seed[1], seed[0]] = True

        if self.empty:
            self.cells = new_cells
            self.boundary = new_cells
            self.all_cells = new_cells
            self.empty = False
        else:
            self.cells = np.dstack((self.cells, new_cells))
            self.boundary = np.dstack((self.boundary, new_cells))
            self.all_cells = np.sum(self.cells, axis=2)

        # Add parameters for new organism
        self.grow.append(random.random() * .5)
        self.attack.append(random.random())
        self.color.append((random.randint(0, 50),
                           random.randint(0, 255),
                           random.randint(0, 50)))

    def generate_template(self, radius):
        """ Generates a circular template to determine valid growing areas. """
        template = np.zeros((self.height, self.width), dtype=bool)
        cx, cy = self.width / 2, self.height / 2  # The center of circle
        y, x = np.ogrid[-radius: radius, -radius: radius]
        index = x**2 + y**2 <= radius**2
        template[cy-radius:cy + radius, cx-radius:cx + radius][index] = True
        return template

    def update_all_cells(self):
        """ Get mask of all current cells. """
        self.all_cells = np.sum(self.cells, axis=2)

    def get_boundary(self, cells):
        """ Returns boundary cells of the input matrix. """
        return cells - nd.binary_erosion(cells)

    def clear_cells(self, array):
        for c in range(self.cells.shape[-1]):
            self.cells[..., c] = self.cells[..., c] * np.invert(array)

    def growth(self):
        """ Grows each organism according to grow chance and template. """
        for c in range(self.boundary.shape[-1]):
            area = np.bitwise_and(
                nd.binary_dilation(self.cells[..., c]) - self.cells[..., c],
                np.invert(self.all_cells)) * self.template
            area[area > 0] = np.random.random(np.sum(area)) < self.grow[c]
            self.cells[..., c] += area
            self.boundary[..., c] = (self.cells[..., c] -
                                     nd.binary_erosion(self.cells[..., c]))
            self.all_cells = np.bitwise_or(self.all_cells,
                                           self.boundary[..., c])

    def decay(self):
        """ Removes expired cells. """
        self.life -= (time.time() - self.last_update)
        self.clear_cells(np.sum(self.life < 0, axis=2))
        self.update_all_cells()

    def fight(self):
        for c in range(self.cells.shape[-1]):
            area = np.bitwise_and(nd.binary_dilation(self.cells[..., c]) -
                                  self.cells[..., c],
                                  self.all_cells - self.cells[..., c])
            area[area > 0] = np.random.random(np.sum(area)) < self.attack[c]
            self.clear_cells(area.astype(bool))
            self.cells[..., c] += area
            self.boundary[..., c] = (self.cells[..., c] -
                                     nd.binary_erosion(self.cells[..., c]))
