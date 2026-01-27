# def generalSearch(problem, queueing-function):
# nodes = makeQueue(makeNode(problem.initialState))
# while(nodes.goalTest()){
#     if(isEmpty(nodes)){
#         return failure
#     }
#     nodes = removeFront(nodes)
#     if(problem.goalTest(node.state)){
#         return node;
#     }
#     nodes = queueingFunction(nodes,expand(node,problem.operators))
# }

from collections import deque
from typing import Callable, List, Any, Optional


class Node:
    """Repräsentiert einen Knoten im Suchbaum"""
    
    def __init__(self, state, parent=None, depth=0):
        self.state = state
        self.parent = parent
        self.depth = depth
    
    def __repr__(self):
        return f"Node(state={self.state}, depth={self.depth})"
    
    def get_path(self):
        """Rekonstruiert den Pfad vom Startknoten zu diesem Knoten"""
        path = []
        current = self
        while current:
            path.append(current.state)
            current = current.parent
        return list(reversed(path))


class Problem:
    """Abstrakte Basisklasse für Suchprobleme"""
    
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state
    
    def goal_test(self, state) -> bool:
        """Prüft ob ein State das Ziel ist"""
        return state == self.goal_state
    
    def get_successors(self, state) -> List[Any]:
        """Gibt alle Nachfolger-States zurück (muss überschrieben werden)"""
        raise NotImplementedError


def expand(node: Node, problem: Problem) -> List[Node]:
    """Expandiert einen Knoten und gibt alle Nachfolger-Knoten zurück"""
    successors = []
    for successor_state in problem.get_successors(node.state):
        successor_node = Node(
            state=successor_state,
            parent=node,
            depth=node.depth + 1
        )
        successors.append(successor_node)
    return successors


def general_search(problem: Problem, queueing_function: Callable) -> Optional[Any]:
    """
    Generischer Suchalgorithmus (folgt dem Pseudocode exakt)
    
    Args:
        problem: Das zu lösende Problem
        queueing_function: Strategie zum Einfügen neuer Nodes
        
    Returns:
        Ziel-State bei Erfolg, None bei Misserfolg
    """
    # MAKE-QUEUE(MAKE-NODE(problem.INITIAL-STATE))
    nodes = deque([Node(problem.initial_state)])
    
    # loop do
    while True:
        # if EMPTY(nodes) then return "failure"
        if not nodes:
            return None
        
        # node = REMOVE-FRONT(nodes)
        node = nodes.popleft()
        
        # if problem.GOAL-TEST(node.STATE) succeeds then return node
        if problem.goal_test(node.state):
            return node.state
        
        # nodes = QUEUEING-FUNCTION(nodes, EXPAND(node, problem.OPERATORS))
        new_nodes = expand(node, problem)
        nodes = queueing_function(nodes, new_nodes)


# Queueing Functions für verschiedene Strategien

def breadth_first_queueing(nodes: deque, new_nodes: List[Node]) -> deque:
    """BFS: Neue Nodes am Ende anfügen"""
    nodes.extend(new_nodes)
    return nodes


def depth_first_queueing(nodes: deque, new_nodes: List[Node]) -> deque:
    """DFS: Neue Nodes am Anfang einfügen"""
    return deque(new_nodes + list(nodes))