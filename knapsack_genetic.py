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
        weights.append(random.randint(1, 10))
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
def get_population_fitness(population, count_items, max_weight, weights, values):
    fitness = []
    for i in range(len(population)):
        fitness.append(fitness_eval(population[i], count_items, max_weight, weights, values))
    return fitness

# returns a list of individuals selected from the roulette
# the individuals need to pass the probability threshold
def roulette_selection(population, fitness, prob_thresh):
    selection = []
    total_value = sum(fitness)
    for i in range(len(population)):
        if fitness[i]/total_value >= prob_thresh:
            selection.append(population[i])
    return selection

def tournament_selection(population, fitness):
    k_competitors = max(int(len(population) / 3), 2)
    
    competitors = []
    competitors_fitness = []
    for i in range(k_competitors):
        rand_id = random.randint(0, len(population)-1)
        competitors.append(population[rand_id])
        competitors_fitness.append(fitness[rand_id])
    
    while len(competitors) > 1:
        weakest_id = competitors_fitness.index(min(competitors_fitness))
        del competitors[weakest_id]
        del competitors_fitness[weakest_id]

    return competitors[0]





def mutation(genotype, mutation_rate):
    for i in range(len(genotype)):
        if random.random() <= mutation_rate:
            if int(genotype[i]) == 1:
                genotype = change_str_char_at_i(genotype, '0', i)
            else:
                genotype = change_str_char_at_i(genotype, '1', i)
    return genotype

def change_str_char_at_i(string, char, i):
    return string[:i] + char + string[i+1:]

def mutate_population(population, mutation_rate):
    for genotype in population:
        genotype = mutation(genotype, mutation_rate)
    return population

# double-point crossover
def crossover(mom, dad):
    point1 = random.randint(1, len(mom))
    point2 = random.randint(1, len(mom))
    if point1 > point2:
        point1, point2 = point2, point1
    
    kid1 = mom[:point1] + dad[point1:point2] + mom[point2:]
    # kid2 = dad[:point1] + mom[point1:point2] + dad[point2:]
    return kid1#, kid2


def select_reproduce_mutate(population, fitness, prob_thresh, mutation_rate):
    # Selection
    original_len = len(population)
    # selection = roulette_selection(population, fitness, prob_thresh)
    selection = tournament_selection(population, fitness)
    if len(selection) > original_len:
        selection = selection[:original_len]
    
    # Crossover
    children = []
    while len(children) < original_len:
        parent1 = selection[random.randint(0, len(selection)-1)]
        parent2 = selection[random.randint(0, len(selection)-1)]
        child = crossover(parent1, parent2)
        children.append(child)
    
    # Mutate
    return mutate_population(children, mutation_rate)

def pick_best_individuals(population, fitness_p, offspring, fitness_o):
    population_combined = list(zip(population, fitness_p))
    offspring_combined = list(zip(offspring, fitness_o))
    
    population_combined.sort(key=lambda x: x[1], reverse=True)
    offspring_combined.sort(key=lambda x: x[1], reverse=True)

    best_individuals = population_combined[:len(population)] + offspring_combined[:len(population)]
    best_individuals.sort(key=lambda x: x[1], reverse=True)
    best_individuals = best_individuals[:len(population)]

    best_fitness_value = best_individuals[0][1]
    best_individuals = [genotype for genotype, _ in best_individuals]

    return best_individuals, best_fitness_value


def genetic_main_loop(max_weight, count_items, pop_size, selection_thresh, mutation_rate, gen_iter):
    values = generate_values(count_items)
    weights = generate_weights(count_items)
    population = generate_population(count_items, pop_size)
    best_solution = ["", 0]
    for i in range(gen_iter):
        population_fitness = get_population_fitness(population, count_items, max_weight, weights, values)
        children = select_reproduce_mutate(population, population_fitness, selection_thresh, mutation_rate)
        children_fitness = get_population_fitness(children, count_items, max_weight, weights, values)
        population, top_fitness_tmp = pick_best_individuals(population, population_fitness, children, children_fitness)
        if top_fitness_tmp >= best_solution[1]:
            best_solution[0] = population[0]
            best_solution[1] = top_fitness_tmp
    
    return best_solution[0], best_solution[1]



max_weight = 20
count_items = 10
pop_size = 1000
selection_thresh = 0.2
mutation_rate = 0.01
generation_iterator = 100
print(genetic_main_loop(max_weight, count_items, pop_size, selection_thresh, mutation_rate, generation_iterator))



# weights = generate_weights(count_items)
# values = generate_values(count_items)
# population = generate_population(count_items, pop_size)

# print("Weights:", weights)
# print("Values:", values)

# for i in range(pop_size):
#     print(population[i], ":", fitness_eval(population[i], count_items, total_weight, weights, values))