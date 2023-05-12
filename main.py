import general_search_alg as gs
import PuzzleProblem as pp
#part I use external library:
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
def test_algorithms(algorithms, initial_states, sizes):
    """
    Tests different algorithms on a set of 8-puzzle problems
    :param algorithms: list of algorithms to test
    :param initial_states: list of initial states for the problems
    :param sizes: list of sizes of the problems
    :return: a dataframe containing the results of the tests
    """
    results = []
    for algorithm, heuristic in algorithms:
        for size, initial_state in zip(sizes, initial_states):
            problem = pp.Problem(size, initial_state)
            start_time = time.time()
            solution = gs.general_search(problem, gs.search_queueing_function, heuristic_function=heuristic)
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000
            expanded_nodes = solution["expanded_nodes"]
            max_queue_size = solution["max_queue_size"]
            result = {
                "Algorithm": algorithm,
                "Size": size,
                "Depth": solution["cost"],
                "Execution Time(ms)": round(execution_time, 3),
                "Expanded Nodes": expanded_nodes,
                "Max Queue Size": max_queue_size
            }
            results.append(result)

    return pd.DataFrame(results)
def call_algorithm(algorithm_choice, initial_state, size):
    """
    Calls the chosen algorithm on the specified problem
    :param algorithm_choice: the chosen algorithm
    :param initial_state: the initial state of the problem
    :param size: the size of the problem
    :return: None
    """
    problem = pp.Problem(size=size, initial_state=initial_state)
    if algorithm_choice == '1':
        solution = gs.general_search(problem, gs.search_queueing_function, heuristic_function=None, show_info=True)
        gs.print_solution(solution,problem, heuristic_function=None)

    elif algorithm_choice == '2':
        solution = gs.general_search(problem, gs.search_queueing_function,
                                     heuristic_function=pp.Problem.misplaced_tile_heuristic, show_info=True)
        gs.print_solution(solution,problem, heuristic_function=pp.Problem.misplaced_tile_heuristic)

    elif algorithm_choice == '3':
        solution = gs.general_search(problem, gs.search_queueing_function,
                                     heuristic_function=pp.Problem.manhattan_distance_heuristic, show_info=True)
        gs.print_solution(solution,problem, heuristic_function=pp.Problem.manhattan_distance_heuristic)

    else:
        print("Invalid algorithm choice. Stop")

def main():
    while True:
        print("\n--- 8-Puzzle Solver ---")
        print("1. Random Puzzle Solver")
        print("2. Run Tests")
        print("--- n-Puzzle Solver ---")
        print("3. Custom Puzzle Solver")
        print("4. Quit")
        choice = input("Please select an option: ")

        if choice == '3':
            print("warning, this part will take a long time to run, please don't push so hard!")
            size = int(input("Enter the size of the puzzle (e.g., 3 for an 8-puzzle, 4 for a 15-puzzle, 5 for a 24-puzzle etc.): "))
            is_random = input("Would you like to generate a random puzzle? (y/n): ")
            if is_random == 'y':
                initial_state = None
            else:
                initial_state = input(
                    f"Enter your initial state for a {size}x{size} puzzle (e.g., 1,2,3,4,5,6,7,8,0 for 1 2 3 | 4 5 6 | 7 8 0): ")
            # Convert string to 2D list
                initial_state = [list(map(int, initial_state.split(',')))[i:i + size] for i in range(0, size * size, size)]
                if len([num for row in initial_state for num in row]) != size * size:
                    raise ValueError("The provided initial state does not match your puzzle size.")
                    break

            print("1. UCS")
            print("2. A* Misplaced Tile")
            print("3. A* Manhattan Distance")
            algorithm_choice = input("Choose an algorithm: ")
            call_algorithm(algorithm_choice, initial_state,size)
            break

        elif choice == '1':
            print("1. UCS")
            print("2. A* Misplaced Tile")
            print("3. A* Manhattan Distance")
            algorithm_choice = input("Choose an algorithm: ")
            call_algorithm(algorithm_choice,initial_state=None,size=3)
            break
        elif choice == '2':
            algorithms = [
                ("UCS", None),
                ("A* Misplaced Tile", pp.Problem.misplaced_tile_heuristic),
                ("A* Manhattan Distance", pp.Problem.manhattan_distance_heuristic)
            ]
            # 8-puzzle initial states with different depths from the project description.
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
                ],
                [
                    [0, 7, 2],
                    [4, 6, 1],
                    [3, 5, 8]
                ]
            ]
            sizes = [3] * len(initial_states)
            print("Running tests of 8-puzzle game...")
            results_df = test_algorithms(algorithms, sizes=sizes, initial_states=initial_states)
            results_df.to_csv("algorithm_comparison.csv", index=False)
            print("Generating plots...")
            plt.figure()
            ax = sns.lineplot(data=results_df, x="Depth", y="Execution Time(ms)", hue="Algorithm", marker="o")
            #source from https://www.geeksforgeeks.org/matplotlib-pyplot-fill_between-in-python/
            ax.fill_between(results_df["Depth"], 0, results_df["Execution Time(ms)"], where=results_df["Depth"] >= 16, color='red', alpha=0.3)
            plt.text(18, ax.get_ylim()[1]*0.05, "Hard Depth", color='red', fontsize=12)
            plt.title("Time Complexity Comparison")
            plt.savefig("time_complexity_comparison.png")
            plt.close()

            # Expanded nodes plot
            plt.figure()
            ax = sns.lineplot(data=results_df, x="Depth", y="Expanded Nodes", hue="Algorithm", marker="o")
            ax.fill_between(results_df["Depth"], 0, results_df["Expanded Nodes"], where=results_df["Depth"] >= 16, color='red', alpha=0.3)
            plt.text(18, ax.get_ylim()[1]*0.1, "Hard Depth", color='red', fontsize=12)
            plt.title("Expanded Nodes Comparison")
            plt.savefig("expanded_nodes_comparison.png")
            plt.close()
            # Max Queue Size plot
            plt.figure()
            ax = sns.lineplot(data=results_df, x="Depth", y="Max Queue Size", hue="Algorithm", marker="o")
            ax.fill_between(results_df["Depth"], 0, results_df["Max Queue Size"], where=results_df["Depth"] >= 16, color='red', alpha=0.3)
            plt.text(18, ax.get_ylim()[1]*0.2, "Hard Depth", color='red', fontsize=12)
            plt.title("Max Queue Size Comparison")
            plt.savefig("max_queue_size_comparison.png")
            plt.close()
            print("Results saved to algorithm_comparison.csv, time_complexity_comparison.png, expanded_nodes_comparison.png and max_queue_size_comparison.png")
            break

        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
