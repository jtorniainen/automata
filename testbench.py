# This is for comparing execution times of different implementations
import automata
import timeit


def run_simulation_1():
    n = 100
    specimens = create_specimens()
    all_cells = automata.get_all_cells(specimens, 200, 100)
    for itr in range(n):
        all_cells = automata.grow(specimens, all_cells)
        automata.attack(specimens, all_cells)


def run_simulation_2():
    n = 100
    specimens = create_specimens()
    all_cells = automata.get_all_cells(specimens, 200, 100)
    for itr in range(n):
        all_cells = automata.grow(specimens, all_cells)
        automata.attack2(specimens, all_cells)


def create_specimens():
    specimens = []
    for k in range(10):
        specimens.append(automata.Organism(199, 99, (0, 0, 0)))
    return specimens


a = timeit.timeit(run_simulation_1, number=10)
b = timeit.timeit(run_simulation_2, number=10)
print("Simulation 01: %0.2f" % a)
print("Simulation 02: %0.2f" % b)
