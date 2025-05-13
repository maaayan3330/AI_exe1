import pygame
import time
import search

# צבעים
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (100, 100, 255)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
YELLOW = (255, 255, 100)

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

CELL_SIZE = 40
# Define the class PressurePlateProblem
class PressurePlateProblem:
    def __init__(self, initial):
        self.map = initial

    def successor(self, state):
        pass

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
    import pygame
    import time
    from ex1 import PressurePlateProblem  # ודא שהקובץ שלך נקרא כך

    # הלוח
    initial_map = (
        (99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99),
        (99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 98, 98, 98, 98, 99),
        (99, 99, 99, 98, 98, 99, 99, 99, 99, 99, 98, 99, 98, 98, 99),
        (99, 99, 98, 98, 98, 99, 99, 98, 25, 99, 98, 98, 99, 98, 99),
        (99, 99, 98, 98, 98, 98, 98, 98, 45, 98, 2, 98, 99, 98, 99),
        (99, 99, 99, 42, 99, 99, 99, 98, 98, 99, 99, 99, 99, 98, 99),
        (99, 99, 98, 98, 22, 99, 99, 99, 99, 99, 98, 98, 98, 98, 99),
        (99, 99, 98, 98, 98, 99, 98, 98, 98, 99, 98, 99, 99, 99, 99),
        (99, 99, 98, 98, 98, 99, 98, 98, 12, 99, 98, 98, 98, 98, 99),
        (99, 99, 99, 41, 99, 99, 98, 15, 98, 98, 23, 99, 99, 98, 99),
        (99, 98, 98, 98, 20, 99, 98, 98, 98, 98, 98, 99, 99, 98, 99),
        (99, 98, 10, 98, 98, 99, 98, 98, 99, 98, 98, 99, 99, 98, 99),
        (99, 98, 98, 98, 11, 40, 98, 98, 98, 13, 98, 99, 99, 98, 99),
        (99, 1, 98, 98, 21, 99, 98, 98, 98, 98, 98, 98, 43, 98, 99),
        (99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99),
    )

    # תום 13
    # actions = ['U', 'R', 'D', 'R', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'R', 'U', 'R', 'U', 'U', 'L', 'L', 'D', 'D', 'R', 'D', 'L', 'U', 'L', 'D', 'R', 'D', 'L', 'U', 'U', 'U', 'U', 'U', 'L', 'U', 'R', 'R', 'R', 'U', 'R', 'R', 'R', 'D', 'D', 'R', 'R', 'L', 'L', 'D', 'D', 'D', 'D', 'R', 'D', 'D', 'D', 'R', 'R', 'R', 'R', 'R', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'L', 'L', 'L', 'D', 'D', 'D', 'U', 'L',
    #             'L', 'L', 'D', 'D', 'D', 'R', 'D', 'D', 'D', 'D', 'R', 'R', 'R', 'R', 'R', 'D', 'D', 'D', 'D', 'L', 'L', 'L', 'L']
    # אלון
    # actions = ['U', 'R', 'D', 'R', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'R', 'U', 'L', 'R', 'R', 'U', 'U', 'L', 'L', 'D', 'L', 'D', 'D', 'R', 'D', 'L', 'U', 'U', 'U', 'U', 'U', 'L', 'U', 'R', 'R', 'R', 'U', 'R', 'R', 'R', 'D', 'D', 'R', 'R', 'L', 'L', 'D', 'D', 'D', 'D', 'R', 'D', 'D', 'D', 'R', 'R', 'R', 'R', 'R', 'U', 'U', 'U', 'U', 'U',
    #             'U', 'U', 'U', 'U', 'L', 'L', 'L', 'D', 'D', 'D', 'U', 'U', 'U', 'R', 'R', 'R', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'L', 'L', 'L', 'L']
    # # # maayn
    # actions = ['U', 'R', 'D', 'R', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'R', 'U', 'R', 'U', 'U', 'L', 'L', 'D', 'D', 'R', 'D', 'L', 'U', 'L', 'D', 'R', 'D', 'L', 'U',
    #             'U', 'U', 'U', 'U', 'L', 'U', 'R', 'R', 'R', 'U', 'R', 'R', 'R', 'D', 'D', 'R', 'R', 'L', 'L', 'D', 'D', 'D', 'D', 'R', 'D', 'D', 'D', 'R', 'R', 'R', 'R', 'R', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'L', 'L', 'L', 'D', 'D', 'D', 'U', 'L', 'L', 'L', 'D', 'D', 'D', 'R', 'D', 'D', 'D', 'D', 'R', 'R', 'R', 'R', 'R', 'D', 'D', 'D', 'D', 'L', 'L', 'L', 'L']
  
    # שאלה 11
    actions = ['R', 'U', 'U', 'L', 'U', 'R', 'R', 'D', 'R', 'D', 'R', 'R', 'R', 'R', 'R', 'D', 'R', 'U', 'U', 'U',
                'D', 'D', 'D', 'R', 'R', 'R', 'U', 'U', 'U', 'U', 'U', 'L', 'L', 'L', 'U', 'U', 'R', 'R', 'R', 'U', 'U', 'U', 'U', 'L', 'U', 'L', 'L', 'D', 'D', 'D']

    pygame.init()
    screen = pygame.display.set_mode((len(initial_map[0]) * CELL_SIZE, len(initial_map) * CELL_SIZE))
    pygame.display.set_caption("Pressure Plate Problem Simulation")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    # יצירת האובייקט של הבעיה
    problem = PressurePlateProblem(initial_map)
    state = problem.initial  # זהו ה־state בפורמט שלך

    for action in actions:
        found = False
        for a, new_state in problem.successor(state):
            if a == action:
                state = new_state
                found = True
                break
        if not found:
            print(f"❌ פעולה לא חוקית: {action}")
            break

        # שרטוט מצב
        screen.fill((255, 255, 255))
        current_map = problem.get_effective_map(state)
        draw_board(screen, current_map, font)
        pygame.display.flip()

        time.sleep(0.5)
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

    pygame.quit()

# Run the simulation
run_simulation()




#   (5,6) (5,5,3) (7 , 9, 2).... ()  {} {}  -start
#   (5,5) (5,4,3)(7 , 9, 2).....() {} {}  -  push
#   (5,6) (5,4,3) (7 , 9, 2).... ()    - right
#   (5,7) (5,4,3) (7 , 9, 2).... ()    - right
#   (4,7) (5,4,3) (7 , 9, 2).... ()    - up
#    (3,7) (5,4,3) (7 , 9, 2).... ()    - up
#    (3,6) (5,4,3) (7 , 8, 2) .... () - left
#    (3,5) (5,4,3) (7  , 7, 2) .... () - left 
#     (4,5) (5,4,3) (7  , 7, 2) .... () - down
#     (4,4) (5,4,3) (7  , 7, 2) .... () - left