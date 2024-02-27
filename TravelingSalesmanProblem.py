import random


# Each chromosone is the order of the cities we visit
def gen_genome(len):
    genome = []
    while True:
        rnd = random.randint(0, len)
        if rnd not in genome:
            genome.append(rnd)
        if len(genome) == len:
            return {"score": 0, "genome": genome}


def gen_population(pop_size, len):
    population = []
    for i in range(pop_size):
        population.append(gen_genome(len))
    return population


def genetic_alg(pop_size, map, iter):
    population = gen_population(pop_size,len(map[0]))
    
    for i in range(iter):
        population = evaluate_func(population,map)
        population = crossover(population)
    
    return None


def evaluate_func(population, map):
    for genome in population:
        f = 0
        for i in range(len(genome) - 1):
            f += map[genome[i]][genome[i] + 1]
        genome['score'] = f
    return sorted(population, key=lambda x: x['score'],reverse=True)


# for this we take the top half of the population and breed them to fill up the population
def crossover(population):
    population = population[:len(population)/2]
    children = []    
    for i in range(0,len(population),2):
        dad = population[i]['genome']
        mom = population[i+1]['genome']
        
        point1 = random.randint(0, len(dad))
        point2 = random.randint(0, len(dad))

        if(point2 < point1):
            point1,point2 = point2,point1
        
        child1 = dad[point1:point2]
        child2 = dad[:point1]
        child2.append(dad[point2:])
        for j in mom:
            if j not in child1:
                child1.append(j)
            if j not in child2:
                child2.append(j)
        
        child1 = {
            'score':0,
            'genome':child1
        }
        child2 = {
            'score':0,
            'genome':child2
        }
        children.append([child1,child2])
    
    population.append(children)    
        
        
    return population


if __name__ == "__main__":
    # Example usage:
    graph = [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]
    start_city = 0
    min_cost = 0

    print("Minimum cost of traveling salesman tour:", min_cost)
