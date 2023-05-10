import PuzzleProblem as pp
import random
import time
import heapq
def general_search(problem, queueing_function, heuristic_function=None, show_info=False):
    initial_node = pp.MyTreeNode(problem.initial_state)
    nodes = [(0, (initial_node, 0))]  # (priority, (node, cost))
    visited = set()
    depth = 0

    while nodes:
        _, (node, cost) = heapq.heappop(nodes)

        if show_info:
            print("Expanding state:")
            heuristic_value = heuristic_function(node.state) if heuristic_function else None
            print_state_with_info(node.state, cost, heuristic=heuristic_value)

        if problem.goal_test(node.state):
            return {"state": node.state, "parent": node.parent, "cost": cost, "depth": depth, "success": True}

        visited.add(str(node.state))
        next_states = problem.get_next_states(node)
        nodes = queueing_function(nodes, next_states, visited, cost)
        depth = max(depth, cost+1)

    return {"success": False}

def uniform_cost_queueing_function(nodes, next_states, visited, current_cost):
    for successor in next_states:
        state_str = str(successor.state)
        if state_str not in visited:
            heapq.heappush(nodes, (current_cost + 1, (successor, current_cost + 1)))
    return nodes

def search_queueing_function(nodes, next_states, visited, current_cost, heuristic_function=None):
    for successor in next_states:
        state_str = str(successor.state)
        if state_str not in visited:
            heuristic = heuristic_function(successor) if heuristic_function else 0
            priority = current_cost + 1 + heuristic
            heapq.heappush(nodes, (priority, (successor, current_cost + 1)))
    return nodes

# def a_star_queueing_function(heuristic_function):
#     def queueing_function(nodes, next_states, visited, current_cost):
#         for successor in next_states:
#             state_str = str(successor.state)
#             if state_str not in visited:
#                 heuristic = heuristic_function(successor.state) if heuristic_function else 0
#                 priority = current_cost + 1 + heuristic
#                 heapq.heappush(nodes, (priority, (successor, current_cost + 1)))
#         return nodes
#     return queueing_function



def print_state_with_info(state, cost, heuristic=None):
    problem.print_state(state)
    print(f"g(n) = {cost}")
    if heuristic is not None:
        print(f"h(n) = {heuristic}")
    print()


def print_solution(solution, heuristic_function=None):
    if not solution["success"]:
        print("No solution found.")
    else:
        print("Solution found with cost:", solution["cost"])
        if heuristic_function:
            print("Depth:", solution["depth"])
            if solution["cost"] != 0:
                state = solution["state"]
                g_n = solution["cost"]
                h_n = heuristic_function(state)
                print_state_with_info(state, g_n, heuristic=h_n)
        else:
            state = solution["state"]
            g_n = solution["cost"]
            print_state_with_info(state, g_n)



if __name__ == "__main__":
    # initial_state = [
    #     [1, 2, 3],
    #     [4, 5, 6],
    #     [0, 7, 8]
    # ]
    initial_state = [
        [1, 2, 3],
        [5, 0, 6],
        [4, 7, 8]
    ]
    problem = pp.Problem(initial_state)


    start_time = time.time()
    solution = general_search(problem, uniform_cost_queueing_function,show_info=False)
    end_time = time.time()

    print_solution(solution)
    print("Execution time: {:.6f} seconds".format(end_time - start_time))

    start_time = time.time()
    solution = general_search(problem, search_queueing_function, heuristic_function=problem.misplaced_tile_heuristic, show_info=True)
    end_time = time.time()

    print("A* with Misplaced Tile heuristic:")
    print_solution(solution, problem.misplaced_tile_heuristic)
    print("Execution time: {:.6f} seconds\n".format(end_time - start_time))

    # A* with Manhattan Distance heuristic
    start_time = time.time()
    solution = general_search(problem, search_queueing_function, heuristic_function=problem.manhattan_distance_heuristic, show_info=True)
    end_time = time.time()

    print("A* with Manhattan Distance heuristic:")
    print_solution(solution, problem.manhattan_distance_heuristic)
    print("Execution time: {:.6f} seconds".format(end_time - start_time))