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

