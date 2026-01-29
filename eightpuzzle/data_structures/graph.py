class Graph:
    """Einfache Graph-Datenstruktur mit Adjazenzliste"""
    
    def __init__(self):
        self.adjacency_list = {}
    
    def add_edge(self, from_node, to_node):
        """Fügt eine gerichtete Kante hinzu"""
        if from_node not in self.adjacency_list:
            self.adjacency_list[from_node] = []
        self.adjacency_list[from_node].append(to_node)
    
    def add_undirected_edge(self, node1, node2):
        """Fügt eine ungerichtete Kante hinzu"""
        self.add_edge(node1, node2)
        self.add_edge(node2, node1)
    
    def get_neighbors(self, node):
        """Gibt alle Nachbarn eines Knotens zurück"""
        return self.adjacency_list.get(node, [])
    
    def __repr__(self):
        return f"Graph({self.adjacency_list})"