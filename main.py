import heapq
import random
import time
from itertools import chain

class Problem:
    def __init__(self, initial_state=None):
        if initial_state:
            self.initial_state = initial_state
        else:
            self.initial_state = self.generate_random_state()
        self.goal_state = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8]
        ]

    def generate_random_state(self):
        state = list(chain.from_iterable(self.goal_state))
        random.shuffle(state)
        return [state[i:i + 3] for i in range(0, 9, 3)]

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

def general_search(problem, queueing_function):
    nodes = [(0, (problem.initial_state, None, 0))]  # (priority, (state, parent, cost))
    visited = set()
    depth = 0

    while nodes:
        _, (state, parent, cost) = heapq.heappop(nodes)
        if problem.goal_test(state):
            return {"state": state, "parent": parent, "cost": cost, "depth": depth, "success": True}

        visited.add(str(state))
        successors = problem.successors(state)
        nodes = queueing_function(nodes, successors, visited, cost)
        depth = max(depth, cost + 1)

    return {"success": False}


def uniform_cost_queueing_function(nodes, successors, visited, current_cost):
    for successor in successors:
        state_str = str(successor)
        if state_str not in visited:
            heapq.heappush(nodes, (current_cost + 1, (successor, state_str, current_cost + 1)))
    return nodes

def print_solution(solution):
    if not solution["success"]:
        print("No solution found.")
    else:
        print("Solution found with cost:", solution["cost"])
        print("Depth:", solution["depth"])
        print("State:")
        for row in solution["state"]:
            print(row)


if __name__ == "__main__":
    initial_state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    problem = Problem(initial_state)

    start_time = time.time()
    solution = general_search(problem, uniform_cost_queueing_function)
    end_time = time.time()

    print_solution(solution)
    print("Execution time: {:.6f} seconds".format(end_time - start_time))