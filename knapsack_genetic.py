import random

def generate_population(count_items, population_size):
    population = []
    for i in range(population_size):
        genome = ""
        for j in range(count_items):
            if random.random() >= 0.5:
                genome += str(1)
            else:
                genome += str(0)
        population.append(genome)
    return population

def cost_eval(genome, count_items, max_weight, weights, values):
    if len(genome) > count_items:
        return 0

    genome_weight = 0
    genome_value = 0

    index = 0
    for gene in genome:
        if int(gene) == 0:
            index += 1
            continue
        elif int(gene) == 1:
            genome_weight += weights[index]
            genome_value += values[index]
            if genome_weight > max_weight:
                genome_value = 0
                break
        index += 1
    return genome_value


W = 15
weights = [1, 2, 3, 4, 5]
values = [1, 2, 3, 4, 5]
count_items = 5
pop_size = 10
population = generate_population(count_items, pop_size)

for i in range(pop_size):
    print(population[i], ":", cost_eval(population[i], count_items, W, weights, values))

