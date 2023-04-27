
import random
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

    def successors(self, state):
        successors = []
        i, j = self.find_zero(state)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y = i + dx, j + dy
            if 0 <= x < 3 and 0 <= y < 3:
                new_state = [row.copy() for row in state]
                new_state[i][j], new_state[x][y] = new_state[x][y], new_state[i][j]
                successors.append(new_state)
        return successors

    def find_zero(self, state):
        for i, row in enumerate(state):
            for j, cell in enumerate(row):
                if cell == 0:
                    return i, j

    def print_state(self, state):
        print("State:")
        for row in state:
            print(row)
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
                    correct_i, correct_j = divmod(cell, 3)
                    manhattan_distance += abs(i - correct_i) + abs(j - correct_j)
        return manhattan_distance