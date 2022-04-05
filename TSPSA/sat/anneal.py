import math
import random
import pandas as pd
from tabulate import tabulate


class SimAnneal:

    def __init__(self, coords, T=-1, alpha=-1, stopping_T=-1, stopping_iter=-1):

        self.coords = coords
        self.N = len(coords)
        self.T = math.sqrt(self.N) if T == -1 else T
        self.alpha = 0.995 if alpha == -1 else alpha
        self.stopping_temperature = 1e-8 if stopping_T == -1 else stopping_T
        self.stopping_iter = 100000 if stopping_iter == -1 else stopping_iter
        self.iteration = 1

        self.nodes = [i for i in range(self.N)]

        self.best_solution = None
        self.best_fitness = float("Inf")
        self.fitness_list = []
        self.temperature_list = []

        self.greedy_sol_fitness = None
        self.cur_solution = None
        self.cur_fitness = None

    def initial_solution(self):
        """
        Greedy algorithm to get an initial solution (closest-neighbour).
        """

        cur_node = random.choice(self.nodes)  # start from a random node
        solution = [cur_node]

        free_nodes = set(self.nodes)
        free_nodes.remove(cur_node)

        while free_nodes:

            next_node = min(free_nodes, key=lambda x: self.dist(cur_node, x))  # nearest neighbour
            free_nodes.remove(next_node)
            solution.append(next_node)
            cur_node = next_node

        cur_fit = self.fitness(solution)

        if cur_fit < self.best_fitness:  # If best found so far, update best fitness
            self.best_fitness = cur_fit
            self.best_solution = solution

        self.fitness_list.append(cur_fit)

        self.greedy_sol_fitness = cur_fit
        return solution, cur_fit

    def dist(self, node_0, node_1):
        """
        Euclidean distance between two nodes.
        """
        coord_0, coord_1 = self.coords[node_0], self.coords[node_1]
        return math.sqrt((coord_0[0] - coord_1[0]) ** 2 + (coord_0[1] - coord_1[1]) ** 2)

    def fitness(self, solution):
        """
        Total distance of the current solution path.
        """

        cur_fit = 0
        for i in range(self.N):
            cur_fit += self.dist(solution[i % self.N], solution[(i + 1) % self.N])
        return cur_fit

    def p_accept(self, candidate_fitness):
        """
        Probability of accepting if the candidate is worse than current.
        Depends on the current temperature and difference between candidate and current.
        """
        return math.exp(-abs(candidate_fitness - self.cur_fitness) / self.T)

    def accept(self, candidate):
        """
        Accept with probability 1 if candidate is better than current.
        Accept with probabilty p_accept(..) if candidate is worse.
        """
        candidate_fitness = self.fitness(candidate)
        if candidate_fitness < self.cur_fitness:
            self.cur_fitness, self.cur_solution = candidate_fitness, candidate
            if candidate_fitness < self.best_fitness:
                self.best_fitness, self.best_solution = candidate_fitness, candidate
        else:
            if random.random() < self.p_accept(candidate_fitness):
                self.cur_fitness, self.cur_solution = candidate_fitness, candidate

    def anneal(self):
        """
        Execute simulated annealing algorithm.
        """
        # Initialize with the greedy solution.
        self.cur_solution, self.cur_fitness = self.initial_solution()

        while self.T >= self.stopping_temperature and self.iteration < self.stopping_iter:

            candidate = list(self.cur_solution)

            l = random.randint(2, self.N - 1)
            i = random.randint(0, self.N - l)
            candidate[i : (i + l)] = reversed(candidate[i : (i + l)])

            self.accept(candidate)
            self.temperature_list.append(self.T)
            self.T *= self.alpha
            self.iteration += 1

            self.fitness_list.append(self.cur_fitness)

        improvement = 100 * (self.fitness_list[0] - self.best_fitness) / (self.fitness_list[0])

        d = {
            'Начальное решение при помощи жадного алгоритма': self.greedy_sol_fitness,
            'Метод имитации отжига': self.best_fitness,
            'Улучшение относительно жадного алгоритма': f'{round(improvement, 2)} %'
        }

        df = pd.DataFrame.from_dict(d, orient='index')
        df = df.rename(columns={0: 'Results'})

        print(
            tabulate(df, headers=df.columns, tablefmt='pretty')
        )

