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
LOCKED_DOORS = list(range(40, 50))
PRESSED_PLATES = list(range(30, 40))
PRESSURE_PLATES = list(range(20, 30))
KEY_BLOCKS = list(range(10, 20))

DIRECTIONS = {
    "R": (0, 1),
    "L": (0, -1),
    "U": (-1, 0),
    "D": (1, 0)
}

class PressurePlateProblem(search.Problem):
    def __init__(self, initial):
        self.map = initial
        self.goal = None
        self.visited_states = set()
        self.base_map = [list(row) for row in initial]
        self.doors_info = []
        self.plates_info = []

        agent_placement = None
        key_blocks = []

        for i, row in enumerate(initial):
            for j, placement in enumerate(row):
                if placement == AGENT:
                    agent_placement = (i, j)
                    self.base_map[i][j] = FLOOR
                elif placement in KEY_BLOCKS:
                    key_blocks.append((i, j, placement % 10))
                    self.base_map[i][j] = FLOOR
                elif placement == GOAL:
                    self.goal = (i, j)
                elif placement in LOCKED_DOORS:
                    self.doors_info.append((i, j, placement % 10))
                elif placement in PRESSURE_PLATES:
                    self.plates_info.append((i, j, placement % 10))

        self.rows = len(self.map)
        self.cols = len(self.map[0])
        self.pressure_plate_counts = self.count_by_type(self.map, PRESSURE_PLATES)

        # added pressed_positions to the state
        initial_state = (
            agent_placement,
            tuple(sorted(key_blocks)),
            frozenset(),
            frozenset(),
            frozenset()  # pressed_positions
        )

        search.Problem.__init__(self, initial_state, goal=self.goal)
        ###############################################################################################

    def count_by_type(self, matrix, valid_range):
        counter = {}
        for row in matrix:
            for cell in row:
                if cell in valid_range:
                    block_type = cell % 10
                    counter[block_type] = counter.get(block_type, 0) + 1
        return counter

    def get_effective_map(self, state):
        pressed = dict(state[3])
        open_doors = set(state[2])
        key_blocks = list(state[1])
        pressed_positions = set(state[4])

        map_copy = [list(row) for row in self.base_map]

        for i, j, t in self.doors_info:
            if t in open_doors:
                map_copy[i][j] = FLOOR

        for i, j, t in self.plates_info:
            if (i, j) in pressed_positions:
                map_copy[i][j] = WALL

        for r, c, t in key_blocks:
            map_copy[r][c] = 10 + t

        rowA, colA = state[0]
        map_copy[rowA][colA] = AGENT

        return map_copy
