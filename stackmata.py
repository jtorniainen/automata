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
        self.new_color = []
        self.empty = True
        self.all_cells = np.zeros((self.height, self.width), dtype=bool)
        self.life = []
        self.template = self.generate_template(width/2)
        self.last_update = time.time()
        self.centers = []

    def add_organism(self, seed):
        """ Add new organism to the stack """
        new_cells = np.zeros((self.height, self.width), dtype=bool)
        new_cells[seed[1], seed[0]] = True

        if self.empty:
            self.cells = new_cells
            self.boundary = new_cells
            self.all_cells = new_cells
            self.empty = False
            self.life = new_cells.astype(float) * 1000
        else:
            self.cells = np.dstack((self.cells, new_cells))
            self.boundary = np.dstack((self.boundary, new_cells))
            self.life = np.dstack((self.life, new_cells.astype(float) * 5))
            self.all_cells = np.sum(self.cells, axis=2)

        # Add parameters for new organism
        self.centers.append((seed[1], seed[0]))
        self.grow.append(random.random() * .15 + 0.05)
        self.attack.append(random.random() * .2)
        self.color.append((random.randint(0, 255),
                           random.randint(0, 255),
                           random.randint(0, 255)))
        self.new_color.append(random.random())

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
        self.last_update = time.time()
        for c in range(self.boundary.shape[-1]):
            area = np.bitwise_and(
                nd.binary_dilation(self.cells[..., c]) - self.cells[..., c],
                np.invert(self.all_cells)) * self.template
            area[area > 0] = np.random.random(np.sum(area)) < self.grow[c]
            self.cells[..., c] += area
            new_life = self.calculate_life(self.cells[..., c], area, 1)
            self.life[..., c] += new_life
            self.boundary[..., c] = (self.cells[..., c] -
                                     nd.binary_erosion(self.cells[..., c]))
            self.all_cells = np.bitwise_or(self.all_cells,
                                           self.boundary[..., c])

    def decay(self):
        """ Removes expired cells. """
        self.life[self.cells] -= (time.time() - self.last_update)
        self.clear_cells(np.sum(self.life < 0, axis=2) > 0)
        self.update_all_cells()
        self.life[self.life < 0] = 0
        self.last_update = time.time()

    def fight(self):
        for c in range(self.cells.shape[-1]):
            area = np.bitwise_and(nd.binary_dilation(self.cells[..., c]) -
                                  self.cells[..., c],
                                  self.all_cells - self.cells[..., c])
            area[area > 0] = np.random.random(np.sum(area)) < self.attack[c]
            self.clear_cells(area.astype(bool))

    def calculate_life(self, cells, area, radius):
        y, x = nd.center_of_mass(cells)
        life = np.zeros(np.shape(area))
        for cell in np.transpose(area.nonzero()):
            d = np.sqrt(np.power(y - cell[0], 2) + np.power(x - cell[1], 2))
            life[cell[0], cell[1]] = (1.0 / d) * radius + random.random() * .5 + .1
        return life
