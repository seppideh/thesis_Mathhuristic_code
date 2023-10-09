import random
from scipy.spatial.distance import cdist

def fitness_function(chromosome,Vic):
    total_distance = 0
    euclidean_distance = cdist(
        Vic, chromosome, metric='euclidean')
    min_list = []
    for row in euclidean_distance:
        min_list.append(min(row))
    total_distance = sum(min_list)
    return total_distance


def generate_population(population_size,Vic, clusters_hypo):
    population = []
    for _ in range(population_size):
        seed_points = random.sample(Vic, clusters_hypo)
        population.append(seed_points)
    return population

    # for i in range(population_size):
    #     initial_clusters = ClusteringSolution()
    #     individual = {'Seed_Numbers': initial_clusters.seedNumbers(), 'Seed_Position': initial_clusters.position(),
    #                   'Objective_Func': initial_clusters.cost(), 'allocate_factories': initial_clusters.factoriesAllocation()}
    #     population.append(individual)
    # return population


def RouletteWheelSelection(p):
    r = random.random()


# Perform crossover between two parent chromosomes
def crossover(parent1, parent2,clusters_hypo):
    child1 = []
    child2 = []
    for i in range(clusters_hypo):
        if random.random() < 0.5:
            child1.append(parent1[i])
            child2.append(parent2[i])
        else:
            child1.append(parent2[i])
            child2.append(parent1[i])
    return child1, child2


def clustering_solution(seed_points,Vic):
    euclidean_distance = cdist(
            Vic, seed_points, metric='euclidean')
    min_index = []
    for row in euclidean_distance:
        row = row.tolist()
        min_index.append(row.index(min(row))+1)
    return min_index


class ClusteringSolution:
    def seedNumbers(self):
        seedpoints = list(random.sample(
            range(1, numOfFactories+1), clusters_hypo))
        # self.result=sorted(seedpoints)
        # return self.result
        return sorted(seedpoints)

    def position(self):
        position = []
        for num in self.seedNumbers():
            position.append(Vic[num-1])
        return position

    def euclidean(self):
        euclidean_distance_Matrix = cdist(
            Vic, self.position(), metric='euclidean')
        return euclidean_distance_Matrix

    def cost(self):
        min_list = []
        for row in self.euclidean():
            min_list.append(min(row))
        cost = sum(min_list)
        return cost

    def factoriesAllocation(self):
        min_index = []
        for row in self.euclidean():
            row = row.tolist()
            min_index.append(row.index(min(row))+1)
        return min_index
