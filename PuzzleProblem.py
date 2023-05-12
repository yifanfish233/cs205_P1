#Part I use external library:
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
    def __init__(self, size = 3,initial_state=None):
        self.size = size
        self.goal_state = [[(i * size + j + 1) % (size * size) for j in range(size)] for i in range(size)]

        if initial_state:
            self.initial_state = initial_state
            print("Setting initial state:")
            self.print_state(initial_state)
        else:
            #if random state is not solvable, generate another one
            print("Generating random initial state:")
            temp = self.generate_random_state()
            while not self.check_solvable(temp, self.goal_state):
                print("Not solvable, generating another one")
                temp = self.generate_random_state()
            print("Solvable, setting initial state:")
            self.initial_state = temp
            self.print_state(self.initial_state)

    def generate_random_state(self):
        """
        Generate a random state
        :return:
        """
        state = [[None] * self.size for _ in range(self.size)]
        nums = list(range(self.size*self.size))
        random.shuffle(nums)
        for i in range(self.size):
            for j in range(self.size):
                state[i][j] = nums.pop()
        print("Generated random initial state:")
        self.print_state(state)
        return state

    def goal_test(self, state):
        return state == self.goal_state

    def get_next_states(self, node):
        """
        Get next states
        :param node:
        :return:
        """
        next_states = []
        i, j = self.find_zero(node.state)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y = i + dx, j + dy
            if 0 <= x < self.size and 0 <= y < self.size:
                # use copy to avoid shallow copy. Otherwise, the state will be changed
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
    def get_size(self):
        return self.size
    def print_state(self, state):
            for i in range(self.size):
                for j in range(self.size):
                    print(state[i][j], end=" ")
                print()

    def check_solvable(self,state, goal_state):
        """
        Check if the puzzle is solvable, source from https://www.geeksforgeeks.org/check-instance-8-puzzle-solvable/
        :param state:
        :param goal_state:
        :return:
        """
        def inversion_counter(puzzle_state):
            flat_puzzle = [tile for row in puzzle_state for tile in row if tile != 0]
            inversions = 0
            for i in range(len(flat_puzzle)):
                for j in range(i + 1, len(flat_puzzle)):
                    if flat_puzzle[i] > flat_puzzle[j]:
                        inversions += 1
            return inversions

        initial_inversions = inversion_counter(state)
        goal_inversions = inversion_counter(goal_state)

        return initial_inversions % 2 == goal_inversions % 2

    def misplaced_tile_heuristic(self, state):
        misplaced_tiles = sum(
            1 for i, row in enumerate(state) for j, cell in enumerate(row)
            if cell != 0 and cell != self.goal_state[i][j]
        )
        return misplaced_tiles

    def manhattan_distance_heuristic(self, state):
        #Manhattan distance is the sum of the absolute values of the horizontal and vertical distance for each tile.
        manhattan_distance = 0
        for i, row in enumerate(state):
            for j, cell in enumerate(row):
                if cell != 0:
                    correct_i = (cell - 1) // self.size
                    correct_j = (cell - 1) % self.size
                    manhattan_distance += abs(i - correct_i) + abs(j - correct_j)
        return manhattan_distance