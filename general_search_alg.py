import PuzzleProblem as pp
import heapq
def general_search(problem, queueing_function, heuristic_function=None, show_info=False):
    initial_node = pp.MyTreeNode(problem.initial_state)
    nodes = [(0, (initial_node, 0))]  # (priority, (node, cost))
    visited = set()
    expanded_nodes = 0
    max_queue_size = 0
    while nodes:

        _, (node, cost) = heapq.heappop(nodes)
        expanded_nodes +=1
        max_queue_size = max(max_queue_size, len(nodes))
        if show_info:
            print("Expanding state:")
            # heuristic_value = heuristic_function(problem, node.state) if heuristic_function else None
            heuristic_value = heuristic_function(problem,node.state) if heuristic_function else None
            print_state_with_info(node.state, cost, heuristic=heuristic_value)

        if problem.goal_test(node.state):
            return {"state": node.state, "parent": node.parent, "cost": cost, "expanded_nodes": expanded_nodes, "max_queue_size": max_queue_size, "success": True}

        visited.add(str(node.state))
        next_states = problem.get_next_states(node)
        nodes = queueing_function(nodes, next_states, visited, cost, problem, heuristic_function)
    return {"success": False,"max_queue_size": max_queue_size}


def search_queueing_function(nodes, next_states, visited, current_cost, problem, heuristic_function=None):
    for successor in next_states:
        state_str = str(successor.state)
        if state_str not in visited:
            heuristic = heuristic_function(problem, successor.state) if heuristic_function else 0  # hard code 0 for UCS
            priority = current_cost + 1 + heuristic
            heapq.heappush(nodes, (priority, (successor, current_cost + 1)))
    return nodes

def print_state(state):
    n = len(state)
    for i in range(n):
        for j in range(n):
            print(state[i][j], end=" ")
        print()

def print_state_with_info(state, cost, heuristic=None):
    print_state(state)
    print(f"g(n) = {cost}")
    if heuristic is not None:
        print(f"h(n) = {heuristic}")
    print()

def print_solution(solution,problem, heuristic_function=None):
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
