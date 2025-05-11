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
        self.goal = None
        ##############################################################################################
        self.visited_states = set()
        #################################################################################################
        self.map_cache = {}
        ############################################################################################
        # I want to pass the constructor not the all netrix just the - initial stats
        agent_placement = None
        key_blocks = []
        for i, row in enumerate(initial):
            for j, placement in enumerate(row):
                if placement == AGENT:
                    agent_placement = (i,j)
                if placement in KEY_BLOCKS:
                    # i keep the placement of the cube and its number
                    key_blocks.append((i,j,placement % 10))
                # i will keep the goal for later
                if placement == GOAL:
                    self.goal = (i,j)
                    # print("that the goal",self.goal)
        # keep info for later
        self.rows = len(self.map)
        self.cols = len(self.map[0])
        # keep the num of "pressure plates"
        self.pressure_plate_counts = self.count_by_type(self.map, PRESSURE_PLATES)
        # so far I just collect the all informetion and now i will add it to states - frozenset - no open door in the beging , plated coverd
        initial_state = (agent_placement, tuple(sorted(key_blocks)), frozenset(), frozenset())
        # note - I keep the first item in the initial_state to be = the agent = state[0]
        # print("📦 Initial state:", agent_placement, key_blocks, self.goal)
        search.Problem.__init__(self, initial_state, goal=self.goal)
        print("📦 Initial state:", agent_placement, key_blocks, self.goal)


    # this function is to keep the data i need
    def count_by_type(self, matrix, valid_range):
        counter = {}
        for row in matrix:
            for cell in row:
                if cell in valid_range:
                    block_type = cell % 10
                    counter[block_type] = counter.get(block_type, 0) + 1
        return counter

    # to copy to each state the map that relevnt for him 
    def get_effective_map(self, state):
        if state in self.map_cache:
            return self.map_cache[state]
        # get the num of pressed
        pressed = dict(state[3])
        required = self.pressure_plate_counts
        key_blocks = list(state[1])
        open_doors = set(state[2])

        map_copy = [list(row) for row in self.map]
        for i in range(self.rows):
            for j in range(self.cols):
                cell = map_copy[i][j]
                # if the cell is a open door - now
                if cell in LOCKED_DOORS and (cell % 10) in open_doors:
                    map_copy[i][j] = FLOOR

                # if the cell is pressed botten - now 
                if cell in PRESSURE_PLATES:
                   type_of = cell % 10
                   if pressed.get(type_of , 0) == required.get(type_of, 0):
                       map_copy[i][j] = WALL

                # if the agent is in other placement
                if cell == AGENT:
                    # delete it 
                    map_copy[i][j] = FLOOR 

                # delete all key blockes
                if cell in KEY_BLOCKS:
                    map_copy[i][j] = FLOOR 

        # update the new one place of the agent
        rowA , colA = state[0]
        map_copy[rowA][colA] = AGENT
        # update the all key blockes new placne ment
        for r, c, t in key_blocks:
            map_copy[r][c] = 10 + t
        self.map_cache[state] = map_copy
        return map_copy 
    
    def normalize_state(agent, key_blocks, open_doors, plates_covered):
        return (
            agent,
            tuple(sorted(key_blocks)),
            frozenset(open_doors),
            frozenset(sorted(plates_covered.items()))
        )

    
    def successor(self, state):
        """ Generates the successor states returns [(action, achieved_states, ...)]"""
        # first thing - check for every UP DOWN LEFT RIGHT the all possible situtions
        #########################################################################################
        # print("🔁 Generating successors for:", state[0])
        # print("🔁 Called successor for:", state[0])
       #############################################################################################
        new_states = []
        for direction in ["R", "L", "U", "D"]:
            possible_moves = self.helper_successor(state, direction)
            new_states.extend(possible_moves)
        # print("✅ New state:", new_states)
        return new_states
    
    def helper_successor(self, state , direction):
        results = []
        # ##### check for wrong cases - for better time run :
        # case 1 - if the next step is out of the boundry of the metrix
        if not self.out_of_boundry(state, direction):
            return results
        
        # the corrent map
        map_for_state = self.get_effective_map(state)
        ##################################################################למחוק
        direction_row, direction_col = DIRECTIONS[direction]
        row_of_agent, col_of_agent = state[0]
        next_row = row_of_agent + direction_row
        next_col = col_of_agent + direction_col
        ##################################################################למחוק
        # print(f"🚶 Agent at {state[0]}, trying direction: {direction}")
        # print(f"🗺️ Next cell value: {map_for_state[next_row][next_col]}")
        ###################################################################################
        ##### check for wrong cases - for better time run : #####
        # case 2 - if the next step of the agent is to wall 
        if self.next_move_wall(state, direction, map_for_state):
            return results
        # case 3 - if the agent next stop is to a "pressure plates"
        if self.next_move_pressure_plates(state, direction, map_for_state):
            return results
        # case 4 - if the agent next stop is to a "key blocks" that have a "key block" after it or a wall
        # *cube after cube | *wall after cube | *worng pressuer number after cube | *push a cube and its go behond the boundery
        if self.push_block_invalid(state, direction, map_for_state):
            return results
        # case 5 - if the agent next stop is to a locked door
        if self.locked_door(state, direction, map_for_state):
            return results
        

        # check now for good cases to insert to the states :
        row_of_agent , col_of_agent = state[0]
        direction_row, direction_col = DIRECTIONS[direction]
        key_blocks = list(state[1])
        open_doors = set(state[2])
        plates_covered = dict(state[3])

        one_move_row, one_move_col = row_of_agent + direction_row, col_of_agent + direction_col
        two_move_row, two_move_col = row_of_agent + 2 * direction_row, col_of_agent + 2 * direction_col


        # case 1 - the agent want to move to an empty place
        if map_for_state[one_move_row][one_move_col] in [FLOOR, GOAL]:
            # keep the new placment of the agen
            new_agent_placement = (one_move_row, one_move_col)
            # keep the all info about the "key blockes"
            new_state = (new_agent_placement, tuple(sorted(key_blocks)), frozenset(open_doors), frozenset(plates_covered.items()))
            # print("🧠 Created new_state:", new_state)
            # results.append((direction, new_state))
            if new_state not in self.visited_states:
                self.visited_states.add(new_state)
                results.append((direction, new_state))

            return results
        
        # case 2 - the agent want to push a "key block" to FLOOR and it is valid (it mean there is no wall/key block after the one he want to push) - we cannn push!!
        if map_for_state[one_move_row][one_move_col] in KEY_BLOCKS:
            if map_for_state[two_move_row][two_move_col] == FLOOR:
                key_type = (map_for_state[one_move_row][one_move_col]) % 10
                if (one_move_row, one_move_col, key_type) in key_blocks:
                    # remove the position of the old cube
                    key_blocks.remove((one_move_row, one_move_col, key_type))
                    # add it to the new position
                    key_blocks.append((two_move_row, two_move_col, key_type))
                    # update all
                    new_state = ((one_move_row, one_move_col), tuple(sorted(key_blocks)), frozenset(open_doors), frozenset(plates_covered.items()))
                    # print("🧠 Created new_state:", new_state)
                    # results.append((direction, new_state))
                    if new_state not in self.visited_states:
                        self.visited_states.add(new_state)
                        results.append((direction, new_state))
                    return results

        # case 3 - the agent push a "key block" and now it is on a pressure plates 
        # check if the next is a cube
        if map_for_state[one_move_row][one_move_col] in KEY_BLOCKS:  
            # keep the num 
            key_type = (map_for_state[one_move_row][one_move_col]) % 10
            # check if there is a pressure plate
            if map_for_state[two_move_row][two_move_col] in PRESSURE_PLATES:
                pressure_type = (map_for_state[two_move_row][two_move_col]) % 10
                # if it is a correct push
                if key_type == pressure_type:
                    # we coverd one more so we will keep it
                    plates_covered[key_type] = plates_covered.get(key_type, 0) + 1
                    # now maybe we open a door 
                    if plates_covered[key_type] == self.pressure_plate_counts[key_type]:
                        open_doors.add(key_type)
                    # remove the placment of the cube becuse we did a move
                    key_blocks.remove((one_move_row, one_move_col, key_type))
                    new_agent_placement = (one_move_row, one_move_col)
                    new_state = (new_agent_placement, tuple(sorted(key_blocks)), frozenset(open_doors),frozenset(plates_covered.items()))
                    # print("🧠 Created new_state:", new_state)
                    # results.append((direction, new_state))
                    if new_state not in self.visited_states:
                        self.visited_states.add(new_state)
                        results.append((direction, new_state))
                    return results
                
        return results


        ##################################### תחשבי אם כיסת את המצב של אםם זה אזור לחוץ כבר
    
    # helpper functions for helper seccessor
    # case 1 
    def out_of_boundry(self, state, direction):
        row_of_agent , col_of_agent = state[0]
        direction_row, direction_col = DIRECTIONS[direction]
        new_row = row_of_agent + direction_row
        new_col = col_of_agent + direction_col

        # print(f"🧭 Move: {direction}, From ({row_of_agent},{col_of_agent}) ➡️ To ({new_row},{new_col})")
        # print(f"🧱 Bounds check: rows={self.rows}, cols={self.cols}")

        return 0 <= new_row < self.rows and 0 <= new_col < self.cols
    
    # case 2 
    def next_move_wall(self, state, direction, new_map):
        row_of_agent , col_of_agent = state[0]
        direction_row, direction_col = DIRECTIONS[direction]
        return new_map[row_of_agent + direction_row][col_of_agent + direction_col] == WALL

    # case 3
    def next_move_pressure_plates(self, state, direction, new_map):
        row_of_agent , col_of_agent = state[0]
        direction_row, direction_col = DIRECTIONS[direction]
        return new_map[row_of_agent + direction_row][col_of_agent + direction_col] in PRESSURE_PLATES

    # case 4
    def push_block_invalid(self, state, direction, new_map):
        row_of_agent , col_of_agent = state[0]
        direction_row, direction_col = DIRECTIONS[direction]

        one_move_row, one_move_col = row_of_agent + direction_row, col_of_agent + direction_col
        two_move_row, two_move_col = row_of_agent + 2 * direction_row, col_of_agent + 2 * direction_col

        # first check if the move push a cube - so if in the other plate there is a key!
        if new_map[one_move_row][one_move_col] in KEY_BLOCKS:
            # now there is a cube - first check if the placement after it is in the bounderis
            if not (0 <= two_move_row < self.rows and 0 <= two_move_col < self.cols):
                # the next step is out of bounderies for ROW and COL
                return True
            # so it is in boundry - check if there is a cube after it - 2 cube in a row cannot
            if new_map[two_move_row][two_move_col] in KEY_BLOCKS:
                return True
            # check if there is a wall after it
            if new_map[two_move_row][two_move_col] ==  WALL:
                return True
            # check if we push the cube to a wrong pressure
            if new_map[two_move_row][two_move_col] in PRESSURE_PLATES:
                plate_pressure = new_map[two_move_row][two_move_col]
                key_block = new_map[one_move_row][one_move_col]
                if (plate_pressure % 10) != (key_block % 10):
                    # they have diffrent numbers 
                    return True
        # it is all good
        return False

    # case 5
    def locked_door(self, state, direction, new_map):
        row_of_agent , col_of_agent = state[0]
        direction_row, direction_col = DIRECTIONS[direction]

        cell = new_map[row_of_agent + direction_row][col_of_agent + direction_col]
        open_doors = state[2]

        # try to enter a door and it locked - not in open doors
        if cell in LOCKED_DOORS and (cell % 10) not in open_doors:
            return True
        return False


    def goal_test(self, state):
        """ given a state, checks if this is the goal state, compares to the created goal state returns True/False"""
        # print("👀 Checking goal for:", state[0], "==", self.goal)
        # i want to check if agent is on goal
        return state[0] == self.goal

    # def h(self, node):
    #     """ This is the heuristic. It gets a node (not a state)
    #     and returns a goal distance estimate"""
    #     """Simple heuristic: Manhattan distance from agent to goal"""
    #     agent_pos = node.state[0]
    #     goal_pos = self.goal

    #     return abs(agent_pos[0] - goal_pos[0]) + abs(agent_pos[1] - goal_pos[1])

    # def h(self, node):
    #     state = node.state
    #     agent_pos = state[0]
    #     key_blocks = state[1]
        
    #     # מרחק הסוכן למטרה
    #     agent_to_goal = abs(agent_pos[0] - self.goal[0]) + abs(agent_pos[1] - self.goal[1])
        
    #     # סכום מרחקי בלוקים ללחצנים מהסוג הנכון
    #     total_block_to_plate = 0
    #     for block_row, block_col, block_type in key_blocks:
    #         closest_plate_dist = float('inf')
    #         for i in range(self.rows):
    #             for j in range(self.cols):
    #                 cell = self.map[i][j]
    #                 if cell in PRESSURE_PLATES and cell % 10 == block_type:
    #                     dist = abs(i - block_row) + abs(j - block_col)
    #                     closest_plate_dist = min(closest_plate_dist, dist)
    #         total_block_to_plate += closest_plate_dist

    #     return agent_to_goal + total_block_to_plate

    def h(self, node):
        agent_pos = node.state[0]
        key_blocks = node.state[1]
        plates_covered = dict(node.state[3])

        # חלק 1: מרחק הסוכן למטרה
        agent_to_goal = abs(agent_pos[0] - self.goal[0]) + abs(agent_pos[1] - self.goal[1])

        # חלק 2: סכום מרחקי כל בלוק ללחצן המתאים הקרוב ביותר
        block_to_plate_total = 0
        for r, c, block_type in key_blocks:
            if plates_covered.get(block_type, 0) >= self.pressure_plate_counts.get(block_type, 0):
                continue  # כבר כל הלחצנים מהסוג הזה מכוסים
            min_dist = float('inf')
            for i in range(self.rows):
                for j in range(self.cols):
                    cell = self.map[i][j]
                    if cell in PRESSURE_PLATES and cell % 10 == block_type:
                        dist = abs(r - i) + abs(c - j)
                        if dist < min_dist:
                            min_dist = dist
            if min_dist < float('inf'):
                block_to_plate_total += min_dist  # סכום המרחקים המינימליים של בלוקים ללחצנים

        return agent_to_goal + block_to_plate_total



def create_pressure_plate_problem(game):
    print("<<create_pressure_plate_problem")
    """ Create a pressure plate problem, based on the description.
    game - tuple of tuples as described in pdf file"""
    return PressurePlateProblem(game)

if __name__ == '__main__':
    # print("hiiiiiiiiiiiiiiiiii")
    ex1_check.main()
