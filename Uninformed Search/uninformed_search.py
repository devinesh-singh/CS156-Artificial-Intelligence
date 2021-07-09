#!/usr/bin/env python
# coding: utf-8

# In[1]:


import data_structures
from queue import PriorityQueue
import heapq


# In[2]:


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


# In[5]:


def bfs(problem):
    visited = set() # store all visited nodes 
    queue = data_structures.Queue() # the queue to store the nodes
    state = problem.start_state() # initialize the start state
    root = data_structures.Node(state) # initilize the root state
    queue.push(root) # push the root node into the queue
    
    while True:
        if queue.is_empty():
            return None # root node is null, therefore no solution
        node = queue.pop()
        if problem.is_goal(node.state):
            return node.solution() # return the solution if it is 
        if node.state not in visited: # check if the node has already been visited (if not, add it)
            visited.add(node.state)
            for child_state, action, action_cost in problem.successors(node.state):
                child_node = data_structures.Node(child_state, node, action)
                queue.push(child_node)
    


# In[ ]:

# incomplete code
def ucs(problem):
    visited = set() # store all visited nodes
    queue = data_structures.PriorityQueue() # the queue to store the nodes
    state = problem.start_state() # initialize the start state
    root = data_structures.Node(state) # initilize the root state
    queue.push(root, 0) # push the root node into the queue
    
    while True:
        if queue.is_empty():
            return None # root node is null, therefore no solution
        node = queue.pop()
        if problem.is_goal(node.state):
            return node.solution() # return the solution if it is
        if node.state not in visited: # check if the node has already been visited (if not, add it)
            visited.add(node.state)
            for child_state, action, action_cost in problem.successors(node.state):
                child_node = data_structures.Node(child_state, node, action)
                child_node.cumulative_cost = node.cumulative_cost + action_cost
                queue.push(child_node, child_node.cumulative_cost)
    



# In[ ]:




