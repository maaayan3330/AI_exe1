import search
import ex1  # ודאי שזה שם הקובץ שלך

def print_solution(solution):
    if solution:
        path = [n.action for n in solution.path()][1:]
        print("Solution found:")
        print("Length:", len(path))
        print("Path:", path)
    else:
        print("No solution found.")

def test_small_map():
    test_map = (
        (99, 99, 99, 99, 99, 99),
        (99, 98, 10, 98, 40, 99),
        (99, 98, 98, 20, 98, 99),
        (99, 98, 98, 98, 98, 99),
        (99, 98, 1, 98, 2, 99),
        (99, 99, 99, 99, 99, 99),
    )

    problem = ex1.create_pressure_plate_problem(test_map)
    solution = search.astar_search(problem, problem.h)
    print_solution(solution)

if __name__ == '__main__':
    test_small_map()
