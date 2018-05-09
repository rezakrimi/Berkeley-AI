# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    n = Directions.NORTH
    e = Directions.EAST

    result = []
    st = util.Stack()
    visited = set([])

    current = problem.getStartState()
    st.push((current, "", 0))

    while not st.isEmpty():
        while st.top()[0] in visited:
            st.pop()
            result.pop()

        current = st.top()
        visited.add(current[0])

        if current[1] != "":
            result.append(current[1])

        if problem.isGoalState(current[0]):
            break

        for each in problem.getSuccessors(current[0]):
            if each[0] not in visited:
                st.push(each)

    path = []
    for each in result:
        if each == "South":
            path.append(s)
        elif each == "West":
            path.append(w)
        elif each == "North":
            path.append(n)
        else:
            path.append(e)

    return path
    util.raiseNotDefined()


def get_path(input):
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    n = Directions.NORTH
    e = Directions.EAST

    result = []
    for index in range(len(input)-1):
        i, j = input[index][0]
        i2, j2 = input[index+1][0]

        if i2 == i+1: result.append(e)
        elif i2 == i-1: result.append(w)
        elif j2 == j+1: result.append(n)
        elif j2 == j-1: result.append(s)
    return result

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    result = []
    qu = util.Queue()
    visited = set([])
    current = [problem.getStartState()]

    qu.push(current)

    while not qu.isEmpty():
        current = qu.pop()
        visited.add(current[-1])

        if problem.isGoalState(current[-1]):
            result = current
            break

        for each in problem.getSuccessors(current[-1]):
            if each[0] not in visited:
                temp = list(current)
                temp.append(each[0])
                qu.push(temp)
                visited.add(each[0])

    path = get_path(result)
    return path
    util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    n = Directions.NORTH
    e = Directions.EAST

    result = []
    qu = util.PriorityQueue()
    visited = set([])
    current = (problem.getStartState(), "", 0)
    qu.update(current, 0)
    costs = {}
    parents = {}
    parents[problem.getStartState()] = (problem.getStartState(), "")

    while not qu.isEmpty():
        cost, current= qu.pop()
        visited.add(current[0])

        if problem.isGoalState(current[0]):
            result = current[0]
            break

        for each in problem.getSuccessors(current[0]):
            if each[0] not in visited:
                qu.update(each, cost+each[2])
                if each[0] not in costs:
                    costs[each[0]] = cost+each[2]
                    parents[each[0]] = (current[0], each[1])
                elif costs[each[0]] > cost+each[2]:
                    costs[each[0]] = cost + each[2]
                    parents[each[0]] = (current[0], each[1])

    path = []
    while parents[result][0] != result:
        path.append(parents[result][1])
        result = parents[result][0]

    path.reverse()
    result = []
    for each in path:
        if each == "South":
            result.append(s)
        elif each == "West":
            result.append(w)
        elif each == "North":
            result.append(n)
        elif each == "East":
            result.append(e)

    return result
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    n = Directions.NORTH
    e = Directions.EAST

    result = []
    qu = util.PriorityQueue()
    visited = set([])
    current = (problem.getStartState(), "", 0)
    qu.update(current, 0)
    costs = {}
    parents = {}
    parents[problem.getStartState()] = (problem.getStartState(), "")

    while not qu.isEmpty():
        cost, current = qu.pop()
        visited.add(current[0])

        if problem.isGoalState(current[0]):
            result = current[0]
            break

        for each in problem.getSuccessors(current[0]):
            if each[0] not in visited:
                qu.update(each, cost + each[2] + heuristic(each[0], problem))
                if each[0] not in costs:
                    costs[each[0]] = cost + each[2]
                    parents[each[0]] = (current[0], each[1])
                elif costs[each[0]] > cost + each[2] + heuristic(each[0], problem):
                    costs[each[0]] = cost + each[2] + heuristic(each[0], problem)
                    parents[each[0]] = (current[0], each[1])

    path = []
    while parents[result][0] != result:
        path.append(parents[result][1])
        result = parents[result][0]

    path.reverse()
    result = []
    for each in path:
        if each == "South":
            result.append(s)
        elif each == "West":
            result.append(w)
        elif each == "North":
            result.append(n)
        elif each == "East":
            result.append(e)

    return result
    util.raiseNotDefined()

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
