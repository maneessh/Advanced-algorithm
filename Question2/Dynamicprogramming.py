
"""You are given a list of tile multipliers.
Each tile has a number on it.
When you remove (burst) a tile, you earn points equal to:
left tile value X current tile value Xright tile value
After removing a tile, the remaining tiles become neighbors.
Your goal is to remove all tiles in an order that gives the maximum total points.
"""

"""This problem is solved using interval dynamic programming,
 where we maximize points by considering each tile as the last removal in a subarray 
 and combining optimal solutions of left and right subproblems."""
def max_points(tile_multipliers):
    nums = [1] + tile_multipliers + [1]
    n = len(nums)

    # DP table
    dp = [[0] * n for _ in range(n)]

    # Length of interval
    for length in range(2, n):
        for i in range(0, n - length):
            j = i + length
            for k in range(i + 1, j):
                dp[i][j] = max(
                    dp[i][j],
                    dp[i][k] + dp[k][j] + nums[i] * nums[k] * nums[j]
                )

    return dp[0][n - 1]

#According to the first example
tile_multipliers = [3, 1, 5, 8]
print(max_points(tile_multipliers))

#According to the second example
tile_multipliers = [1, 5]
print(max_points(tile_multipliers))

