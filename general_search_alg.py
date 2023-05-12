import PuzzleProblem as pp
import heapq
def general_search(problem, queueing_function, heuristic_function=None, show_info=False):
    """
    General search algorithm
    :param problem: an instance of the problem being solved
    :param queueing_function: a function that determines how to add nodes to the queue
    :param heuristic_function: a heuristic function used by the A* algorithm
    :param show_info: boolean indicating whether to print intermediate information
    :return: dictionary containing details about the solution
    """
    initial_node = pp.MyTreeNode(problem.initial_state)
    # (priority, (node, cost))
    nodes = [(0, (initial_node, 0))]
    visited = set()
    expanded_nodes = 0
    max_queue_size = 0
    while nodes:
        _, (node, cost) = heapq.heappop(nodes)
        expanded_nodes += 1
        max_queue_size = max(max_queue_size, len(nodes))
        if show_info:
            print("Expanding state:")
            heuristic_value = heuristic_function(problem, node.state) if heuristic_function else None
            print_state_with_info(node.state, cost, heuristic=heuristic_value)

        if problem.goal_test(node.state):
            return {"state": node.state, "parent": node.parent, "cost": cost, "expanded_nodes": expanded_nodes, "max_queue_size": max_queue_size, "success": True}

        visited.add(str(node.state))
        next_states = problem.get_next_states(node)
        nodes = queueing_function(nodes, next_states, visited, cost, problem, heuristic_function)
    return {"success": False,"max_queue_size": max_queue_size}


def search_queueing_function(nodes, next_states, visited, current_cost, problem, heuristic_function=None):
    """
    Search queueing function - decides how nodes are added to the queue
    :param nodes: list of current nodes in the queue
    :param next_states: list of next states that can be reached from the current state
    :param visited: set of visited states
    :param current_cost: current cost g(n) for the current state
    :param problem: an instance of the problem being solved
    :param heuristic_function: a heuristic function used by the A* algorithm
    :return: updated list of nodes
    """
    for successor in next_states:
        state_str = str(successor.state)
        if state_str not in visited:
            heuristic = heuristic_function(problem, successor.state) if heuristic_function else 0  # hard code 0 for UCS
            priority = current_cost + 1 + heuristic
            heapq.heappush(nodes, (priority, (successor, current_cost + 1)))
    return nodes

def print_state(state):
    """
    :param state:
    :return: None, Prints the current state.
    """
    n = len(state)
    for i in range(n):
        for j in range(n):
            print(state[i][j], end=" ")
        print()

def print_state_with_info(state, cost, heuristic=None):
    """
    Prints the current state along with cost and heuristic information
    :param state: the current state
    :param cost: the current cost to reach the state
    :param heuristic: the heuristic value of the current state
    :return: None
    """
    print_state(state)
    print(f"g(n) = {cost}")
    if heuristic is not None:
        print(f"h(n) = {heuristic}")
        print("f(n) =", cost + heuristic)
    print()

def print_solution(solution, problem, heuristic_function=None):
    """
    :param solution:
    :param problem:
    :param heuristic_function:
    :return:
    """
    if not solution["success"]:
        print("No solution found.")
    else:
        print("Solution found with cost:", solution["cost"])
        print("Expanded nodes:", solution["expanded_nodes"])
        print("Max Queue Size:", solution["max_queue_size"])
        if heuristic_function:
            print("Depth:", solution["cost"])
            if solution["cost"] != 0:
                state = solution["state"]
                g_n = solution["cost"]
                h_n = heuristic_function(problem,state)
                print_state_with_info(state, g_n, heuristic=h_n)
        else:
            state = solution["state"]
            g_n = solution["cost"]
            print_state_with_info(state, g_n)

        def generate_optimal_path(node):
            optimal_path = [node]
            while node.parent is not None:
                node = node.parent
                optimal_path.append(node)
            return optimal_path[::-1]  # Reverse the path

        # Generate the optimal path
        optimal_path = generate_optimal_path(solution["parent"])
        print("\nOptimal Path:")
        for i, node in enumerate(optimal_path):
            print(f"\nStep {i}:")
            print_state(node.state)
        print(f"\nStep {i+1}: Goal State")
        print_state(problem.goal_state)

