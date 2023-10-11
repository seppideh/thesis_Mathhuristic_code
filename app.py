import random
import math
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
from docplex.mp.model import Model
from my_functions import fitness_function, generate_population, crossover, clustering_solution, change_sizeOf_parameters
from readFile_function import read_file
from mathematical_model import TaxPolicy, CapTradePolicy, CapPolicy, OfsetPolicy

# Problem Definition
numOfFactories = 24
finalClusters = 1
clusters_hypo = 1*finalClusters  # seed_points_count
Emax = 2000000000
H = 0.04                         # carbon price
M = 10000000000                  # big number
gamma = 0.05                     # polution cost
tax = 0.11

# GA Parameters

MaxIt = 50                               # Maximum Number of Iterations
population_size = 100                                # Population Size

pCrossover = 0.8                         # Crossover Percentage
# Number of Parnets (population_c)
nCrossover = 2*round(pCrossover*population_size/2)

pMutation = 0.3                          # Mutation Percentage
nMutation = round(pMutation*population_size)        # Number of Mutants
mu = 0.1                                 # Mutation Rate

slp = 8                                 # Selection Pressure
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
    # print(BestSol.get('Objective_Func'))

best_chromosome = BestSol.get('seed_points')

# for seed_point in best_chromosome:
#     print(seed_point)


ClusterMembers = clustering_solution(best_chromosome, Vic)
# print(ClusterMembers)

TaxClusters = []
CapTradeClusters = []
CapClusters = []
OfsetClusters = []

clusters = []
for clusterNum in range(1, clusters_hypo+1):
    # factories numbers in cluster
    factNums = [i for i, x in enumerate(ClusterMembers) if x == clusterNum]
    print(factNums)
    [Vicn, CEn, CErn, Dn, Capn, PCn, PCrn, SPn, FCn] = change_sizeOf_parameters(
        Vic, CE, CEr, D, Cap, PC, PCr, SP, FC, factNums)

    [status, objective_function, Q, W, QW] = TaxPolicy(
        CEn, CErn, Dn, Capn, PCn, PCrn, SPn, FCn, len(factNums), tax, gamma)
    [status, objective_function, beta, Q, W, QW, eb, es] = CapTradePolicy(
        CEn, CErn, Dn, Capn, PCn, PCrn, SPn, FCn, len(factNums), Emax, H, M, gamma)
    [status, objective_function, beta, Q, W, QW] = CapPolicy(
        CEn, CErn, Dn, Capn, PCn, PCrn, SPn, FCn, len(factNums), Emax, M, gamma)
    [status, objective_function, beta, Q, W, QW, eb] = OfsetPolicy(
        CEn, CErn, Dn, Capn, PCn, PCrn, SPn, FCn, len(factNums), Emax, H, M, gamma)

    print('Solution status:', status)
    print("Objective value:", objective_function)
    # print('beta:', beta)
    print('Q:', Q)
    print('W:', W)
    print('QW:', QW)
    # print('eb:', eb)
    # print('es:', es)
