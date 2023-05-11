import time
import general_search_alg as gs
import PuzzleProblem as pp
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
def test_algorithms(algorithms, initial_states):
    results = []
    for algorithm, heuristic in algorithms:
        for depth, initial_state in enumerate(initial_states):
            problem = pp.Problem(initial_state)
            start_time = time.time()
            solution = gs.general_search(problem, gs.search_queueing_function, heuristic_function=heuristic)
            end_time = time.time()
            execution_time = (end_time - start_time)* 1000
            expanded_nodes = solution["expanded_nodes"]
            max_queue_size = solution["max_queue_size"]
            result = {
                "Algorithm": algorithm,
                "Depth": solution["cost"],
                "Execution Time(ms)": round(execution_time, 3),
                "Expanded Nodes": expanded_nodes,
                "Max Queue Size": max_queue_size
            }
            results.append(result)

    return pd.DataFrame(results)

def main():
    while True:
        print("\n--- 8-Puzzle Solver ---")
        print("1. Custom Puzzle Solver")
        print("2. Random Puzzle Solver")
        print("3. Run Tests")
        print("4. Quit")
        choice = input("Please select an option: ")

        if choice == '1':
            initial_state = input("Enter your initial state (e.g., 1,2,3,4,5,6,7,8,0 for 1 2 3 | 4 5 6 | 7 8 0): ")
            # Convert string to 2D list
            initial_state = [list(map(int, initial_state.split(',')))[i:i+3] for i in range(0, 9, 3)]
            print("1. UCS")
            print("2. A* Misplaced Tile")
            print("3. A* Manhattan Distance")
            algorithm_choice = input("Choose an algorithm: ")
            problem = pp.Problem(initial_state)
            if algorithm_choice == '1':
                gs.general_search(problem, gs.search_queueing_function, heuristic_function=None, show_info=True)
                break
            elif algorithm_choice == '2':
                gs.general_search(problem, gs.search_queueing_function, heuristic_function=problem.misplaced_tile_heuristic, show_info=True)
                break
            elif algorithm_choice == '3':
                gs.general_search(problem, gs.search_queueing_function, heuristic_function=problem.manhattan_distance_heuristic, show_info=True)
                break
            else:
                print("Invalid algorithm choice.")
                break

        elif choice == '2':
            print("1. UCS")
            print("2. A* Misplaced Tile")
            print("3. A* Manhattan Distance")
            algorithm_choice = input("Choose an algorithm: ")
            problem = pp.Problem()
            if algorithm_choice == '1':
                solution = gs.general_search(problem, gs.search_queueing_function, heuristic_function=None, show_info=True)
                gs.print_solution(solution, heuristic_function=None)
                break
            elif algorithm_choice == '2':
                solution = gs.general_search(problem, gs.search_queueing_function, heuristic_function=problem.misplaced_tile_heuristic, show_info=True)
                gs.print_solution(solution, heuristic_function=problem.misplaced_tile_heuristic)
                break
            elif algorithm_choice == '3':
                solution = gs.general_search(problem, gs.search_queueing_function, heuristic_function=problem.manhattan_distance_heuristic, show_info=True)
                gs.print_solution(solution, heuristic_function=problem.manhattan_distance_heuristic)
                break
            else:
                print("Invalid algorithm choice.")
                break
        elif choice == '3':
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
                ],
                [
                    [0, 7, 2],
                    [4, 6, 1],
                    [3, 5, 8]
                ]
            ]
            results_df = test_algorithms(algorithms, initial_states)
            results_df.to_csv("algorithm_comparison.csv", index=False)
            plt.figure()
            sns.lineplot(data=results_df, x="Depth", y="Execution Time(ms)", hue="Algorithm", marker="o")
            plt.title("Time Complexity Comparison")
            plt.savefig("time_complexity_comparison.png")
            plt.close()

            # Expanded nodes plot
            plt.figure()
            sns.lineplot(data=results_df, x="Depth", y="Expanded Nodes", hue="Algorithm", marker="o")
            plt.title("Expanded Nodes Comparison")
            plt.savefig("expanded_nodes_comparison.png")
            plt.close()
            # Max Queue Size plot
            plt.figure()
            sns.lineplot(data=results_df, x="Depth", y="Max Queue Size", hue="Algorithm", marker="o")
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


