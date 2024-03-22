import random
import csv

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
# each individual contains its genotype, value and weight
# each individual's genotype is of length count_times (the amount of knapsack items)
# returns a population list of size population_size
def generate_population(count_items, population_size):
    if population_size % 2 != 0:
        population_size += 1
        
    population = []
    for i in range(population_size):
        genotype = ""
        for j in range(count_items):
            if random.random() >= 0.5:
                genotype += str(1)
            else:
                genotype += str(0)
        individual = {"genotype": genotype, "value": 0, "weight": 0}
        population.append(individual)
    return population

# evaluate the fitness of one individual
# returns the fitness value of the individual
def fitness_eval(individual, count_items, max_weight, weights, values):
    genotype = individual["genotype"]
    if len(genotype) > count_items:
        individual["value"] = 0
        return individual

    indiv_value = 0
    indiv_weight = 0

    index = 0
    for gene in genotype:
        if int(gene) == 0:
            index += 1
            continue
        elif int(gene) == 1:
            indiv_value += values[index]
            indiv_weight += weights[index]
            if indiv_weight > max_weight:
                indiv_value = 0
                break
        index += 1
        
    individual["value"] = indiv_value
    individual["weight"] = indiv_weight
    return individual

# evaluate the fitness of each genotype in a population
# returns a list of fitness values of each individual in the population
def evaluate_fitness(population, count_items, max_weight, weights, values):
    return [fitness_eval(ind, count_items, max_weight, weights, values) for ind in population]
    
# Tournamnet selection, chooses two most fittest individuals
# elitism_proportion should be between 0 and 1
def tournament_selection(population, elitism_proportion, tournament_size):
    selected_inds = []

    
    # elitism seleciton
    pop_sorted = sorted(population, key=lambda x: x["value"], reverse=True)
    
    for i in range(int(len(population) * elitism_proportion)):
        if pop_sorted[i]["value"] > 0:
            selected_inds.append(pop_sorted[i])
        else:
            break
    
    # if of odd length - remove one element
    if len(selected_inds) % 2 != 0:
        selected_inds.pop()
    
    # several limited size tournaments
    # for _ in range(len(population)//2):
    while len(selected_inds) < len(population):
        tournament = random.sample(population, tournament_size)
        tournament_fitness = [ind["value"] for ind in tournament]

        # select the fittest ind
        fittest_individual_index = tournament_fitness.index(max(tournament_fitness))
        selected_inds.append(tournament[fittest_individual_index])
        
        # select the 2nd fittest ind
        tournament_fitness[fittest_individual_index] = float('-inf') # setting the 1st fittest to not be selected with the max
        fittest_individual_index = tournament_fitness.index(max(tournament_fitness))
        selected_inds.append(tournament[fittest_individual_index])

    return selected_inds

# double-point crossover
def crossover_ind(mom, dad):
    mom_genotype = mom["genotype"]
    dad_genotype = dad["genotype"]
    
    point1 = random.randint(1, len(mom_genotype))
    point2 = random.randint(1, len(mom_genotype))
    if point1 > point2:
        point1, point2 = point2, point1
    
    kid1_genotype = mom_genotype[:point1] + dad_genotype[point1:point2] + mom_genotype[point2:]
    kid2_genotype = dad_genotype[:point1] + mom_genotype[point1:point2] + dad_genotype[point2:]
    
    kid1 = {"genotype": kid1_genotype, "value": 0, "weight": 0}
    kid2 = {"genotype": kid2_genotype, "value": 0, "weight": 0}

    return kid1, kid2

def crossover_population(population, crossover_rate):
    kids = []
    while len(kids) < len(population):
        p1_id = random.randint(0, len(population)-1)
        p2_id = random.randint(0, len(population)-1)
        while p2_id == p1_id:
            p2_id = random.randint(0, len(population)-1)
        
        parent1 = population[p1_id]
        parent2 = population[p2_id]
        
        if random.random() <= crossover_rate:
            kid1, kid2 = crossover_ind(parent1, parent2)
            kids.append(kid1)
            kids.append(kid2)
        # else:
        #     kids.append(parent1)
        #     kids.append(parent2)
    return kids

