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

# help with the drections
DIRECTIONS = {
    "R": (0, 1),
    "L": (0, -1),
    "U": (-1, 0),
    "D": (1, 0)
}



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
                if placement in KEY_BLOCKS:
                    # i keep the placement of the cube and its number
                    key_blocks.append((i,j,placement - 10))
                # i will keep the goal for later
                if placement == GOAL:
                    self.goal = (i,j)
        # keep info for later
        self.rows = len(self.map)
        self.cols = len(self.map[0])
        # keep the num of "pressure plates"
        self.pressure_plate_counts = self.count_by_type(self.map, PRESSURE_PLATES)
        # keep the num of "pressure plates"
        self.key_block_counts = self.count_by_type(self.map, KEY_BLOCKS)
        # keep 
        self.door_requirements = self.count_doors_and_required_plates(self.map)
        # so far I just collect the all informetion and now i will add it to states
        initial_state = (agent_placement, tuple(sorted(key_blocks)))
        # note - I keep the first item in the initial_state to be = the agent = state[0]
        search.Problem.__init__(self, initial_state)

    # this function is to keep the data i need
    def count_by_type(self, matrix, valid_range):
        counter = {}
        for row in matrix:
            for cell in row:
                if cell in valid_range:
                    block_type = cell % 10
                    counter[block_type] = counter.get(block_type, 0) + 1
        return counter

    # to keep track of the doors
    def count_doors_and_required_plates(self, matrix):
        plate_counter = {}
        door_counter = {}

        for row in matrix:
            for cell in row:
                if cell in PRESSURE_PLATES:
                    plate_type = cell % 10
                    plate_counter[plate_type] = plate_counter.get(plate_type, 0) + 1
                elif cell in LOCKED_DOORS:
                    door_type = cell % 10
                    door_counter[door_type] = door_counter.get(door_type, 0) + 1

        return {door_type: plate_counter.get(door_type, 0) for door_type in door_counter}


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
        if self.next_move_pressure_plates(state, direction):
            return results
        # case 4 - if the agent next stop is to a "key blocks" that have a "key block" after it or a wall
        # *cube after cube | *wall after cube | *worng pressuer number | *push a cube and its go behond the boundery
        if self.push_block_invalid(state, direction):
            return results
        # case 5 - if the agent next stop is to a locked door
        if self.locked_door(state, direction):
            return results
        

        # check now for good cases to insert to the states :
        row_of_agent , col_of_agent = state[0]
        direction_row, direction_col = DIRECTIONS[direction]

        # case 1 - the agent want to move to an empty place
        if self.map[row_of_agent + direction_row][col_of_agent + direction_col] == FLOOR:
            # keep the new placment of the agen
            new_agent_placement = (row_of_agent + direction_row, col_of_agent + direction_col)
            # keep the all info about the "key blockes"
            key_blocks = state[1]
            new_state = (new_agent_placement, key_blocks)
            results.append((direction, new_state))
        # case 2 - the agent want to push a "key block" to FLOOR and it is valid (it mean there is no wall/key block after the one he want to push) - we cannn push!!
        if self.map[row_of_agent + direction_row + 1][col_of_agent + direction_col + 1] == FLOOR:
            key_blocks = list(state[1])
            key_type = self.map[row_of_agent + direction_row][col_of_agent + direction_col] - 10

            # remove the position of the old cube
            key_blocks.remove((row_of_agent + direction_row, col_of_agent + direction_col, key_type))

            # add it to the new position
            key_blocks.append((row_of_agent + 2 * direction_row, col_of_agent + 2 * direction_col, key_type))

            new_state = ((row_of_agent + direction_row, col_of_agent + direction_col),tuple(sorted(key_blocks)))
            results.append((direction, new_state))


        # check for good cases that need a special update
        # case 1 - the agent push a "key block" and now it is on a pressure plates 
        # check what type of the  "key" we have

        # check if we push to the right pressure plates

        # to reduce 1 from the type door and check if to change it to floor + if it is the same type nakt it a wall


        

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
            if self.map[row_of_agent][col_of_agent + 1] in PRESSURE_PLATES: 
                return True
        elif direction == "L":
            if self.map[row_of_agent][col_of_agent - 1] in PRESSURE_PLATES: 
                return True
        elif direction == "U":
            if self.map[row_of_agent - 1][col_of_agent] in PRESSURE_PLATES: 
                return True
        elif direction == "D":
            if self.map[row_of_agent + 1][col_of_agent] in PRESSURE_PLATES: 
                return True
        return False

    # case 4
    def push_block_invalid(self, state, direction):
        row_of_agent , col_of_agent = state[0]
        direction_row, direction_col = DIRECTIONS[direction]

        # first check if the move push a cube
        if self.map[row_of_agent + direction_row][col_of_agent + direction_col] in KEY_BLOCKS:
            # first check if the placement after it is in the bounderis
            one_step_row , one_step_col = (row_of_agent + direction_row + direction_row), (col_of_agent + direction_col + direction_col)
            if not (0 <= one_step_row < self.rows and 0 <= one_step_col < self.cols):
                # the next step is out of bounderies for ROW and COL
                return True
            # so it is in boundry - check if there is a cube after it
            if self.map[one_step_row][one_step_col] in KEY_BLOCKS:
                return True
            # check if there is a wall after it
            if self.map[one_step_row][one_step_col] ==  WALL:
                return True
            # check if we push it to a wrong pressure
            if self.map[one_step_row][one_step_col] in PRESSURE_PLATES:
                plate_pressure = self.map[one_step_row][one_step_col]
                key_block = self.map[row_of_agent + direction_row][col_of_agent + direction_col]
                if (plate_pressure % 10) != (key_block % 10):
                    # they have diffrent numbers 
                    return True
        # it is all good
        return False

    # case 5
    def locked_door(self, state, direction):
        row_of_agent , col_of_agent = state[0]
        direction_row, direction_col = DIRECTIONS[direction]

        if self.map[row_of_agent + direction_row][col_of_agent + direction_col] in LOCKED_DOORS:
            # now i will do a check if the door is free to go or not
            type_door = (self.map[row_of_agent + direction_row][col_of_agent + direction_col]) % 10
            if self.door_requirements.get(type_door, 0) > 0 :
                # the door is locekd
                return True
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
