# Course: CS261 - Data Structures
# Author: Dakota Junkman
# Assignment: 6
# Description: Directed graph implementation

import heapq
from collections import deque

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Adds a new vertex to the graph. 
        return: number of vertices in the graph
        """
        # update vertex count
        self.v_count += 1

        # add new row to the matrix
        self.adj_matrix.append([0] * self.v_count)

        # extend each other row to include the new vertex
        for i in range(len(self.adj_matrix) - 1):
            self.adj_matrix[i].append(0)
        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Adds edge between src and dst to the graph.
        param src: beginning of the edge
        param dst: end of the edge
        param weight: weight of the edge
        return: None
        """
        if weight < 1:
            return

        if src == dst:
            return
        
        if not (0 <= src < self.v_count) or not (0 <= dst < self.v_count):
            return
        
        self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        Removes an edge between src and dst.
        param src: beginning of edge
        param dst: end of edge
        return: None
        """
        if not (0 <= src < self.v_count) or not (0 <= dst < self.v_count):
            return

        self.adj_matrix[src][dst] = 0      

    def get_vertices(self) -> []:
        """
        Returns a list of vertices in the graph.
        """
        return [num for num in range(self.v_count)]

    def get_edges(self) -> []:
        """
        Returns a list of each vertex in the graph.
        return: a list of tuples
            tuple[0] = edge source
            tuple[1] = edge destination
            tuple[2] = edge weight
        """
        edges = []

        # loop over each position in the matrix
        # when value at the position is non-zero an edge exists and is added to the edge list
        for i in range(len(self.adj_matrix)):
            for j in range(len(self.adj_matrix[i])):
                if self.adj_matrix[i][j] != 0:
                    edges.append((i, j, self.adj_matrix[i][j]))
        return edges

    def is_valid_path(self, path: []) -> bool:
        """
        Determines if a valid path exists from the start vertex to end vertex.
        param path: list of vertices in the path
        return: True when path is valid, else False
        """
        if len(path) == 0 or (len(path) == 1 and 0 <= path[0] < self.v_count):
            return True
        
        if len(path) == 1 and not (0 <= path[0] < self.v_count):
            return False
        
        # start at second vertex and loop
        # check previous vertex for an edge to the current vertex
        # return False when an edge doesn't exist
        # when end of loop is reached we can return True
        for i in range(1, len(path)):
            cur = path[i]
            prev = path[i - 1]
            if self.adj_matrix[prev][cur] == 0:
                return False
        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Performs a depth-first search starting at the passed-in vertex.
        param v_start: vertex to start the search
        param v_end: vertex to end the search (defaults to None)
        return: list of visited vertices
        """
        if not (0 <= v_start < self.v_count):
            return []

        vertices = []
        stack = []
        seen = set()

        stack.append(v_start)

        while stack and v_end not in seen:
            item = stack.pop()
            if item not in seen:
                seen.add(item)
                vertices.append(item)

                # push adjacent vertices on to the stack
                # iterate over adjacent vertices backwards
                # this ensures vertices are explored in asending order
                adjacent = self.adj_matrix[item]
                for i in range(len(adjacent) - 1, -1, -1):
                    if adjacent[i] != 0:
                        stack.append(i)
        return vertices
        

    def bfs(self, v_start, v_end=None) -> []:
        """
        Performs a breadth-first search starting at the passed-in vertex.
        param v_start: vertex to start the search
        param v_end: vertex to end the search (defaults to None)
        return: list of visited vertices
        """
        if not (0 <= v_start < self.v_count):
            return []
        
        vertices = []
        queue = deque()
        seen = set()

        queue.append(v_start)

        while queue and v_end not in seen:
            item = queue.popleft()
            if item not in seen:
                seen.add(item)
                vertices.append(item)

                # enqueue adjacent vertices in ascending order
                adjacent = self.adj_matrix[item]
                for i in range(len(adjacent)):
                    if adjacent[i] != 0:
                        queue.append(i)
        return vertices

    def has_cycle(self):
        """
        Determines whether or not the graph contains a cycle.
        Requires detect_cycle helper method. 
        return: True when cycle is found, else False
        """
        for i in range(len(self.adj_matrix)):
            if self.detect_cycle(i):
                return True
        return False
    
    def detect_cycle(self, vertex: int) -> bool:
        """
        Detects whether or not the graph contains a cycle using DFS.
        param vertex: vertex to start DFS from
        return: True when cycle found, else False
        """
        visited = set()
        stack = []

        # stack will hold vertex and its parent
        stack.append(vertex)

        while stack:
            cur_vertex = stack.pop()
            if cur_vertex not in visited:
                visited.add(cur_vertex)

                # examine adjacent vertices
                # when we make it back to the original vertex, we have a cycle
                for i in range(len(self.adj_matrix[cur_vertex])):
                    if self.adj_matrix[cur_vertex][i] != 0 and i not in visited:
                        stack.append(i)
                    elif self.adj_matrix[cur_vertex][i] != 0 and i == vertex:
                        return True
        return False

    def dijkstra(self, src: int) -> []:
        """
        TODO: Write this implementation
        """
        pass

if __name__ == '__main__':

    # print("\nPDF - method add_vertex() / add_edge example 1")
    # print("----------------------------------------------")
    # g = DirectedGraph()
    # print(g)
    # for _ in range(5):
    #     g.add_vertex()
    # print(g)

    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # for src, dst, weight in edges:
    #     g.add_edge(src, dst, weight)
    # print(g)


    # print("\nPDF - method get_edges() example 1")
    # print("----------------------------------")
    # g = DirectedGraph()
    # print(g.get_edges(), g.get_vertices(), sep='\n')
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # print(g.get_edges(), g.get_vertices(), sep='\n')


    # print("\nPDF - method is_valid_path() example 1")
    # print("--------------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    # for path in test_cases:
    #     print(path, g.is_valid_path(path))


    # print("\nPDF - method dfs() and bfs() example 1")
    # print("--------------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # for start in range(5):
    #     print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)


    # print("\nPDF - dijkstra() example 1")
    # print("--------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # for i in range(5):
    #     print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    # g.remove_edge(4, 3)
    # print('\n', g)
    # for i in range(5):
    #     print(f'DIJKSTRA {i} {g.dijkstra(i)}')