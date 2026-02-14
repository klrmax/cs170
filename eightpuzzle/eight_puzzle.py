from general_search import Problem, a_star_queueing
from typing import List, Tuple, Optional


class EightPuzzleProblem(Problem):
    
    # Eight-Puzzle Problem: Slide tiles to reach the goal state
    # State: Tuple with 9 numbers (0 = blank tile)
    
    def __init__(self, initial_state: Tuple[int, ...], goal_state: Tuple[int, ...]):

        # Args: 
        # initial_state: Starting state of the puzzle
        # goal_state: Goal state of the puzzle

        if len(initial_state) != 9 or len(goal_state) != 9:
            raise ValueError("States must have exactly 9 elements!")
        
        super().__init__(initial_state, goal_state)
    
    def goal_test(self, state: Tuple[int, ...]) -> bool:
        # Checks if the current state matches the goal state
        return state == self.goal_state
    
    def get_blank_position(self, state: Tuple[int, ...]) -> int:
        # Finds the position of the blank tile (0)
        # Returns: Index from 0 to 8
        return state.index(0)
    
    
    def get_possible_moves(self, state: Tuple[int, ...]) -> List[str]:
        # Returns all possible movement directions
        # Returns: List with 'up', 'down', 'left', 'right'
        blank_pos = self.get_blank_position(state)
        # convert 1D index to 2D coordinates
        row = blank_pos // 3
        col = blank_pos % 3
        
        moves = []
        
        if row > 0:  # Can move up
            moves.append('north')
        if row < 2:  # Can move down
            moves.append('south')
        if col > 0:  # Can move left
            moves.append('west')
        if col < 2:  # Can move right
            moves.append('east')
        
        return moves
    
    def get_successors(self, state: Tuple[int, ...]) -> List[Tuple[int, ...]]:
        # Returns all successor states in one array (all possible moves)
        successors = []
        moves = self.get_possible_moves(state)
        
        for move in moves:
            new_state = self.move(state, move)
            if new_state:
                successors.append(new_state)
        
        return successors
    
    def move(self, state: Tuple[int, ...], direction: str) -> Optional[Tuple[int, ...]]:
        # Moves the blank tile in the specified direction if possible
        blank_pos = self.get_blank_position(state)
        row = blank_pos // 3
        col = blank_pos % 3
        
        # Calculate new position of the blank tile
        new_row, new_col = row, col
        
        if direction == 'north':
            new_row = row - 1
        elif direction == 'south':
            new_row = row + 1
        elif direction == 'west':
            new_col = col - 1
        elif direction == 'east':
            new_col = col + 1
        else:
            return None
        
        # Check if new position is valid
        if new_row < 0 or new_row > 2 or new_col < 0 or new_col > 2:
            return None
        
        # Calculate new index
        new_blank_pos = new_row * 3 + new_col
        
        # Swap the blank tile (0) with the target tile to create the new state
        state_list = list(state)
        state_list[blank_pos], state_list[new_blank_pos] = state_list[new_blank_pos], state_list[blank_pos]
        
        return tuple(state_list)


# Example usage
if __name__ == "__main__":
    from algorithms.general_search import general_search, a_star_queueing, uniform_cost_queueing
    from heuristics import misplaced_tiles_heuristic, manhattan_heuristic
    from functools import partial

    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    #hardcoded solvable initial state
    initial = (1, 2, 3, 4, 5, 6, 7, 0, 8)
    problem = EightPuzzleProblem(initial, goal)
    
    # Ask the user for the method
    print("=== Eight Puzzle Solver ===")

    print("Choose an algorithm:")
    print("1: Uniform Cost Search (UCS)")
    print("2: A* with Misplaced Tiles")
    print("3: A* with Manhattan Distance")
    
    choice = input("\nEnter choice (1-3): ")

    # Configure based on choice
    if choice == "1":
        print("\nSolving with UCS")
        strategy = uniform_cost_queueing
    elif choice == "2":
        print("\nSolving with A* (Misplaced Tiles)")
        h_func = partial(misplaced_tiles_heuristic, goal=problem.goal_state)
        strategy = partial(a_star_queueing, heuristic_fn=h_func)
    elif choice == "3":
        print("\nSolving with A* (Manhattan)")
        h_func = partial(manhattan_heuristic, goal=problem.goal_state)
        strategy = partial(a_star_queueing, heuristic_fn=h_func)
    else:
        print("Invalid choice. Defaulting to UCS.")
        strategy = uniform_cost_queueing

    result_node, total_expanded = general_search(problem, strategy)

    if result_node:
        print(f"Expanded Nodes: {total_expanded}")
        print(f"Path length: {result_node.depth}")
        print(f"Goal State Reached: {result_node.state}")
    else:
        print("No solution found. after expanding", total_expanded, "nodes.")