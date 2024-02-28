import random

INT_MAX = 2147483647

# Each chromosone is the order of the cities we visit

#TODO define a start postion as it needs to be a cycle
def gen_genome(leng,start):
    genome = []
    while True:
        rnd = random.randint(0, leng-1)
        if rnd not in genome and rnd != start:
            genome.append(rnd)
        if len(genome) == leng-1:
            genome = [start]+genome+[start]
            return {"score": 0, "genome": genome}


def gen_population(pop_size, len,start):
    population = []
    for i in range(pop_size):
        # print(population)
        population.append(gen_genome(len,start))
    return population


def genetic_alg(pop_size, map, iter,start = 0):
    population = gen_population(pop_size, len(map[0]),start)
    print(population)
    # print(len(population))
    for i in range(iter):
        print(i)
        population = evaluate_func(population, map)[:int(pop_size/2)]
        # population = roulette_selection(population)
        population = crossover(population,start)
        population = mutate(population)
    population = evaluate_func(population, map)
    
    return population[0]


def evaluate_func(population, map):
    # print(len(population))
    for genome in population:
        f = 0
        for i in range(len(genome['genome'])-1):
            # print( map[genome['genome'][i]][genome['genome'][i + 1]])
            # print(genome)
            # print(map[genome['genome'][i]][genome['genome'][i + 1]])
            f += map[genome['genome'][i]][genome['genome'][i + 1]]
        genome['score'] = f
        # print(genome)
       
    return sorted(population, key=lambda x: x["score"], reverse=False)


def roulette_selection(population, prob_thresh=0.5):
    selection = []
    total_value = sum(item["score"] for item in population)
    for i in range(len(population)):
        if population[i]["score"] / total_value >= prob_thresh:
            selection.append(population[i])
    return selection


def mutate(population, p=0.2):
   
    for i in population:
        # print(i)
        rnd = random.random()
        if(rnd<p):
            
            rnd_ind1 = random.randint(1,len(i['genome'])-2)
            rnd_ind2 = random.randint(1,len(i['genome'])-2)
            
            i['genome'][rnd_ind1], i['genome'][rnd_ind2] = i['genome'][rnd_ind2], i['genome'][rnd_ind1]
            
    
    return population


# for this we take the top half of the population and breed them to fill up the population
def crossover(population,start):
    children = []
    for i in range(0, len(population), 2):
        dad = population[i]["genome"][1:-1]
        mom = population[i + 1]["genome"][1:-1]

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
        children = children + [child1,child2]

    population = population + children

    return population


if __name__ == "__main__":
    # Example usage:
    graph = [
        [0, 2, INT_MAX, 12, 5],
        [2, 0, 4, 8, INT_MAX],
        [INT_MAX, 4, 0, 3, 3],
        [12, 8, 3, 0, 10],
        [5, INT_MAX, 3, 10, 0],
    ]
    print(genetic_alg(20,graph,100))
    
    
    min_cost = 0
