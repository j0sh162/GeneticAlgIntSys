import numpy as np

def knapsack(weights, values, capacity):
    n = len(weights)
    # Initialize a 2D array to store the maximum value that can be obtained
    # for different weights and different items
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    # Build DP table in bottom-up manner
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(values[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    # Traceback to find items included in the knapsack
    included_items = []
    i, j = n, capacity
    while i > 0 and j > 0:
        if dp[i][j] != dp[i - 1][j]:
            included_items.append(i - 1)
            j -= weights[i - 1]
        i -= 1

    # Return the maximum value and the list of included items
    return dp[n][capacity], included_items


if __name__ == '__main__':
    # Example usage:
    capacity = 20 
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    weights = [2, 8, 3, 8, 1, 9, 3, 6, 5, 4]


    max_value, items = knapsack(weights, values, capacity)
    print("Maximum value:", max_value)
    print("Items included:", items)
