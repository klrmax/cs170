import time
import csv
from functools import partial
from general_search import general_search
from eight_puzzle import EightPuzzleProblem
from heuristics import misplaced_tiles_heuristic, manhattan_heuristic, ucs_heuristic


TEST_CASES = {
    'testcase_1': (1, 2, 3, 4, 5, 6, 7, 8, 0),  # depth 0
    'testcase_2': (1, 2, 3, 4, 5, 6, 0, 7, 8),  # depth 2
    'testcase_3': (1, 2, 3, 5, 0, 6, 4, 7, 8),  # depth 4
    'testcase_4': (1, 3, 6, 5, 0, 2, 4, 7, 8),  # depth 8
    'testcase_5': (1, 3, 6, 5, 0, 7, 4, 8, 2),  # depth 12
    'testcase_6': (1, 6, 7, 5, 0, 3, 4, 8, 2),  # depth 16
    'testcase_7': (7, 1, 2, 4, 8, 5, 6, 3, 0),  # depth 20
    'testcase_8': (0, 7, 2, 4, 6, 1, 3, 5, 8),  # depth 24
}

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)


def run_test(test_name, initial, algo_name, heuristic_fn, grid_size=3):
    problem = EightPuzzleProblem(initial, GOAL, grid_size)
    
    start = time.time()
    result_node, nodes = general_search(problem, heuristic_fn)
    duration = time.time() - start
    
    return {
        'test_case': test_name,
        'algorithm': algo_name,
        'depth': result_node.depth if result_node else 'N/A',
        'nodes': nodes,
        'time_s': round(duration, 6)
    }


def run_all_tests():
    results = []
    
    algorithms = [
        ('UCS', ucs_heuristic),
        ('A* Misplaced', misplaced_tiles_heuristic),
        ('A* Manhattan', manhattan_heuristic),
    ]
    
    total = len(TEST_CASES) * len(algorithms)
    current = 0
    
    for test_name, initial in TEST_CASES.items():
        print(f"\n{test_name}: {initial}")
        
        for algo_name, heuristic in algorithms:
            current += 1
            
            h_func = partial(heuristic, goal=GOAL, grid_size=3)  # Wrap heuristic for general_search

            try:
                result = run_test(test_name, initial, algo_name, h_func)
                results.append(result)  
                print(f"  [{current}/{total}] {algo_name:20} - "
                      f"Depth: {result['depth']:2}, Nodes: {result['nodes']:6}, "
                      f"Time: {result['time_s']:.4f}s")
            except Exception as e:
                print(f"  [{current}/{total}] {algo_name:20} - ERROR: {e}")
    
    with open('test_results.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['test_case', 'algorithm', 'depth', 
                                                 'nodes', 'time_s'])
        writer.writeheader()
        writer.writerows(results)
    

    print("Results saved to test_results.csv")
    
    return results

if __name__ == "__main__":
     results = run_all_tests()