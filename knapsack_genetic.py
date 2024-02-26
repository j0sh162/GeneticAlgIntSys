import random
# generates a list of values for knapsack items as a range: [1, n]
# return list is of length count_times (the amount of knapsack items)
def generate_values(count_items):
    return [*range(1, count_items+1)]

# generates a list of random weights: [1, 10]
# return list is of length count_times (the amount of knapsack items)
def generate_weights(count_items):
    weights = []
    for i in range(count_items):
        weights.append(int(random.random()*10))
    return weights

# generate a population of given size (population_size)
# each individual (genotype) is of length count_times (the amount of knapsack items)
# returns a population list of size population_size
def generate_population(count_items, population_size):
    population = []
    for i in range(population_size):
        genotype = ""
        for j in range(count_items):
            if random.random() >= 0.5:
                genotype += str(1)
            else:
                genotype += str(0)
        population.append(genotype)
    return population

# evaluate the fitness of one genotype
# returns the fitness value of the genotype
def fitness_eval(genotype, count_items, max_weight, weights, values):
    if len(genotype) > count_items:
        return 0

    genotype_weight = 0
    genotype_value = 0

    index = 0
    for gene in genotype:
        if int(gene) == 0:
            index += 1
            continue
        elif int(gene) == 1:
            genotype_weight += weights[index]
            genotype_value += values[index]
            if genotype_weight > max_weight:
                genotype_value = 0
                break
        index += 1
    return genotype_value

# evaluate the fitness of each genotype in a population
# returns a list of fitness values of each individual in the population
def population_fitness(population, count_items, max_weight, weights, values):
    fitness = []
    for i in range(len(count_items)):
        fitness.append(fitness_eval(population[i], count_items, max_weight, weights, values))
    return fitness

# returns a list of individuals selected from the roulette
# the individuals need to pass the probability threshold
def roulette_selection(prob_thresh, population, fitness):
    selection = []
    total_value = sum(fitness)
    for i in range(len(population)):
        if fitness[i]/total_value >= prob_thresh:
            selection.append(population[i])
    return selection



pop_size = 10

total_weight = 20
count_items = 5
weights = generate_weights(count_items)
values = generate_values(count_items)
population = generate_population(count_items, pop_size)

print("Weights:", weights)
print("Values:", values)

for i in range(pop_size):
    print(population[i], ":", fitness_eval(population[i], count_items, total_weight, weights, values))