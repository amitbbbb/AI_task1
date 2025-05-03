import ex1_check
import search
import utils

id = ["211548045"]

""" Rules """
BLANK = 0
WALL = 99
FLOOR = 98
AGENT = 1
GOAL = 2
AGENT_ON_GOAL = 3 
LOCKED_DOORS = list(range(40, 50))
PRESSED_PLATES = list(range(30, 40))
PRESSURE_PLATES = list(range(20, 30))
KEY_BLOCKS = list(range(10, 20))
directions = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1)
}

""" This class implements a pressure plate problem """



class PressurePlateProblem(search.Problem):
    """This class implements a pressure plate problem"""

    def __init__(self, initial):

        self.visited_states = set()
        self.map = initial
        goal = self.find_goal(initial)
        self.goal = goal
        agent = self.find_agent(initial)
        g = 0
        state = (initial, agent, g)

        """ Constructor only needs the initial state.
        Don't forget to set the goal or implement the goal test"""
        search.Problem.__init__(self, state, goal)

    def successor(self, state):
        """ Generates the successor states returns [(action, achieved_states, ...)]"""
        
        # print("successor")
        successors = []
        for direction, delta in directions.items():
            is_valid, new_state = self.make_move(state, direction)
            hashable_map = tuple(tuple(row) for row in new_state[0])
            if is_valid:
                if hashable_map in self.visited_states:
                    continue
                self.visited_states.add(hashable_map)
                successors.append((direction, new_state))
        return successors

    def goal_test(self, state):
        """ given a state, checks if this is the goal state, compares to the created goal state returns True/False"""
        return state[0][self.goal[0]][self.goal[1]] == AGENT_ON_GOAL
            

    def h(self, node):
        """ This is the heuristic. It gets a node (not a state)
        and returns a goal distance estimate"""
        agent = node.state[1]
        goal = self.goal
        g = node.state[2]
        # Manhattan distance heuristic
        return 3 * abs(agent[0] - goal[0]) + abs(agent[1] - goal[1]) + g

    def make_move(self, state, action):
        """ given a state and an action, returns the new state"""
        is_valid = False
        map, old_agent, g = state
        # print(f"Agent is at: {old_agent}")
        new_map = [list(row) for row in map]
        dx, dy = directions[action]
        new_agent_pos = (old_agent[0] + dx, old_agent[1] + dy)
        new_cell_val = new_map[new_agent_pos[0]][new_agent_pos[1]]
        if new_cell_val in LOCKED_DOORS or new_cell_val == WALL or new_cell_val in PRESSURE_PLATES or new_cell_val in PRESSED_PLATES:
            return is_valid, state
        if new_cell_val == FLOOR:
            new_map[old_agent[0]][old_agent[1]] = FLOOR
            new_map[new_agent_pos[0]][new_agent_pos[1]] = AGENT
            is_valid = True
        elif new_cell_val == GOAL:
            new_map[old_agent[0]][old_agent[1]] = FLOOR
            new_map[new_agent_pos[0]][new_agent_pos[1]] = AGENT_ON_GOAL
            is_valid = True
        elif new_cell_val in KEY_BLOCKS:
            second_cell_pos = (new_agent_pos[0] + dx, new_agent_pos[1] + dy)
            second_cell_val = new_map[second_cell_pos[0]][second_cell_pos[1]]
            if second_cell_val == FLOOR:
                new_map[old_agent[0]][old_agent[1]] = FLOOR
                new_map[new_agent_pos[0]][new_agent_pos[1]] = AGENT
                new_map[second_cell_pos[0]][second_cell_pos[1]] = new_cell_val
                is_valid = True
            elif second_cell_val in PRESSURE_PLATES and self.same_type(new_cell_val, second_cell_val):
                new_map[old_agent[0]][old_agent[1]] = FLOOR
                new_map[new_agent_pos[0]][new_agent_pos[1]] = AGENT
                new_map[second_cell_pos[0]][second_cell_pos[1]] = second_cell_val + 10
                # open door if needed
                is_locked_door_exist = False
                for i in range(len(new_map)):
                    for j in range(len(new_map[i])):
                        if new_map[i][j] in LOCKED_DOORS and self.same_type(new_map[i][j], second_cell_val):
                            is_locked_door_exist = True
                            break
                if is_locked_door_exist:
                    for i in range(len(new_map)):
                        for j in range(len(new_map[i])):
                            if new_map[i][j] == second_cell_val + 20:
                                new_map[i][j] = FLOOR
                is_valid = True
        new_map = tuple(tuple(row) for row in new_map)
        return is_valid, (new_map, new_agent_pos, g + 1)
            
    def same_type(self, cell1_val, cell2_val):
        """ given two cell values, checks if they are the same type"""
        return cell1_val % 10 == cell2_val % 10

    def find_goal(self, map):
        """ given a map, return it's goal position"""
        for i, row in enumerate(map):
            for j, cell in enumerate(row):
                if cell == GOAL:
                    return (i, j)
        return None

    def find_agent(self, map):
        """ given a map, return the agent position"""
        for i, row in enumerate(map):
            for j, cell in enumerate(row):
                if cell == AGENT:
                    return (i, j)
        return None

def create_pressure_plate_problem(game):
    print("<<create_pressure_plate_problem")
    """ Create a pressure plate problem, based on the description.
    game - tuple of tuples as described in pdf file"""
    return PressurePlateProblem(game)


if __name__ == '__main__':
    ex1_check.main()
