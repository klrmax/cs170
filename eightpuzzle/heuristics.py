
def manhattan_heuristic(state: tuple, goal: tuple) -> float:
    # Standalone Manhattan distance calculator.
    # sum(x1 - x2 + y1 - y2) for all tiles except the blank (0).
    dist = 0
    for i, tile in enumerate(state):
        if tile != 0:
            # Current coordinates in 3x3 grid
            curr_row, curr_col = i // 3, i % 3
            
            # Target coordinates for this specific tile
            goal_idx = goal.index(tile)
            goal_row, goal_col = goal_idx // 3, goal_idx % 3
            
            dist += abs(curr_row - goal_row) + abs(curr_col - goal_col)
    return float(dist)


def misplaced_tiles_heuristic(state: tuple, goal: tuple) -> float:
    # Counts how many tiles are not in their target position.
    return sum(1 for s, g in zip(state, goal) if s != g and s != 0)

def ucs_heuristic(state: tuple, goal: tuple) -> float:
    return 0.0