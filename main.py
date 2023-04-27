import PuzzleProblem as pp
import random
import time
import heapq
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

def search_queueing_function(nodes, successors, visited, current_cost, heuristic_function=None):
    for successor in successors:
        state_str = str(successor)
        if state_str not in visited:
            heuristic = heuristic_function(successor) if heuristic_function else 0
            priority = current_cost + 1 + heuristic
            heapq.heappush(nodes, (priority, (successor, state_str, current_cost + 1)))
    return nodes

def a_star_queueing_function(heuristic_function):
    def queueing_function(nodes, successors, visited, current_cost):
        for successor in successors:
            state_str = str(successor)
            if state_str not in visited:
                heuristic = heuristic_function(successor) if heuristic_function else 0
                priority = current_cost + 1 + heuristic
                heapq.heappush(nodes, (priority, (successor, state_str, current_cost + 1)))
        return nodes
    return queueing_function

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
        [0, 7, 8]
    ]
    problem = pp.Problem(initial_state)


    start_time = time.time()
    solution = general_search(problem, uniform_cost_queueing_function)
    end_time = time.time()

    print_solution(solution)
    print("Execution time: {:.6f} seconds".format(end_time - start_time))

    start_time = time.time()
    solution = general_search(problem, a_star_queueing_function(problem.misplaced_tile_heuristic))
    end_time = time.time()

    print("A* with Misplaced Tile heuristic:")
    print_solution(solution)
    print("Execution time: {:.6f} seconds\n".format(end_time - start_time))

    # A* with Manhattan Distance heuristic
    start_time = time.time()
    solution = general_search(problem, a_star_queueing_function(problem.manhattan_distance_heuristic))
    end_time = time.time()

    print("A* with Manhattan Distance heuristic:")
    print_solution(solution)
    print("Execution time: {:.6f} seconds".format(end_time - start_time))