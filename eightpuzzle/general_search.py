from collections import deque  
from typing import Callable, List, Any, Optional, Tuple
import heapq

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

def general_search(problem: Problem, queueing_function: Callable) -> Optional[Any]:
    nodes = [Node(problem.initial_state)]
    expanded_nodes = 0
    best_cost = {}

    while True:
        if not nodes:
            return None
        
        node = heapq.heappop(nodes)
        if node.state in best_cost and node.cost >= best_cost[node.state]:
            continue 
        best_cost[node.state] = node.cost
        expanded_nodes += 1 
        
        if problem.goal_test(node.state):
            # Print the solution path
            from heuristics import manhattan_heuristic
            path = node.get_path()
            
            for i, state in enumerate(path):
                h_val = manhattan_heuristic(state, problem.goal_state)
                print(f"The best state to expand with g(n) = {i} and h(n) = {int(h_val)} is...")
                state_list = list(state)
                print(f"[[{state_list[0]}, {state_list[1]}, {state_list[2]}],")
                print(f" [{state_list[3]}, {state_list[4]}, {state_list[5]}],")
                print(f" [{state_list[6]}, {state_list[7]}, {state_list[8]}]]")
                print()
            
            print("Goal state!")
            print(f"Solution depth was {node.depth}")
            print(f"Number of nodes expanded: {expanded_nodes}")
            return node, expanded_nodes
        
        new_nodes = expand(node, problem)
        nodes = queueing_function(nodes, new_nodes)
        
def uniform_cost_queueing(nodes: deque, new_nodes: List[Node]) -> deque:
    #UCS: Priority is just the path cost g(n)
    for node in new_nodes:
        node.evaluation_cost = node.cost
        heapq.heappush(nodes, node)  
    return nodes

def a_star_queueing(nodes: deque, new_nodes: List[Node], heuristic_fn: Callable) -> deque:
    #A*: Sort by f(n) = g(n) + h(n)
    for node in new_nodes:
        node.evaluation_cost = node.cost + heuristic_fn(node.state)
        heapq.heappush(nodes, node)
    return nodes 