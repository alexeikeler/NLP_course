import random

from anneal import SimAnneal
from visualize_tsp import TSPPlotter


def read_coords(path):
    coords = []
    with open(path, "r") as f:
        for line in f.readlines():
            line = [float(x.replace("\n", "")) for x in line.split(" ")]
            coords.append(line)
    print(len(coords))
    return coords


def generate_random_coords(num_nodes):
    return [[random.uniform(-1000, 1000), random.uniform(-1000, 1000)] for _ in range(num_nodes)]


def main():
    # coords = read_coords("coord.txt")
    coords = generate_random_coords(45)

    sa = SimAnneal(coords, stopping_iter=5000)
    sa.anneal()
    #sa.results()

    plotter = TSPPlotter()
    plotter.plot_temperature(sa.temperature_list)
    plotter.plot_learning(sa.fitness_list)
    plotter.visualize_routes([sa.best_solution], sa.coords)
    plotter.draw()


if __name__ == '__main__':
    main()
