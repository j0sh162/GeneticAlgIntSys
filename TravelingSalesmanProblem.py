import sys

def tsp(graph, start):
    n = len(graph)
    # Initialize memoization table with -1
    memo = [[-1] * (1 << n) for _ in range(n)]

    # Helper function to solve TSP recursively
    def tsp_helper(curr, visited):
        if visited == (1 << n) - 1:  # All cities have been visited
            return graph[curr][start]
        
        if memo[curr][visited] != -1:  # Check if result already exists in memo
            return memo[curr][visited]

        min_cost = sys.maxsize
        for city in range(n):
            if (visited >> city) & 1 == 0:  # Check if city has not been visited
                cost = graph[curr][city] + tsp_helper(city, visited | (1 << city))
                min_cost = min(min_cost, cost)

        memo[curr][visited] = min_cost
        return min_cost

    # Start with the first city and visit all other cities
    return tsp_helper(start, 1 << start)



if __name__ == '__main__':
    # Example usage:
    graph = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    start_city = 0

    min_cost = tsp(graph, start_city)
    print("Minimum cost of traveling salesman tour:", min_cost)
