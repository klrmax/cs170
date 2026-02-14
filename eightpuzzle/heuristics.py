def manhattan_heuristic(state: tuple, goal: tuple, grid_size: int = 3) -> float:
    #Sum of Manhattan distances for all misplaced tiles.
    dist = 0
    for i, tile in enumerate(state):
        if tile != 0:
            curr_row, curr_col = i // grid_size, i % grid_size
            goal_idx = goal.index(tile)
            goal_row, goal_col = goal_idx // grid_size, goal_idx % grid_size
            dist += abs(curr_row - goal_row) + abs(curr_col - goal_col)
    return float(dist)

def misplaced_tiles_heuristic(state: tuple, goal: tuple, grid_size: int = 3) -> float:
    #Count of tiles not in their goal position (excluding blank)
    return float(sum(1 for s, g in zip(state, goal) if s != g and s != 0))

def ucs_heuristic(state: tuple, goal: tuple, grid_size: int = 3) -> float:
    #UCS heuristic (always 0)
    return 0.0