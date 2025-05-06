import time

import ex1
import search


def run_problem(func, targs=(), kwargs=None):
    if kwargs is None:
        kwargs = {}
    result = (-3, "default")
    try:
        result = func(*targs, **kwargs)

    except Exception as e:
        result = (-3, e)
    return result


# check_problem: problem, search_method, timeout
# timeout_exec: search_method, targs=[problem], timeout_duration=timeout
def solve_problems(problem, algorithm):
    for row in problem:
        print(row)

    try:
        p = ex1.create_pressure_plate_problem(problem)
    except Exception as e:
        print("Error creating problem: ", e)
        return None

    if algorithm == "gbfs":
        result = run_problem((lambda p: search.greedy_best_first_graph_search(p, p.h)),targs=[p])
    else:
        result = run_problem((lambda p: search.astar_search(p, p.h)), targs=[p])

    if result and isinstance(result[0], search.Node):
        solve = result[0].path()[::-1]
        solution = [pi.action for pi in solve][1:]
        print(len(solution), solution)
    else:
        print("no solution")


problem1 = (
    (99,99,99,99,99,99),
    (99,2,40,98,98,99),
    (99,99,99,10,98,99),
    (99,98,98,98,98,99),
    (99,20,98,98,1,99),
    (99,99,99,99,99,99),
)
# solution1: len(solution) = 16
problem2 = (
    (99,99,99,99,99,99,99,99,99,99,99,99,99,99,99),
    (99,98,98,98,99,99,99,99,99,99,99,99,99,99,99),
    (99,98,99,98,99,99,99,99,99,99,98,98,99,99,99),
    (99,98,99,98,98,99,25,98,99,99,98,98,98,99,99),
    (99,98,99,98,2,45,98,98,98,98,98,98,98,99,99),
    (99,98,99,99,99,99,98,98,99,99,99,42,99,99,99),
    (99,98,98,98,98,99,99,99,99,99,22,98,98,99,99),
    (99,99,99,99,98,99,98,98,98,99,98,98,98,99,99),
    (99,98,98,98,98,99,12,98,98,99,98,98,98,99,99),
    (99,98,99,99,23,98,98,15,98,99,99,41,99,99,99),
    (99,98,99,99,98,98,98,98,98,99,20,98,98,98,99),
    (99,98,99,99,98,98,99,98,98,99,98,98,10,98,99),
    (99,98,99,99,98,13,98,98,98,40,11,98,98,98,99),
    (99,98,43,98,98,98,98,98,98,99,21,98,98,1,99),
    (99,99,99,99,99,99,99,99,99,99,99,99,99,99,99),)
# solution2: len(solution) = 50


def main():
    start = time.time()
    problem = [problem1, problem2]
    for p in problem:
        for a in ['astar', 'gbfs']:
            solve_problems(p, a)
    end = time.time()
    print('Submission took:', end-start, 'seconds.')


if __name__ == '__main__':
    main()
