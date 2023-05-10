
import random


class MyTreeNode:
    def __init__(self, state, parent=None):
        """
        Initialize a tree node with a state
        :param state: the puzzle state
        :param parent: the parent node
        """
        self.state = state
        self.parent = parent
        self.children = []
        self.visited = False

    def __lt__(self, other):
        """
        Customized comparison functions
        :param other: the other tree node
        :return: which one is smaller. if current one is smaller, return True; otherwise, return False
        """
        return self.state < other.state

class Problem:
    def __init__(self, initial_state=None):
        self.goal_state = [
            [1,2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ]
        if initial_state:
            self.initial_state = initial_state
            print("Setting initial state:")
            self.print_state(initial_state)
        else:
            self.initial_state = self.generate_random_state()

    def generate_random_state(self):
        state = [[None] * 3 for _ in range(3)]
        nums = list(range(9))
        random.shuffle(nums)
        for i in range(3):
            for j in range(3):
                state[i][j] = nums.pop()
        print("Generated random initial state:")
        self.print_state(state)
        return state

    def goal_test(self, state):
        return state == self.goal_state

    def get_next_states(self, node):
        next_states = []
        i, j = self.find_zero(node.state)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y = i + dx, j + dy
            if 0 <= x < 3 and 0 <= y < 3:
                new_state = [row.copy() for row in node.state]
                new_state[i][j], new_state[x][y] = new_state[x][y], new_state[i][j]
                new_node = MyTreeNode(new_state, node)
                next_states.append(new_node)
        return next_states

    def find_zero(self, state):
        for i, row in enumerate(state):
            for j, cell in enumerate(row):
                if cell == 0:
                    return i, j

    def print_state(self, state, representation="grid"):
        if representation == "list":
            for row in state:
                print(row)
        elif representation == "grid":
            for i in range(3):
                for j in range(3):
                    print(state[i][j], end=" ")
                print()
        else:
            print("Invalid representation.")

    def misplaced_tile_heuristic(self, state):
        misplaced_tiles = sum(
            1 for i, row in enumerate(state) for j, cell in enumerate(row)
            if cell != 0 and cell != self.goal_state[i][j]
        )
        return misplaced_tiles

    def manhattan_distance_heuristic(self, state):
        manhattan_distance = 0
        for i, row in enumerate(state):
            for j, cell in enumerate(row):
                if cell != 0:
                    correct_i, correct_j = divmod(cell - 1, 3)
                    manhattan_distance += abs(i - correct_i) + abs(j - correct_j)
        return manhattan_distance

