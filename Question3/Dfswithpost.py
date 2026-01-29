from collections import deque

class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None


def build_tree(values):
    if not values or values[0] is None:
        return None

    root = TreeNode(values[0])
    queue = deque([root])
    i = 1

    while queue and i < len(values):
        node = queue.popleft()

        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1

        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1

    return root




class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def minServiceCenters(self, root):
        self.centers = 0

        def dfs(node):
            if not node:
                return 2  # covered

            left = dfs(node.left)
            right = dfs(node.right)

            if left == 0 or right == 0:
                self.centers += 1
                return 1  # has service center

            if left == 1 or right == 1:
                return 2  # covered

            return 0  # needs service

        # If root still needs service, place one
        if dfs(root) == 0:
            self.centers += 1

        return self.centers

tree_vals = [0, 0, None, 0, None, 0, None, None, 0]

root = build_tree(tree_vals)

sol = Solution()
print(sol.minServiceCenters(root))
