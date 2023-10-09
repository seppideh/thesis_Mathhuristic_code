import random
import math
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
from docplex.mp.model import Model
from my_functions import fitness_function, generate_population, crossover, clustering_solution
from readFile_function import read_file

# Define the Model

# MWMS_model = Model(name="Linear Program")

# # Variables
# x = MWMS_model.continuous_var(name='x', lb=0)
# y = MWMS_model.continuous_var(name='y', lb=0)

# # Constraints
# c1 = MWMS_model.add_constraint(x+y >= 8, ctname="c1")
# c2 = MWMS_model.add_constraint(2*x+y >= 10, ctname="c2")
# c3 = MWMS_model.add_constraint(x+4*y >= 11, ctname="c3")

# # Objective Function
# obj = 5*x+4*y
# MWMS_model.set_objective('min', obj)
# MWMS_model.print_information()

# # Solvig
# solution = MWMS_model.solve()

# # Output
# print(solution)


# Problem Definition
numOfFactories = 24
finalClusters = 3
clusters_hypo = 3*finalClusters  # seed_points_count


# GA Parameters

MaxIt = 50                               # Maximum Number of Iterations
population_size = 100                                # Population Size

pCrossover = 0.8                         # Crossover Percentage
# Number of Parnets (population_c)
nCrossover = 2*round(pCrossover*population_size/2)

pMutation = 0.3                          # Mutation Percentage
nMutation = round(pMutation*population_size)        # Number of Mutants
mu = 0.1                                 # Mutation Rate

beta = 8                                 # Selection Pressure
# percentage of New otherClusters that investigate
percentSel = 0.2

[Vic, CE, CEr, D, Cap, PC, PCr, SP, FC] = read_file('factories24.txt')


population = generate_population(population_size, Vic, clusters_hypo)
# population.sort(key=lambda item: item['Objective_Func'])
# pop=sorted(pop,key=lambda x:x['Objective_Func'])

BestCost = []


# Genetic Algorithm
for it in range(MaxIt):
    # p = [-(beta/WorstCost) * num for num in costs]
    # p = [np.e ** x for x in p]
    # p = [(1/sum(p))*num for num in p]
    # Calculate fitness for each chromosome
    fitness_scores = [fitness_function(chromosome, Vic)
                      for chromosome in population]

    # Croseeover
    population_c = []
    for k1 in range(1, nCrossover, 2):
        # Select parents for crossover
        parents = random.choices(population, weights=fitness_scores, k=2)

        # Perform crossover to create new offspring
        [child1, child2] = crossover(parents[0], parents[1], clusters_hypo)
        population_c.append(child1)
        population_c.append(child2)

    # mutation
    population_m = []
    # for k2 in nMutation:

    population = population+population_c+population_m
    solutions = []

    for chr in population:
        solution = {'seed_points': chr,
                    'Objective_Func': fitness_function(chr, Vic)}
        solutions.append(solution)

    # sort solutions
    solutions.sort(key=lambda item: item['Objective_Func'])

    # Truncation
    population = [item['seed_points'] for item in solutions]
    population = population[:population_size]

    BestSol = solutions[0]
    BestCost.append(BestSol.get('Objective_Func'))
    print(BestSol.get('Objective_Func'))

best_chromosome = BestSol.get('seed_points')

for seed_point in best_chromosome:
    print(seed_point)


ClusterMembers = clustering_solution(best_chromosome, Vic)
print(ClusterMembers)

TaxClusters = []
CapTradeClusters = []
CapClusters = []
OfsetClusters = []

clusters = []
for clusterNum in range(1, clusters_hypo+1):
    # factories numbers in cluster
    factNums = [i for i, x in enumerate(ClusterMembers) if x == clusterNum]
