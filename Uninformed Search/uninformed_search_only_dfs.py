# -----------------------------------------------------------------------------
# Name:     uninformed_search
# Purpose:  Homework 4 - Implement bfs and ucs graph search algorithms
# -----------------------------------------------------------------------------
"""
Uninformed Search Algorithm implementation
dfs has been implemented for you.
Your task for homework 4 is to implement bfs and ucs.
"""
import data_structures


def dfs(problem):
    """
    Depth first graph search algorithm - implemented for you
    returns a solution for the given search problem
    :param
    problem (a Problem object) representing the quest
            see Problem class definition in spartanquest.py)
    :return: list of actions representing the solution to the quest
                or None if there is no solution
    """
    closed = set()  # keep track of our explored states
    fringe = data_structures.Stack()  # for dfs, the fringe is a stack
    state = problem.start_state()
    root = data_structures.Node(state)
    fringe.push(root)
    while True:
        if fringe.is_empty():
            return None  # Failure - fringe is empty and no solution was found
        node = fringe.pop()
        if problem.is_goal(node.state):
            return node.solution()
        if node.state not in closed:  # we are implementing graph search
            closed.add(node.state)
            for child_state, action, action_cost in problem.successors(
                    node.state):
                child_node = data_structures.Node(child_state, node, action)
                fringe.push(child_node)


def bfs(problem):
    """
    Breadth first graph search algorithm
    returns a solution for the given search problem
    :param
    problem (a Problem object) representing the quest
            see Problem class definition in spartanquest.py)
    :return: list of actions representing the solution to the quest
            or None if there is no solution
    """
    # Enter your code here 
    
    
    


def ucs(problem):
    """
    Uniform cost first graph search algorithm
    returns a solution for the given search problem
    :param
    problem (a Problem object) representing the quest
            see Problem class definition in spartanquest.py)
    :return: list of actions representing the solution to the quest
    """
    # Enter your code here 
    
    
    