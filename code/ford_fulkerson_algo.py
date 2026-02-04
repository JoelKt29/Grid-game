# Joel Khayat and Allan Pariente
import numpy as np

class Graph:
    """
    Attributes: 
    -----------
    adjency: np.array

    Graph class.
    """
    def __init__(self, numNodes, edges):
        """
        Parameters:
        -----------
        numNodes: int
        edges: list[(int, int, int)]

        Defines the adjency matrix of the graph.
        """
        self.adjency = np.zeros((numNodes, numNodes))
        for edge in edges:
            self.adjency[edge[0], edge[1]] = edge[2]

    def bfs(self, source, target, parent):
        """
        Parameters:
        -----------
        source: int
        target: int
        parent: list[int]

        Output:
        -------
        bool

        Returns True if there is a path from source to target in the graph, using breadth-first algorithm, False otherwise, and updates the parent list (to remind the path), using side effect.
        """
        visited = [False] * len(self.adjency)
        queue = [source]
        visited[source] = True
        while queue:
            nodeQueue = queue.pop(0)
            for node in range(len(self.adjency[nodeQueue])):
                if visited[node] == False and self.adjency[nodeQueue][node] > 0:
                    queue.append(node)
                    visited[node] = True
                    parent[node] = nodeQueue
                    if node == target:
                        return True
        return False

    def ford_fulkerson(self, source, target):
        """
        Parameters:
        -----------
        source: int
        target: int
        
        Output:
        -------
        int

        Returns the maximal flow in the graph, using the Ford-Fulkerson algorithm, and updates the adjency matrix (using side effect), to remember the maximal flow path.
        """
        parent = [-1] * len(self.adjency) # Warining: Not necessary, difficult to prove correction bcause there is rests of values. Waring effet de bord
        max_flow = 0
        while self.bfs(source, target, parent):
            path_flow = float("Inf")
            node = target # calculating the flow passing through the path
            while node != source:
                path_flow = min(path_flow, self.adjency[parent[node]][node]) # because if the capacity of the edge parent[s] -> s is inferior to path_flow, then, all path_flow cannot pass through this edge
                node = parent[node]
            max_flow += path_flow
            
            node = target # updating the capacities of the edges
            while node != source:
                prevNode = parent[node]
                self.adjency[prevNode][node] -= path_flow
                self.adjency[node][prevNode] += path_flow
                node = parent[node]
        
        return max_flow