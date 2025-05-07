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
LOCKED_DOORS = list(range(40, 50))
PRESSED_PLATES = list(range(30, 40))
PRESSURE_PLATES = list(range(20, 30))
KEY_BLOCKS = list(range(10, 20))



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
        # keep info for later
        self.rows = len(self.map)
        self.cols = len(self.map[0])
        # so far I just collect the all informetion and now i will add it to states
        initial_state = (agent_placement, tuple(sorted(key_blocks)))
        # note - I keep the first item in the initial_state to be = the agent = state[0]
        search.Problem.__init__(self, initial_state)


    def successor(self, state):
        """ Generates the successor states returns [(action, achieved_states, ...)]"""
        # first thing - check for every UP DOWN LEFT RIGHT the all possible situtions
        new_states = []
        for direction in ["R", "L", "U", "D"]:
            possible_moves = self.helper_successor(state, direction)
            new_states.extend(possible_moves)
        return new_states
    
    def helper_successor(self, state , direction):
        results = []
        ##### check for wrong cases - for better time run : #####
        # case 1 - if the next step is out of the boundry of the metrix
        if not self.out_of_boundry(state, direction):
            return results
        # case 2 - if the next step of the agent is to wall 
        if self.next_move_wall(state, direction):
            return results
        # case 3 - if the agent next stop is to a "pressure plates"
        # case 4 - if the agent next stop is to a "key blocks" that have a "key block" after it or a wall
        # case 5 - if the agent next stop is to a locked door
        # case 6 - if the Agent push a "key block" on a "pressure plates" that not belong to him
        # case 7 - if the agent next move is to an "pressure plates"

        # check now for good cases to insert to the states :
        # case 1 - the agent want to move to an empty place
        # case 2 - the agent want to push a "key block" and it is valid (it mean there is no wall/key block after the one he want to push)

        # check for good cases that need a special update
        # case 1 - the agent push a "key block" and now it is on a pressure plates 
        

        ##################################### תחשבי אם כיסת את המצב של אםם זה אזור לחוץ כבר
        return results
    # helpper functions for helper seccessor
    # case 1 
    def out_of_boundry(self, state, direction):
        row_of_agent , col_of_agent = state[0]
        if direction == "R":
            return col_of_agent + 1 < self.cols
        elif direction == "L":
            return col_of_agent - 1 >= 0
        elif direction == "U":
            return row_of_agent - 1 >= 0
        elif direction == "D":
            return row_of_agent + 1 < self.rows
        # out of boundry
        return False
    
    # case 2 
    def next_move_wall(self, state, direction):
        row_of_agent , col_of_agent = state[0]
        if direction == "R":
            return self.map[row_of_agent][col_of_agent + 1] == WALL
        elif direction == "L":
            return self.map[row_of_agent][col_of_agent - 1] == WALL
        elif direction == "U":
            return self.map[row_of_agent - 1][col_of_agent] == WALL
        elif direction == "D":
            return self.map[row_of_agent + 1][col_of_agent] == WALL
        return False

    # case 3
    def next_move_pressure_plates(self, state, direction):
        row_of_agent , col_of_agent = state[0]
        if direction == "R":
            return self.map[row_of_agent][col_of_agent + 1] == 
        elif direction == "L":
            return self.map[row_of_agent][col_of_agent - 1] == WALL
        elif direction == "U":
            return self.map[row_of_agent - 1][col_of_agent] == WALL
        elif direction == "D":
            return self.map[row_of_agent + 1][col_of_agent] == WALL
        return False




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