######################################################
    def successor(self, state):
        new_states = []
        for direction in ["R", "L", "U", "D"]:
            new_states.extend(self.helper_successor(state, direction))
        return new_states

    def helper_successor(self, state, direction):
        results = []
        if not self.out_of_boundry(state, direction):
            return results

        map_for_state = self.get_effective_map(state)

        if self.next_move_wall(state, direction, map_for_state):
            return results
        if self.next_move_pressure_plates(state, direction, map_for_state):
            return results
        if self.push_block_invalid(state, direction, map_for_state):
            return results
        if self.locked_door(state, direction, map_for_state):
            return results
        if self.dead_end_due_to_stuck_blocks(state, direction, map_for_state):
            return results

        rowA, colA = state[0]
        dr, dc = DIRECTIONS[direction]
        one_r, one_c = rowA + dr, colA + dc
        two_r, two_c = rowA + 2 * dr, colA + 2 * dc

        key_blocks = list(state[1])
        open_doors = set(state[2])
        plates_covered = dict(state[3])
        pressed_positions = set(state[4])

        # Case 1: Move to empty cell
        if map_for_state[one_r][one_c] in [FLOOR, GOAL]:
            new_state = (
                (one_r, one_c),
                tuple(sorted(key_blocks)),
                frozenset(open_doors),
                frozenset(plates_covered.items()),
                frozenset(pressed_positions)
            )
            if (direction, new_state) not in self.visited_states:
                self.visited_states.add((direction, new_state))
                results.append((direction, new_state))
            return results

        # Case 2: Push block to FLOOR
        if map_for_state[one_r][one_c] in KEY_BLOCKS:
            if map_for_state[two_r][two_c] == FLOOR:
                key_type = map_for_state[one_r][one_c] % 10
                if (one_r, one_c, key_type) in key_blocks:
                    key_blocks.remove((one_r, one_c, key_type))
                    key_blocks.append((two_r, two_c, key_type))
                    new_state = (
                        (one_r, one_c),
                        tuple(sorted(key_blocks)),
                        frozenset(open_doors),
                        frozenset(plates_covered.items()),
                        frozenset(pressed_positions)
                    )
                    if (direction, new_state) not in self.visited_states:
                        self.visited_states.add((direction, new_state))
                        results.append((direction, new_state))
                    return results

        # Case 3: Push block to pressure plate (correct)
        if map_for_state[one_r][one_c] in KEY_BLOCKS:
            key_type = map_for_state[one_r][one_c] % 10
            if map_for_state[two_r][two_c] in PRESSURE_PLATES:
                pressure_type = map_for_state[two_r][two_c] % 10
                if key_type == pressure_type:
                    plates_covered[key_type] = plates_covered.get(key_type, 0) + 1
                    if plates_covered[key_type] == self.pressure_plate_counts[key_type]:
                        open_doors.add(key_type)
                    key_blocks.remove((one_r, one_c, key_type))
                    pressed_positions.add((two_r, two_c))
                    new_state = (
                        (one_r, one_c),
                        tuple(sorted(key_blocks)),
                        frozenset(open_doors),
                        frozenset(plates_covered.items()),
                        frozenset(pressed_positions)
                    )
                    if (direction, new_state) not in self.visited_states:
                        self.visited_states.add((direction, new_state))
                        results.append((direction, new_state))
                    return results

        return results

    def out_of_boundry(self, state, direction):
        r, c = state[0]
        dr, dc = DIRECTIONS[direction]
        return 0 <= r + dr < self.rows and 0 <= c + dc < self.cols

    def next_move_wall(self, state, direction, new_map):
        r, c = state[0]
        dr, dc = DIRECTIONS[direction]
        return new_map[r + dr][c + dc] == WALL

    def next_move_pressure_plates(self, state, direction, new_map):
        r, c = state[0]
        dr, dc = DIRECTIONS[direction]
        return new_map[r + dr][c + dc] in PRESSURE_PLATES

    def push_block_invalid(self, state, direction, new_map):
        r, c = state[0]
        dr, dc = DIRECTIONS[direction]
        one_r, one_c = r + dr, c + dc
        two_r, two_c = r + 2 * dr, c + 2 * dc

        if new_map[one_r][one_c] in KEY_BLOCKS:
            if not (0 <= two_r < self.rows and 0 <= two_c < self.cols):
                return True
            if new_map[two_r][two_c] in KEY_BLOCKS or new_map[two_r][two_c] == WALL:
                return True
            if new_map[two_r][two_c] in PRESSURE_PLATES:
                if new_map[two_r][two_c] % 10 != new_map[one_r][one_c] % 10:
                    return True
            cell = new_map[two_r][two_c]
            open_doors = state[2]
            if cell in LOCKED_DOORS and (cell % 10) not in open_doors:
                return True
        return False

    def locked_door(self, state, direction, new_map):
        r, c = state[0]
        dr, dc = DIRECTIONS[direction]
        cell = new_map[r + dr][c + dc]
        return cell in LOCKED_DOORS and (cell % 10) not in state[2]

    def dead_end_due_to_stuck_blocks(self, state, direction, new_map):
        r, c = state[0]
        dr, dc = DIRECTIONS[direction]
        one_r, one_c = r + dr, c + dc
        two_r, two_c = r + 2 * dr, c + 2 * dc

        if new_map[one_r][one_c] in KEY_BLOCKS:
            if not (0 <= two_r < self.rows and 0 <= two_c < self.cols):
                return True
            if new_map[two_r][two_c] == FLOOR:
                type_key = new_map[one_r][one_c] % 10
                if self.is_block_stuck(two_r, two_c, new_map, type_key):
                    return True
        return False

    def is_block_stuck(self, r, c, new_map, type_key):
        if (r, c) in [(i, j) for i, j, _ in self.plates_info]:
            return False

        def is_wall(y, x):
            if 0 <= y < self.rows and 0 <= x < self.cols:
                return new_map[y][x] == WALL or (
                    new_map[y][x] in PRESSURE_PLATES and new_map[y][x] % 10 != type_key)
            return True

        if is_wall(r-1, c) and is_wall(r, c-1):
            return True
        if is_wall(r-1, c) and is_wall(r, c+1):
            return True
        if is_wall(r+1, c) and is_wall(r, c-1):
            return True
        if is_wall(r+1, c) and is_wall(r, c+1):
            return True
        return False

    def goal_test(self, state):
        return state[0] == self.goal

    def h(self, node):
        agent_pos = node.state[0]
        open_doors = node.state[2]
        agent_to_goal = abs(agent_pos[0] - self.goal[0]) + abs(agent_pos[1] - self.goal[1])
        penalty = 6 * sum(1 for _, _, door_id in self.doors_info if door_id not in open_doors)
        return agent_to_goal + penalty


