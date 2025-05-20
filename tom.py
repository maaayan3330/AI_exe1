import ex1_check
import search
import utils

id = ["209379239"]

""" Rules """
BLANK = 0
WALL = 99
FLOOR = 98
AGENT = 1
GOAL = 2
LOCKED_DOORS = list(range(40, 50))
PRESSED_PLATES = list(range(30, 40))
PRESSURE_PLATES = list(range(20, 30))
KEY_BLOCKS = list(range(10, 20))
ACTION_OFFSETS = {
            'U': (-1, 0),
            'D': (1, 0),
            'L': (0, -1),
            'R': (0,1)
        }
 
class PressurePlateProblem(search.Problem):
    """This class implements a pressure plate problem"""

    def __init__(self, initial):
        """ Constructor for the class"""

        # class attributes
        self.map = initial
        self.row_len, self.col_len = len(initial), len(initial[0])
        self.goal = None
        self.pressure_plates_counters = self.count_pressure_plates(self.map)
        self.old_states = set()
        self.doors_pos = self.count_doors(self.map)
        self.plates_pos = self.count_plates_for_class(self.map)
        self.key_blocks_initial = self.count_key_blocks_for_class(self.map)
        self.agent_pos_initial = None

        # initialize objects for state tupple
        agent_pos = None
        key_blocks_pos = []
        open_doors = frozenset()
        pressure_plates = frozenset()

        # iterate through the map to find agent, goal and key blocks
        for i, row in enumerate(self.map):
            for j, cell in enumerate(row):
                if(cell == AGENT): # found agent
                    agent_pos = (i, j)
                elif(cell == GOAL):
                    self.goal = (i,j) # save goal position
                elif(cell in KEY_BLOCKS):
                    key_blocks_pos.append(((cell % 10), (i,j))) # found key block - add the value of it and position
       
        if agent_pos is None:
            raise ValueError("Agent position not found in the map.")

        if self.goal is None:
            raise ValueError("Goal position not found in the map.")
                   
        # compute the state and initialize the game with it
        key_blocks_pos = tuple(sorted(key_blocks_pos)) # order blocks for consistency
        self.agent_pos_initial = agent_pos
        initial_state = (agent_pos, key_blocks_pos, open_doors, pressure_plates)
        search.Problem.__init__(self, initial_state, goal=self.goal)
   
    def count_pressure_plates(self, game_map):
        """Counts for each door id how many pressure plates are there in total"""
        # initialize dictionaries
        plates_count = {}
        pressure_plates = {}

        # count plates by id
        for row in game_map:
            for cell in row:
                if cell in PRESSURE_PLATES:
                    plate_id = cell % 10
                    plates_count[plate_id] = plates_count.get(plate_id, 0) + 1
       
        # count doors and assign the counts
        for row in game_map:
            for cell in row:
                if cell in LOCKED_DOORS:
                    door_id = cell % 10
                    if door_id not in pressure_plates:
                        pressure_plates[door_id] = plates_count.get(door_id, 0)
        return pressure_plates

    def count_doors(self, game_map):
        """Returns list of door ids and their positions"""
        doors = []
        for i in range(self.row_len):
            for j in range(self.col_len):
                cell = game_map[i][j]
                cell_id = cell % 10
                if(cell in LOCKED_DOORS):
                    doors.append((cell_id, (i, j)))
        return doors

    def count_plates_for_class(self, game_map):
        """Returns list of plate ids and their position"""
        plates = []
        for i in range(self.row_len):
            for j in range(self.col_len):
                cell = game_map[i][j]
                cell_id = cell % 10
                if(cell in PRESSURE_PLATES):
                    plates.append((cell_id, (i, j)))
        return plates

    def count_key_blocks_for_class(self, game_map):
        """Returns a list of key block ids and their position"""
        key_blocks = []
        for i in range(self.row_len):
            for j in range(self.col_len):
                cell = game_map[i][j]
                cell_id = cell % 10
                if(cell in KEY_BLOCKS):
                    key_blocks.append((cell_id, (i, j)))
        return key_blocks

        pass

    def successor(self, state):
        """Generates the successor states returns [(action, achieved_states, ...)]"""
        # initialize states list, the map of the state
        successor_states = []
        actions = ['L', 'R', 'U', 'D']
        real_map = self.compute_real_map(state)

        # for each case in {L, R, U, D}, validate the move. if passed tests, compute the state and append to states the tupple (action, computed_state)
        for action in actions:
            # call helper function that validates action
            if not(self.validate_move(action, state, real_map)):
                continue

            # call helper function to compute state
            new_state = self.compute_state(action, state, real_map)

            # check if already visited this state in the set. If not, add to set
            if((action, new_state) in self.old_states):
                continue

            # append to states: (action, computed_state)
            successor_states.append((action, new_state))
            self.old_states.add((action, new_state))

        # return state
        return successor_states
   
    def compute_real_map(self, state):
        """Returns a map of the given state"""
        # compute agent position, open doors and pressed pressure plates
        agent_row, agent_col = state[0]
        key_blocks_pos = state[1]
        open_doors = state[2]
        pressure_plates = dict(state[3])

        # create a mutable copy of the initial map
        copy_map = [list(row) for row in self.map]

        # update doors to FLOOR if open
        for door_id, (i, j) in self.doors_pos:
            if door_id in open_doors:
                copy_map[i][j] = FLOOR
       
        # update initial agent position to FLOOR
        i, j = self.agent_pos_initial
        copy_map[i][j] = FLOOR

        # update initial key block positions to FLOOR
        for block_id, (i, j) in self.key_blocks_initial:
            copy_map[i][j] = FLOOR

        # update real key blocks position from current state
        for block_id, (block_row, block_col) in key_blocks_pos:
            if self.map[block_row][block_col] in PRESSURE_PLATES:
                copy_map[block_row][block_col] = WALL
            else:
                copy_map[block_row][block_col] = 10 + block_id

        # update agent's position
        copy_map[agent_row][agent_col] = AGENT

        return copy_map

    def validate_move(self, action, state, game_map):
        """Validates move in the fitting direction"""
        # check if action not in action offsets
        if action not in ACTION_OFFSETS:
            raise ValueError(f"Invalid action: {action}")
       
        # compute variables from state
        action_row, action_col = ACTION_OFFSETS[action]
        agent_row, agent_col = state[0]
        key_blocks = state[1]
        target_row = agent_row + action_row
        target_col = agent_col + action_col

        # validate target cell
        if not self.validate_target_cell(target_row, target_col, game_map):
            return False

        # if target cell is a key block
        if game_map[target_row][target_col] in KEY_BLOCKS:
            # compute new values for the pushed block
            pushed_row = agent_row + (2 * action_row)
            pushed_col = agent_col + (2 * action_col)
            key_block_id = game_map[target_row][target_col] % 10

            # validate pushed cell
            if not self.validate_pushed_cell(pushed_row, pushed_col, key_blocks, key_block_id, game_map):
                return False
       
        # check if block is pushed to a dead end
        if self.validate_dead_end(state, action, game_map):
            return False

        # passed all tests
        return True

    def validate_target_cell(self, target_row, target_col, game_map):
        """Helper function to validate target cell"""
        # check if target is out of bounds
        if not(0 <= target_row < self.row_len and 0 <= target_col < self.col_len):
            return False
       
        target_cell = game_map[target_row][target_col]

        # check if target is a wall or a pressure plate
        if(target_cell == WALL):
            return False
       
        # check if target is a door
        if(target_cell in LOCKED_DOORS):
                return False
       
        # passed target cell tests
        return True
   
    def validate_pushed_cell(self, pushed_row, pushed_col, key_blocks, key_block_id, game_map):
        """Helper function to validate the pushed cell"""
        # check if key block is pushed out of bounds
        if not(0 <= pushed_row < self.row_len and 0 <= pushed_col < self.col_len):
            return False
           
        pushed_cell = game_map[pushed_row][pushed_col]
       
        # check if key block is pushed into a wall
        if(pushed_cell == WALL):
            return False

        # check if key block is pushed into the wrong pressure plate
        if(pushed_cell in PRESSURE_PLATES):
            plate_id = pushed_cell % 10
            if(key_block_id != plate_id):
                return False
               
        # check if key block is pushed into a locked door
        if(pushed_cell in LOCKED_DOORS):
            return False
               
        # check if key block is pushed into another key block
        if(pushed_cell in KEY_BLOCKS):
            return False
       
        # passed all tests for pushed cell
        return True

    def validate_dead_end(self, state, action, game_map):
        "Check if block is pushed to a dead end"
        agent_row, agent_col = state[0]
        action_row, action_col = ACTION_OFFSETS[action]
        target_row = agent_row + action_row
        target_col = agent_col + action_col
        pushed_row = agent_row + 2 * action_row
        pushed_col = agent_col + 2 * action_col

        # check if agent pushes a key block
        if game_map[target_row][target_col] in KEY_BLOCKS:
            # if next cell is floor, check if pushed block would be stuck
            pushed_block_id = game_map[target_row][target_col] % 10
            if game_map[pushed_row][pushed_col] == FLOOR:
                # check if block would be stuck in corner
                if self.validate_stuck_block(pushed_row, pushed_col, game_map, pushed_block_id):
                    return True  
       
        # no dead end
        return False

    def validate_stuck_block(self, pushed_row, pushed_col, game_map, pushed_block_id):
        # check if block is on a pressure plate
        if (pushed_row, pushed_col) in [(i, j) for plate_id, (i, j) in self.plates_pos]:
            return False

        def is_wall_or_wrong_pressure_plate(x, y):
            if 0 <= x < self.row_len and 0 <= y < self.col_len:
                return game_map[x][y] == WALL or (game_map[x][y] in PRESSURE_PLATES and game_map[x][y] % 10 != pushed_block_id)
            # if it's out of bounds also invalid
            return True              

        # check corners
        if is_wall_or_wrong_pressure_plate(pushed_row-1, pushed_col) and is_wall_or_wrong_pressure_plate(pushed_row, pushed_col-1):  # up + left
            return True
        if is_wall_or_wrong_pressure_plate(pushed_row-1, pushed_col) and is_wall_or_wrong_pressure_plate(pushed_row, pushed_col+1):  # up + right
            return True
        if is_wall_or_wrong_pressure_plate(pushed_row+1, pushed_col) and is_wall_or_wrong_pressure_plate(pushed_row, pushed_col-1):  # down + left
            return True
        if is_wall_or_wrong_pressure_plate(pushed_row+1, pushed_col) and is_wall_or_wrong_pressure_plate(pushed_row, pushed_col+1):  # down + right
            return True
       
        # not stuck
        return False
       
    def compute_state(self, action, state, game_map):
        """"Helper function that takes an action and a given state, and returns the next state after implmenting the action"""
        # check if action not in action offsets
        if action not in ACTION_OFFSETS:
            raise ValueError(f"Invalid action: {action}")
       
        # compute variables
        action_row, action_col = ACTION_OFFSETS[action]
        agent_row, agent_col = state[0]
        key_blocks = list(state[1])
        open_doors = set(state[2])
        pressure_plates = set(state[3])
        target_row = agent_row + action_row
        target_col = agent_col + action_col
        target_cell = game_map[target_row][target_col]
        new_agent_pos = (target_row, target_col)

        # handle moving agent to an empty floor
        if(target_cell == FLOOR or target_cell == GOAL):
            return(new_agent_pos, tuple(key_blocks), frozenset(open_doors), frozenset(pressure_plates))

        # if agent is pushing a key block
        if target_cell in KEY_BLOCKS:
            # compute new values for the pushed block
            pushed_row = agent_row + (2 * action_row)
            pushed_col = agent_col + (2 * action_col)
            pushed_cell = game_map[pushed_row][pushed_col]
            key_block_id = target_cell % 10
            target_pos = (target_row, target_col)
            pushed_pos = (pushed_row, pushed_col)

            # if block is pushed to a floor
            if(pushed_cell == FLOOR):
                return self.push_key_block_to_floor(key_blocks, target_pos, pushed_pos, new_agent_pos, open_doors, pressure_plates)

            # if block is pushed to a pressure plate
            if(pushed_cell in PRESSURE_PLATES):
                plate_id = pushed_cell % 10
                return self.push_key_block_to_plate(key_blocks, target_pos, pushed_pos, key_block_id, plate_id, new_agent_pos, open_doors, pressure_plates)

        # if reached here, return the current state
        return state
   
    def push_key_block_to_floor(self, key_blocks, target_pos, pushed_pos, agent_pos, open_doors, pressure_plates):
        """Handles pushing a block onto floor"""
        for index, (block_id, position) in enumerate(key_blocks):
            if position == target_pos:
                key_blocks[index] = (block_id, pushed_pos)
                break
        return (agent_pos, tuple(sorted(key_blocks)), frozenset(open_doors), frozenset(pressure_plates))
   
    def push_key_block_to_plate(self, key_blocks, target_pos, pushed_pos, key_block_id, plate_id,
                         agent_pos, open_doors, pressure_plates):
        """Handles pushing a block onto a pressure plate"""
        for index, (block_id, position) in enumerate(key_blocks):
            if position == target_pos:
                key_blocks[index] = (block_id, pushed_pos)
                break

        pressure_plates_dict = dict(pressure_plates)
        if key_block_id == plate_id:
            pressure_plates_dict[plate_id] = pressure_plates_dict.get(plate_id, 0) + 1
            if pressure_plates_dict[plate_id] == self.pressure_plates_counters[plate_id]:
                open_doors.add(plate_id)

        return (agent_pos, tuple(sorted(key_blocks)), frozenset(open_doors), frozenset(sorted(pressure_plates_dict.items())))

    def goal_test(self, state):
        """given a state, checks if this is the goal state, compares to the created goal state returns True/False"""
        # check the agent position with the goal position computed in the start (init)
        return state[0] == self.goal
   
    def h(self, node):
        """Computes heuristic sum of agent to goal distance and block"""
        agent_pos = node.state[0]
        key_blocks = node.state[1]
        open_doors = node.state[2]
        pressure_plates = dict(node.state[3])

        # compute agent to goal distance
        agent_to_goal = abs(agent_pos[0] - self.goal[0]) + abs(agent_pos[1] - self.goal[1])

        # compute locked doors penalty
        penalty = 0
        penalty_per_door = 6
        for door_id, (i, j) in self.doors_pos:
            if door_id not in open_doors:
                penalty += penalty_per_door

        return agent_to_goal + penalty


def create_pressure_plate_problem(game):
    print("<<create_pressure_plate_problem")
    """Create a pressure plate problem, based on the description.
    game - tuple of tuples as described in pdf file"""
    return PressurePlateProblem(game)


if __name__ == '__main__':
    ex1_check.main()