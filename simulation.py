import pygame
import time

# צבעים
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (100, 100, 255)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
YELLOW = (255, 255, 100)

# help with the drections
DIRECTIONS = {
    "R": (0, 1),
    "L": (0, -1),
    "U": (-1, 0),
    "D": (1, 0)
}


# חוקים
BLANK = 0
WALL = 99
FLOOR = 98
AGENT = 1
GOAL = 2
AGENT_ON_GOAL = 3

KEY_BLOCKS = list(range(10, 20))
PRESSURE_PLATES = list(range(20, 30))
PRESSED_PLATES = list(range(30, 40))
LOCKED_DOORS = list(range(40, 50))

CELL_SIZE = 60
# Define the class PressurePlateProblem
class PressurePlateProblem:
    def __init__(self, initial):
        self.map = initial

    def successor(self, state):
        """ Generates the successor states returns [(action, achieved_states, ...)]"""
        # first thing - check for every UP DOWN LEFT RIGHT the all possible situtions
        # print("🔁 Generating successors for:", state[0])
        # print("🔁 Called successor for:", state[0])
        # print("i am in succsor")
        new_states = []
        for direction in ["R", "L", "U", "D"]:
            possible_moves = self.helper_successor(state, direction)
            new_states.extend(possible_moves)
        # print("✅ New state:", new_states)
        return new_states
    
    def helper_successor(self, state , direction):
        results = []
        # # the corrent map
        # map_for_state = self.get_effective_map(state)
        # ##################################################################למחוק
        # direction_row, direction_col = DIRECTIONS[direction]
        # row_of_agent, col_of_agent = state[0]
        # next_row = row_of_agent + direction_row
        # next_col = col_of_agent + direction_col
        # ##################################################################למחוק
        # print(f"🚶 Agent at {state[0]}, trying direction: {direction}")
        # print(f"🗺️ Next cell value: {map_for_state[next_row][next_col]}")
        # ##### check for wrong cases - for better time run : #####
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
        print(f"🚶 Agent at {state[0]}, trying direction: {direction}")
        print(f"🗺️ Next cell value: {map_for_state[next_row][next_col]}")
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
        if map_for_state[one_move_row][one_move_col] == FLOOR:
            # keep the new placment of the agen
            new_agent_placement = (one_move_row, one_move_col)
            # keep the all info about the "key blockes"
            new_state = (new_agent_placement, tuple(sorted(key_blocks)), frozenset(open_doors), frozenset(plates_covered.items()))
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
                    new_state = (new_agent_placement, tuple(sorted(key_blocks)), frozenset(open_doors),frozenset(plates_covered.items()) )
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

        print(f"🧭 Move: {direction}, From ({row_of_agent},{col_of_agent}) ➡️ To ({new_row},{new_col})")
        print(f"🧱 Bounds check: rows={self.rows}, cols={self.cols}")

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



def draw_board(screen, grid, font):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            val = grid[row][col]

            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            if val == WALL:
                color = BLACK
            elif val == FLOOR:
                color = WHITE
            elif val == AGENT or val == AGENT_ON_GOAL:
                color = BLUE
            elif val == GOAL:
                color = GREEN
            elif val in KEY_BLOCKS:
                color = RED
            elif val in PRESSURE_PLATES:
                color = YELLOW
            elif val in PRESSED_PLATES:
                color = (255, 165, 0)  # כתום
            elif val in LOCKED_DOORS:
                color = GRAY
            else:
                color = WHITE

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

            # כתיבת הערך
            text = font.render(str(val), True, BLACK)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

def run_simulation():
    # Initial state setup (map)
    # הלוח
    initial_state = (
        (99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99),
        (99, 98, 98, 98, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99),
        (99, 98, 99, 98, 99, 99, 99, 99, 99, 99, 98, 98, 99, 99, 99),
        (99, 98, 99, 98, 98, 99, 25, 98, 99, 99, 98, 98, 98, 99, 99),
        (99, 98, 99, 98, 2, 45, 98, 98, 98, 98, 98, 98, 98, 99, 99),
        (99, 98, 99, 99, 99, 99, 98, 98, 99, 99, 99, 42, 99, 99, 99),
        (99, 98, 98, 98, 98, 99, 99, 99, 99, 99, 22, 98, 98, 99, 99),
        (99, 99, 99, 99, 98, 99, 98, 98, 98, 99, 98, 98, 98, 99, 99),
        (99, 98, 98, 98, 98, 99, 12, 98, 98, 99, 98, 98, 98, 99, 99),
        (99, 98, 99, 99, 23, 98, 98, 15, 98, 99, 99, 41, 99, 99, 99),
        (99, 98, 99, 99, 98, 98, 98, 98, 98, 99, 20, 98, 98, 98, 99),
        (99, 98, 99, 99, 98, 98, 99, 98, 98, 99, 98, 98, 10, 98, 99),
        (99, 98, 99, 99, 98, 13, 98, 98, 98, 40, 11, 98, 98, 98, 99),
        (99, 98, 43, 98, 98, 98, 98, 98, 98, 99, 21, 98, 98, 1, 99),
        (99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99),
    )

    actions = ['L', 'U', 'U', 'R', 'U', 'L', 'L', 'D', 'L', 'D', 'L', 'L', 'L', 'L', 'L', 'D', 'L', 'U', 'U', 'U', 'D',
               'D', 'D', 'L', 'L', 'L', 'U', 'U', 'U', 'U', 'U', 'R', 'R', 'R', 'U', 'U', 'L', 'L', 'L', 'U', 'U', 'U',
               'U', 'U', 'R', 'R', 'D', 'D', 'R', 'D']

    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((len(initial_state[0]) * (CELL_SIZE), len(initial_state) * (CELL_SIZE)))
    pygame.display.set_caption("Pressure Plate Problem")

    clock = pygame.time.Clock()

    problem = PressurePlateProblem(initial_state)
    state = initial_state

    # Run the simulation
    for action in actions:
        for a, n_state in problem.successor(state):
            if a == action:
                state = n_state
                break

        # Clear the screen and redraw the state
        screen.fill((255, 255, 255))  # White background
        draw_board(screen, state, pygame.font.SysFont(None, 24))
        pygame.display.flip()

        time.sleep(0.5)  # Slow down the movement to see it
        clock.tick(60)

        # Event handling to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

    pygame.quit()

# Run the simulation
run_simulation()