from algorithms.graph_search import Problem
from typing import List, Tuple


class NQueensProblem(Problem):
    """N-Queens Problem: Platziere N Damen auf einem NxN Schachbrett ohne Konflikte"""
    
    def __init__(self, n: int):
        self.n = n
        # Initial state: leeres Brett (noch keine Queens platziert)
        initial_state = tuple()
        # Goal state: N Queens platziert (Länge = N)
        goal_state = None  # Wird nicht direkt verglichen, sondern über goal_test geprüft
        super().__init__(initial_state, goal_state)
    
    def goal_test(self, state: Tuple[int, ...]) -> bool:
        """Ziel erreicht wenn N Queens platziert sind und keine Konflikte existieren"""
        return len(state) == self.n
    
    def get_successors(self, state: Tuple[int, ...]) -> List[Tuple[int, ...]]:
        """
        Generiert alle möglichen Nachfolger-States.
        Platziert eine Queen in der nächsten Zeile (len(state)) in jeder möglichen Spalte.
        """
        if len(state) == self.n:
            return []  # Bereits N Queens platziert
        
        successors = []
        next_row = len(state)  # Nächste Zeile zum Platzieren
        
        for col in range(self.n):
            # Prüfe ob diese Position sicher ist
            if self._is_safe(state, next_row, col):
                new_state = state + (col,)
                successors.append(new_state)
        
        return successors
    
    def _is_safe(self, state: Tuple[int, ...], row: int, col: int) -> bool:
        """
        Prüft ob eine Queen an Position (row, col) sicher ist.
        State repräsentiert bereits platzierte Queens.
        """
        for placed_row, placed_col in enumerate(state):
            # Gleiche Spalte?
            if placed_col == col:
                return False
            
            # Gleiche Diagonale?
            if abs(placed_row - row) == abs(placed_col - col):
                return False
        
        return True
    
    def visualize_solution(self, state: Tuple[int, ...]) -> str:
        """Visualisiert die Lösung als Schachbrett"""
        if len(state) != self.n:
            return "Keine vollständige Lösung!"
        
        board = []
        for row in range(self.n):
            line = []
            for col in range(self.n):
                if state[row] == col:
                    line.append('Q')
                else:
                    line.append('.')
            board.append(' '.join(line))
        
        return '\n'.join(board)


# Beispiel-Verwendung
if __name__ == "__main__":
    from algorithms.graph_search import general_search, breadth_first_queueing, depth_first_queueing
    
    # Variable für Board-Größe
    N = 4
    
    print(f"=== {N}-Queens Problem ===\n")
    
    # Problem erstellen
    problem = NQueensProblem(N)
    
    # Mit BFS lösen
    print("Lösung mit BFS:")
    solution_bfs = general_search(problem, breadth_first_queueing)
    if solution_bfs:
        print(f"Gefundene Lösung: {solution_bfs}")
        print(problem.visualize_solution(solution_bfs))
    else:
        print("Keine Lösung gefunden!")
    
    print("\n" + "="*30 + "\n")
    
    # Mit DFS lösen
    print("Lösung mit DFS:")
    solution_dfs = general_search(problem, depth_first_queueing)
    if solution_dfs:
        print(f"Gefundene Lösung: {solution_dfs}")
        print(problem.visualize_solution(solution_dfs))
    else:
        print("Keine Lösung gefunden!")
    
    print("\n" + "="*30 + "\n")
    
    # Jetzt mit N=8 testen
    N = 8
    print(f"=== {N}-Queens Problem ===\n")
    problem_8 = NQueensProblem(N)

    print("Lösung mit BFS:")
    solution_8 = general_search(problem_8, breadth_first_queueing)
    if solution_8:
        print(f"Gefundene Lösung: {solution_8}")
        print(problem_8.visualize_solution(solution_8))
    else:
        print("Keine Lösung gefunden!")

    
    print("Lösung mit DFS:")
    solution_8 = general_search(problem_8, depth_first_queueing)
    if solution_8:
        print(f"Gefundene Lösung: {solution_8}")
        print(problem_8.visualize_solution(solution_8))
    else:
        print("Keine Lösung gefunden!")