# apply bit-flipping mutation to the whole population
def mutate(population, mutation_rate):
    for ind in population:
        genotype = ind["genotype"]
        for i in range(len(genotype)):
            if random.random() <= mutation_rate:
                if int(genotype[i]) == 1:
                    genotype = genotype[:i] + '0' + genotype[i+1:]
                else:
                    genotype = genotype[:i] + '1' + genotype[i+1:]
        ind["genotype"] = genotype
    return population

# Selects the ind with the highest fitness value
def select_best(population):
    sorted_pop = sorted(population, key=lambda x: x["value"], reverse=True)
    return sorted_pop[0]

def get_avg(population):
    values = [p["value"] for p in population ]
    return sum(values)/len(population)

def genetic_main_loop(max_weight, values, weights, pop_size, tournament_size, elitism_proportion, crossover_rate, mutation_rate, gen_iter):
    random.seed(404)

    count_items = len(values)
    population = generate_population(count_items, pop_size)
    
    best_solution = {"genotype": "", "value": 0, "weight": 0}
    gen_solution_found = 0
    
    # Collect data for CSV
    results = []
    
    population = evaluate_fitness(population, count_items, max_weight, weights, values)
    for i in range(gen_iter): 
        # Selection (tournamnet)
        population = tournament_selection(population, elitism_proportion, tournament_size)
        # Crossover - reproduction
        population = crossover_population(population, crossover_rate)
        # Mutate
        population = mutate(population, mutation_rate)
        # Evaluate, save the best solution thus far
        population = evaluate_fitness(population, count_items, max_weight, weights, values)
        tmp_best = select_best(population)
        if tmp_best["value"] > best_solution["value"]:
            best_solution = tmp_best.copy()
            gen_solution_found = i
        
        # # Append data for CSV
        # results.append({
        #     "Generation": i,
        #     "Best Value": best_solution["value"],
        #     "Average Value": get_avg(population),
        #     "Best Weight": best_solution["weight"],
        #     "Best Genotype": best_solution["genotype"],
        #     "Max Weight": max_weight,
        #     "Values": values,
        #     "Weights": weights,
        #     "Population Size": pop_size,
        #     "Tournament Size": tournament_size,
        #     "Crossover Rate": crossover_rate,
        #     "Mutation Rate": mutation_rate,
        #     "Iterations": gen_iter
        # })

    
    return best_solution, gen_solution_found, results#, select_best(population)

def save_results_to_csv(results, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = results[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    random.seed(404)

    max_weight = 50
    # values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    # weights = [2, 7, 1, 9, 2, 10, 2, 6, 3, 7, 2, 1, 8, 2, 9, 1, 3, 10, 3, 4, 3, 9, 3, 5, 7, 5, 9, 1, 5, 6]
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
    weights = [2, 7, 1, 9, 2, 10, 2, 6, 3, 7, 2, 1, 8, 2, 9, 1, 3, 10, 3, 4, 3, 9, 3, 5, 7, 5, 9, 1, 5, 6, 9, 10, 4, 2, 1, 5, 2, 7, 8, 7]
    pop_size = 500
    gen_iter = 1000

    # print(generate_values(40))
    # print(generate_weights(40))

    tournament_size = pop_size // 10
    elitism_proportion = 0.0
    crossover_rate = 0.5
    mutation_rate = 0.05

    best_solution, gen_solution_found, results = genetic_main_loop(max_weight, values, weights, pop_size, tournament_size, elitism_proportion, crossover_rate, mutation_rate, gen_iter)

    print("Best Solution Found:", best_solution)
    print("Generation Solution Found:", gen_solution_found)

    # save_results_to_csv(results, "knapsack_GA_results.csv")
