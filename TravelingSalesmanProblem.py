import random
import numpy as np

INT_MAX = 2147483647

def gen_genome(leng, start):
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


def genetic_alg(pop_size, map, iter,decay = 0.1, start=0):
    population = gen_population(pop_size, len(map[0]), start)
    print(population)
    # print(len(population))
    temp = 100
    for i in range(iter):
        print(i)
        population = evaluate_func(population, map)
        population = roulette_selection(population,temp)
        temp = temp - decay

        population = crossover(population, start)
        population = mutate(population)
    population = evaluate_func(population, map)

    return population[0]


def evaluate_func(population, map):
    for genome in population:
        f = 0
        for i in range(len(genome["genome"]) - 1):
            f += map[genome["genome"][i]][genome["genome"][i + 1]]
        genome["score"] = f

    return sorted(population, key=lambda x: x["score"], reverse=False)


def roulette_selection(population,temp):
    if temp < 1:
        temp = 1
    selection = []
    sum = 0
    for i in population:
        sum = sum + np.exp(i['score']/temp)

    i = 0
    while(len(selection)<len(population)/2):
        if i > len(population):
            i = 0
        p_i = np.exp(population[i]['score']/temp)/sum
        rnd = np.random.rand()
        if p_i > rnd:
            selection = selection + population[i]


    return selection


def mutate(population, p=0.2):
    for i in population:
        rnd = random.random()
        if rnd < p:
            rnd_ind1 = random.randint(1, len(i["genome"]) - 2)
            rnd_ind2 = random.randint(1, len(i["genome"]) - 2)
            i["genome"][rnd_ind1], i["genome"][rnd_ind2] = (
                i["genome"][rnd_ind2],
                i["genome"][rnd_ind1],
            )

    return population


# for this we take the top half of the population and breed them to fill up the population
def crossover(population, start):
    children = []
    for i in range(0, len(population), 2):
        dad = population[i]["genome"][1:-1]
        mom = population[i + 1]["genome"][1:-1]

        point1 = random.randint(0, len(dad) - 1)
        point2 = random.randint(0, len(dad) - 1)

        if point2 < point1:
            point1, point2 = point2, point1

        child1 = dad[point1:point2]
        child2 = dad[:point1] + dad[point2:]

        for j in mom:
            if j not in child1:
                child1.append(j)
            if j not in child2:
                child2.append(j)

        child1 = [start] + child1 + [start]
        child2 = [start] + child2 + [start]

        child1 = {"score": 0, "genome": child1}
        child2 = {"score": 0, "genome": child2}
        children = children + [child1, child2]

    population = population + children

    return population


def generate_city(num_cities):
    np.random.seed(0)
    cost_matrix = np.random.randint(1, 50, size=(num_cities, num_cities))
    cost_matrix = cost_matrix + cost_matrix.T
    np.fill_diagonal(cost_matrix, 0)
    return cost_matrix


if __name__ == "__main__":
    # Example usage:
    graph = [
        [0, 2, INT_MAX, 12, 5],
        [2, 0, 4, 8, INT_MAX],
        [INT_MAX, 4, 0, 3, 3],
        [12, 8, 3, 0, 10],
        [5, INT_MAX, 3, 10, 0],
    ]
    # graph = generate_city(50)
    print(genetic_alg(100, graph, 1000))
    print(graph)
