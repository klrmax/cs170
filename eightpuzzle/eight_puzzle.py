from general_search import Problem
from typing import List, Tuple, Optional

class EightPuzzleProblem(Problem):
    def __init__(self, initial_state: Tuple[int, ...], goal_state: Tuple[int, ...], grid_size: int = 3):
        self.grid_size = grid_size
        expected_length = grid_size * grid_size
        
        if len(initial_state) != expected_length or len(goal_state) != expected_length:
            raise ValueError(f"States must have exactly {expected_length} elements!")
        
        super().__init__(initial_state, goal_state)
    
    def goal_test(self, state: Tuple[int, ...]) -> bool:
        return state == self.goal_state
    
    def get_blank_position(self, state: Tuple[int, ...]) -> int:
        return state.index(0)
    
    def get_possible_moves(self, state: Tuple[int, ...]) -> List[str]:
        blank_pos = self.get_blank_position(state)
        row = blank_pos // self.grid_size  
        col = blank_pos % self.grid_size   
        
        moves = []
        if row > 0: moves.append('north')
        if row < self.grid_size - 1: moves.append('south')
        if col > 0: moves.append('west')
        if col < self.grid_size - 1: moves.append('east')
        return moves
    
    def get_successors(self, state: Tuple[int, ...]) -> List[Tuple[int, ...]]:
        successors = []
        moves = self.get_possible_moves(state)
        
        for move in moves:
            new_state = self.move(state, move)
            if new_state:
                successors.append(new_state)
        return successors
    
    def move(self, state: Tuple[int, ...], direction: str) -> Optional[Tuple[int, ...]]:
        blank_pos = self.get_blank_position(state)
        row = blank_pos // self.grid_size  
        col = blank_pos % self.grid_size  
        
        new_row, new_col = row, col
        if direction == 'north': new_row = row - 1
        elif direction == 'south': new_row = row + 1
        elif direction == 'west': new_col = col - 1
        elif direction == 'east': new_col = col + 1
        else: return None
        
        if new_row < 0 or new_row >= self.grid_size or new_col < 0 or new_col >= self.grid_size: 
            return None
        
        new_blank_pos = new_row * self.grid_size + new_col
        state_list = list(state)
        state_list[blank_pos], state_list[new_blank_pos] = state_list[new_blank_pos], state_list[blank_pos]
        
        return tuple(state_list)