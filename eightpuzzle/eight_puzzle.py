from general_search import Problem
from typing import List, Tuple, Optional


class EightPuzzleProblem(Problem):
    # State: Tuple with 9 numbers (0 = blank tile)
    def __init__(self, initial_state: Tuple[int, ...], goal_state: Tuple[int, ...]):

        if len(initial_state) != 9 or len(goal_state) != 9:
            raise ValueError("States must have exactly 9 elements!")
        
        super().__init__(initial_state, goal_state)
    
    def goal_test(self, state: Tuple[int, ...]) -> bool:
        # Checks if the current state matches the goal state
        return state == self.goal_state
    
    def get_blank_position(self, state: Tuple[int, ...]) -> int:
        # Returns Index from 0 to 8
        return state.index(0)
    
    
    def get_possible_moves(self, state: Tuple[int, ...]) -> List[str]:
        # Returns all possible movement directions
        blank_pos = self.get_blank_position(state)
        # convert 1D index to 2D coordinates
        row = blank_pos // 3
        col = blank_pos % 3
        
        moves = []
        
        if row > 0:
            moves.append('north')
        if row < 2: 
            moves.append('south')
        if col > 0:  
            moves.append('west')
        if col < 2:  
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


