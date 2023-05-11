import PuzzleProblem as pp
import time
import heapq
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
def general_search(problem, queueing_function, heuristic_function=None, show_info=False):
    initial_node = pp.MyTreeNode(problem.initial_state)
    nodes = [(0, (initial_node, 0))]  # (priority, (node, cost))
    visited = set()
    expanded_nodes = 0

    while nodes:
        _, (node, cost) = heapq.heappop(nodes)
        expanded_nodes +=1
        if show_info:
            print("Expanding state:")
            heuristic_value = heuristic_function(problem, node.state) if heuristic_function else None
            print_state_with_info(node.state, cost, heuristic=heuristic_value)

        if problem.goal_test(node.state):
            return {"state": node.state, "parent": node.parent, "cost": cost, "expanded_nodes": expanded_nodes, "success" : True}

        visited.add(str(node.state))
        next_states = problem.get_next_states(node)
        nodes = queueing_function(nodes, next_states, visited, cost, problem, heuristic_function)  # Pass problem and heuristic_function here
    return {"success": False}


def search_queueing_function(nodes, next_states, visited, current_cost, problem, heuristic_function=None):
    for successor in next_states:
        state_str = str(successor.state)
        if state_str not in visited:
            heuristic = heuristic_function(problem, successor.state) if heuristic_function else 0  # Pass problem and successor.state
            priority = current_cost + 1 + heuristic
            heapq.heappush(nodes, (priority, (successor, current_cost + 1)))
    return nodes


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
        print("Expanded nodes:", solution["expanded_nodes"])
        if heuristic_function:
            print("Depth:", solution["cost"])
            if solution["cost"] != 0:
                state = solution["state"]
                g_n = solution["cost"]
                h_n = heuristic_function(state)
                print_state_with_info(state, g_n, heuristic=h_n)
        else:
            state = solution["state"]
            g_n = solution["cost"]
            print_state_with_info(state, g_n)

def test_algorithms(algorithms, initial_states):
    results = []

    for algorithm, heuristic in algorithms:
        for depth, initial_state in enumerate(initial_states):
            problem = pp.Problem(initial_state)
            start_time = time.time()
            solution = general_search(problem, search_queueing_function, heuristic_function=heuristic)
            end_time = time.time()

            execution_time = end_time - start_time
            expanded_nodes = solution["expanded_nodes"]

            result = {
                "Algorithm": algorithm,
                "Depth": depth + 1,
                "Execution Time": execution_time,
                "Expanded Nodes": expanded_nodes
            }
            results.append(result)

    return pd.DataFrame(results)



if __name__ == "__main__":
    algorithms = [
        ("UCS", None),
        ("A* Misplaced Tile", pp.Problem.misplaced_tile_heuristic),
        ("A* Manhattan Distance", pp.Problem.manhattan_distance_heuristic)
    ]
    initial_states = [
        [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ],
        [
            [1, 2, 3],
            [4, 5, 6],
            [0, 7, 8]
        ],
        [
            [1, 2, 3],
            [5, 0, 6],
            [4, 7, 8]
        ],
        [
            [1, 3, 6],
            [5, 0, 2],
            [4, 7, 8]
        ],
        [
            [1, 3, 6],
            [5, 0, 7],
            [4, 8, 2]
        ],
        [
            [1, 6, 7],
            [5, 0, 3],
            [4, 8, 2]
        ],
        [
            [7, 1, 2],
            [4, 8, 5],
            [6, 3, 0]
        ]
    ]
    results_df = test_algorithms(algorithms, initial_states)
    results_df.to_csv("algorithm_comparison.csv", index=False)
    plt.figure()
    sns.lineplot(data=results_df, x="Depth", y="Execution Time", hue="Algorithm", marker="o")
    plt.title("Time Complexity Comparison")
    plt.savefig("time_complexity_comparison.png")
    plt.close()

    # Expanded nodes plot
    plt.figure()
    sns.lineplot(data=results_df, x="Depth", y="Expanded Nodes", hue="Algorithm", marker="o")
    plt.title("Expanded Nodes Comparison")
    plt.savefig("expanded_nodes_comparison.png")
    plt.close()

    ##general test without pandas and plots.
    # problem = pp.Problem()
    # start_time = time.time()
    # solution = general_search(problem, search_queueing_function,heuristic_function=None ,show_info=False)
    # end_time = time.time()
    #
    # print_solution(solution)
    # print("Execution time: {:.6f} seconds".format(end_time - start_time))
    #
    # start_time = time.time()
    # solution = general_search(problem, search_queueing_function, heuristic_function=problem.misplaced_tile_heuristic, show_info=False)
    # end_time = time.time()
    #
    # print("A* with Misplaced Tile heuristic:")
    # print_solution(solution, problem.misplaced_tile_heuristic)
    # print("Execution time: {:.6f} seconds\n".format(end_time - start_time))
    #
    # # A* with Manhattan Distance heuristic
    # start_time = time.time()
    # solution = general_search(problem, search_queueing_function, heuristic_function=problem.manhattan_distance_heuristic, show_info=False)
    # end_time = time.time()
    #
    # print("A* with Manhattan Distance heuristic:")
    # print_solution(solution, problem.manhattan_distance_heuristic)
    # print("Execution time: {:.6f} seconds".format(end_time - start_time))

