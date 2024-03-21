import random
import numpy as np
import csv

INT_MAX = 2147483647

def generate_city(num_cities):
    # Generate random cost matrix for 50 cities
    cost_matrix = np.random.randint(1, 50, size=(num_cities, num_cities))

    # Make diagonal elements zero since it costs nothing to go from a city to itself
    cost_matrix = cost_matrix + cost_matrix.T
    np.fill_diagonal(cost_matrix, 0)

    # Display the cost matrix
    return cost_matrix

# Each chromosone is the order of the cities we visit
def gen_genome(leng,start):
    genome = []
    while True:
        rnd = random.randint(0, leng - 1)
        if rnd not in genome and rnd != start:
            genome.append(rnd)
        if len(genome) == leng - 1:
            genome = [start] + genome + [start]
            return {"score": 0, "genome": genome}


def gen_population(pop_size, len, start):
    population = []
    for i in range(pop_size):
        # print(population)
        population.append(gen_genome(len, start))
    return population


def evaluate_func(population, map):
    for genome in population:
        f = 0
        for i in range(len(genome['genome'])-1):
            # print( map[genome['genome'][i]][genome['genome'][i + 1]])
            # print(genome)
            # print(map[genome['genome'][i]][genome['genome'][i + 1]])
            f += map[genome['genome'][i]][genome['genome'][i + 1]]
        genome['score'] = f
        # print(genome)
       
    # return sorted(population, key=lambda x: x["score"], reverse=True)
    return population

# Tournamnet selection, chooses two most fittest individuals
def tournament_selection(population, tournament_size):
    selected_inds = []

    # several limited size tournaments
    # here we are doing minimization,
    # so the lower the score - the fitter the individual
    for _ in range(len(population)//2):
        tournament = random.sample(population, tournament_size)
        tournament_fitness = [ind["score"] for ind in tournament]

        # select the fittest ind
        fittest_individual_index = tournament_fitness.index(min(tournament_fitness))
        selected_inds.append(tournament[fittest_individual_index])
        
        # select the 2nd fittest ind
        tournament_fitness[fittest_individual_index] = float('inf') # setting the 1st fittest to not be selected with the max
        fittest_individual_index = tournament_fitness.index(min(tournament_fitness))
        selected_inds.append(tournament[fittest_individual_index])

    return selected_inds


def mutate(population, p=0.2):
    for i in population:
        rnd = random.random()
        if(rnd < p):
            rnd_ind1 = random.randint(1,len(i['genome'])-2)
            rnd_ind2 = random.randint(1,len(i['genome'])-2)
            
            i['genome'][rnd_ind1], i['genome'][rnd_ind2] = i['genome'][rnd_ind2], i['genome'][rnd_ind1]
            
    return population

def crossover_ind(mom, dad, start):
    dad = dad["genome"][1:-1]
    mom = mom["genome"][1:-1]

    point1 = random.randint(0, len(dad)-1)
    point2 = random.randint(0, len(dad)-1)
    if point2 < point1:
        point1, point2 = point2, point1

    child1 = dad[point1:point2]
    child2 = dad[:point1] + dad[point2:]
    
    for j in mom:
        if j not in child1:
            child1.append(j)
        if j not in child2:
            child2.append(j)
    
    child1 = [start]+child1+[start]
    child2 = [start]+child2+[start]
    
    child1 = {"score": 0, "genome": child1}
    child2 = {"score": 0, "genome": child2}

    return child1, child2 
    
def crossover(population, start, crossover_rate):
    children = []
    
    while len(children) < len(population):
        p1_id = random.randint(0, len(population)-1)
        p2_id = random.randint(0, len(population)-1)
        while p2_id == p1_id:
            p2_id = random.randint(0, len(population)-1)
        
        parent1 = population[p1_id]
        parent2 = population[p2_id]  

        if random.random() <= crossover_rate:
            child1, child1 = crossover_ind(parent1, parent2, start)
            children.append(child1)
            children.append(child1)
        else:
            children.append(parent1)
            children.append(parent2)

    return children

def select_best(population):
    sorted_pop = sorted(population, key=lambda x: x["score"], reverse=False)
    return sorted_pop[0]


def genetic_alg(map, pop_size, tournament_size, crossover_rate, mutation_rate, iter, start = 0):
    population = gen_population(pop_size, len(map[0]),start)
    best_solution = {"score": INT_MAX, "genome": ""}
    gen_solution_found = 0
    
    # Collect data for CSV
    results = []


    population = evaluate_func(population, map)
    for i in range(iter):
        population = tournament_selection(population, tournament_size)
        population = crossover(population, start, crossover_rate)
        population = mutate(population, mutation_rate)
        population = evaluate_func(population, map)
        
        tmp_best = select_best(population)
        if tmp_best["score"] < best_solution["score"]:
            best_solution = tmp_best.copy()
            gen_solution_found = i
        
        # Append data for CSV
        results.append({
            "Generation": i,
            "Best Score": best_solution["score"],
            "Best Genotype": best_solution["genome"],
            "Population Size": pop_size,
            "Tournament Size": tournament_size,
            "Crossover Rate": crossover_rate,
            "Mutation Rate": mutation_rate,
            "Iterations": gen_iter
        })


    return best_solution, gen_solution_found, results

def save_results_to_csv(results, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = results[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    np.random.seed(0)
    random.seed(404)
    
    # Example usage:
    graph = generate_city(100)
    # graph = [
    #     [0, 2, INT_MAX, 12, 5],
    #     [2, 0, 4, 8, INT_MAX],
    #     [INT_MAX, 4, 0, 3, 3],
    #     [12, 8, 3, 0, 10],
    #     [5, INT_MAX, 3, 10, 0],
    # ]
    pop_size = 500
    gen_iter = 1000
    
    tournament_size = pop_size//10
    crossover_rate = 0.5
    mutation_rate = 0.1
    
    best_solution, gen_solution_found, results = genetic_alg(graph, pop_size, tournament_size, crossover_rate, mutation_rate, gen_iter)

    print("Best Solution Found:", best_solution)
    print("Generation Solution Found:", gen_solution_found)
    print(graph)

    save_results_to_csv(results, "TSP_GA_results.csv")

    
