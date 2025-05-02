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



class PressurePlateProblem(search.Problem):
    """This class implements a pressure plate problem"""

    def __init__(self, initial):

        self.map = initial
        self.goal = self.find_goal(initial)
        agent = self.find_agent(initial)
        state = (initial, agent)

        """ Constructor only needs the initial state.
        Don't forget to set the goal or implement the goal test"""
        search.Problem.__init__(self, state)

    def successor(self, state):
        """ Generates the successor states returns [(action, achieved_states, ...)]"""
        utils.raiseNotDefined()

    def goal_test(self, state):
        """ given a state, checks if this is the goal state, compares to the created goal state returns True/False"""
        return self.map[self.goal[0]][self.goal[1]] == AGENT_ON_GOAL
            

    def h(self, node):
        """ This is the heuristic. It gets a node (not a state)
        and returns a goal distance estimate"""
        agent = node.state[1]
        goal = self.goal
        # Manhattan distance heuristic
        return abs(agent[0] - goal[0]) + abs(agent[1] - goal[1])



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
