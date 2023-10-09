import random

# Constants
POPULATION_SIZE = 50
SEED_POINT_COUNT = 3
MAX_ITERATIONS = 100

# Data points
data_points = [
    [1, 2], [2, 1], [2, 3], [4, 5], [5, 4], [5, 6], [7, 8], [8, 7], [8, 9]
]

# Generate initial population
def generate_population():
    population = []
    for _ in range(POPULATION_SIZE):
        seed_points = random.sample(data_points, SEED_POINT_COUNT)
        population.append(seed_points)
    return population

# Calculate fitness of a chromosome (seed points)
def calculate_fitness(chromosome):
    total_distance = 0
    for point in data_points:
        distances = [calculate_distance(point, seed_point) for seed_point in chromosome]
        min_distance = min(distances)
        total_distance += min_distance
    return total_distance

# Calculate Euclidean distance between two points
def calculate_distance(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

# Perform crossover between two parent chromosomes
def crossover(parent1, parent2):
    child = []
    for i in range(SEED_POINT_COUNT):
        if random.random() < 0.5:
            child.append(parent1[i])
        else:
            child.append(parent2[i])
    return child

# Perform mutation on a chromosome
def mutate(chromosome):
    mutated_chromosome = chromosome.copy()
    index = random.randint(0, SEED_POINT_COUNT - 1)
    mutated_chromosome[index] = random.choice(data_points)
    return mutated_chromosome

# Genetic algorithm for clustering
def genetic_clustering():
    population = generate_population()

    for _ in range(MAX_ITERATIONS):
        # Calculate fitness for each chromosome
        fitness_scores = [calculate_fitness(chromosome) for chromosome in population]

        # Select parents for crossover
        parents = random.choices(population, weights=fitness_scores, k=2)

        # Perform crossover and mutation to create new offspring
        offspring = crossover(parents[0], parents[1])
        offspring = mutate(offspring)

        # Replace the least fit chromosome with the offspring
        min_fitness_index = fitness_scores.index(min(fitness_scores))
        population[min_fitness_index] = offspring

    # Select the best chromosome (seed points) as the result
    best_chromosome = min(population, key=calculate_fitness)
    return best_chromosome

# Run the genetic clustering algorithm
result = genetic_clustering()
print("Cluster Centers:")
for seed_point in result:
    print(seed_point)
