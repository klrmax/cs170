import heapq
from typing import Callable, List, Any, Optional, Tuple

class Node: 
    def __init__(self, state, parent=None, depth=0, cost=0, evaluation_cost=0):
        self.state = state
        self.parent = parent
        self.depth = depth
        self.cost = cost # Path cost g(n)
        self.evaluation_cost = evaluation_cost # f(n) = g(n) + h(n)
    
    def __repr__(self):
        return f"Node(state={self.state}, depth={self.depth}, cost={self.cost}, evaluation_cost={self.evaluation_cost})"

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
        raise NotImplementedError

    def get_step_cost(self, from_state, to_state) -> float:
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

def general_search(problem: Problem, heuristic_fn: Callable) -> Tuple[Optional[Node], int]:
    initial_node = Node(problem.initial_state)
    initial_node.evaluation_cost = 0
    nodes = [initial_node]
    heapq.heapify(nodes)
    expanded_nodes = 0
    best_cost = {} #Dict for best cost per state

    while nodes:
        node = heapq.heappop(nodes)
        
        if node.state in best_cost and node.cost >= best_cost[node.state]:
            continue 

        best_cost[node.state] = node.cost
        expanded_nodes += 1

        if problem.goal_test(node.state):
            return node, expanded_nodes
        
        new_nodes = expand(node, problem)

        for new_node in new_nodes:
            h_n = heuristic_fn(new_node.state, problem.goal_state)
            new_node.evaluation_cost = new_node.cost + h_n  # f(n) = g(n) + h(n)
            heapq.heappush(nodes, new_node)
    
    return None, expanded_nodes