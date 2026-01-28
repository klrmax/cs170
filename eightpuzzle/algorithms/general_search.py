from collections import deque
from typing import Callable, List, Any, Optional


class Node:
    # Represents a search tree node    
    def __init__(self, state, parent=None, depth=0, cost=0, evaluation_cost=0):
        self.state = state
        self.parent = parent
        self.depth = depth
        self.cost = cost # Path cost g(n)
        self.evaluation_cost = evaluation_cost # f(n) = g(n) + h(n)
    
    #string representation for debugging
    def __repr__(self):
        return f"Node(state={self.state}, depth={self.depth}, cost={self.cost}, evaluation_cost={self.evaluation_cost})"

    # enables comparison based on evaluation cost
    def __lt__(self, other):
        return self.evaluation_cost < other.evaluation_cost

    def get_path(self):
        #Reconstructs the solution path from root to this node
        path = []
        current = self
        while current:
            path.append(current.state)
            current = current.parent
        return list(reversed(path))


class Problem:
    
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state
    
    def goal_test(self, state) -> bool:
        return state == self.goal_state
    
    def get_successors(self, state) -> List[Any]:
        #returns all successor states from the given state
        raise NotImplementedError

    def get_step_cost(self, from_state, to_state) -> float:
        #Returns the cost of moving from from_state to to_state
        return 1.0 # Default cost

def expand(node: Node, problem: Problem) -> List[Node]:
    #Expands a node and returns all successor nodes
    successors = []
    for successor_state in problem.get_successors(node.state):
        step_cost = problem.get_step_cost(node.state, successor_state)
        successor_node = Node(
            state=successor_state,
            parent=node,
            depth=node.depth + 1,
            cost=node.cost + step_cost  # Accumulate cost
        )
        successors.append(successor_node)
    return successors

# General Search Algorithm (with expanded nodes counter)
def general_search(problem: Problem, queueing_function: Callable) -> Optional[Any]:
    nodes = deque([Node(problem.initial_state)])
    expanded_nodes = 0

    while True:
        # if EMPTY(nodes) then return "failure"
        if not nodes:
            return None
        
        # node = REMOVE-FRONT(nodes)
        node = nodes.popleft()
        expanded_nodes += 1
        
        # if problem.GOAL-TEST(node.STATE) succeeds then return node
        if problem.goal_test(node.state):
            return node, expanded_nodes
        
        # nodes = QUEUEING-FUNCTION(nodes, EXPAND(node, problem.OPERATORS))
        new_nodes = expand(node, problem)
        nodes = queueing_function(nodes, new_nodes)
        
        return None, expanded_nodes
    


# Different queueing functions

def breadth_first_queueing(nodes: deque, new_nodes: List[Node]) -> deque:
    nodes.extend(new_nodes)
    return nodes


def depth_first_queueing(nodes: deque, new_nodes: List[Node]) -> deque:
    return deque(new_nodes + list(nodes))

def uniform_cost_queueing(nodes: deque, new_nodes: List[Node]) -> deque:
    # UCS: Priority is just the path cost g(n)
    for node in new_nodes:
        node.evaluation_cost = node.cost

    combined = list(nodes) + new_nodes
    combined.sort() # Uses Node.__lt__
    return deque(combined)


def a_star_queueing(nodes: deque, new_nodes: List[Node], heuristic_fn: Callable) -> deque:
    #A*: Sort by f(n) = g(n) + h(n)
    for node in new_nodes:
        node.evaluation_cost = node.cost + heuristic_fn(node.state)
    
    combined = list(nodes) + new_nodes
    combined.sort() # Uses the Node's __lt__ method
    return deque(combined)