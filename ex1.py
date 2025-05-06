import ex1_check
import search
import utils

id = ["No numbers - I'm special!"]

""" Rules """
BLANK = 0
WALL = 99
FLOOR = 98
AGENT = 1
GOAL = 2
# LOCKED_DOORS = [40,...,49]
# PRESSED_PLATES = [30,...,39]
# PRESSURE_PLATES = [20,...,29]
# KEY_BLOCKS = [10,...,19]


class PressurePlateProblem(search.Problem):
    """This class implements a pressure plate problem"""

    def __init__(self, initial):
        # keep the metrix in self.map that it will be for all the functions
        """ Constructor only needs the initial state.
        Don't forget to set the goal or implement the goal test"""
        # initial - the all metrix
        self.map = initial
        # I want to pass the constructor not the all netrix just the - initial stats
        agent_placement = None
        key_blocks = []
        for i, row in enumerate(initial):
            for j, placement in enumerate(row):
                if placement == AGENT:
                    agent_placement = (i,j)
                if placement >= 10 and placement <= 19:
                    # i keep the placement of the cube and its number
                    key_blocks.append((i,j,placement))
                # i will keep the goal for later
                if placement == GOAL:
                    self.goal = (i,j)
        # so far I just collect the all informetion and now i will add it to states
        initial_state = (agent_placement, tuple(sorted(key_blocks)))
        # note - I keep the first item in the initial_state to be = the agent = state[0]
        search.Problem.__init__(self, initial_state)


    def successor(self, state):
        """ Generates the successor states returns [(action, achieved_states, ...)]"""
        utils.raiseNotDefined()

    def goal_test(self, state):
        """ given a state, checks if this is the goal state, compares to the created goal state returns True/False"""
        # i want to check if agent is on goal
        return state[0] == self.goal

    def h(self, node):
        """ This is the heuristic. It gets a node (not a state)
        and returns a goal distance estimate"""
        utils.raiseNotDefined()


def create_pressure_plate_problem(game):
    print("<<create_pressure_plate_problem")
    """ Create a pressure plate problem, based on the description.
    game - tuple of tuples as described in pdf file"""
    return PressurePlateProblem(game)


if __name__ == '__main__':
    ex1_check.main()
