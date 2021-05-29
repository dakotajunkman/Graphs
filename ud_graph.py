# Course: CS 261 Data Structures
# Author: Dakota Junkman
# Assignment: 6
# Description: Undirected graph implementation

import heapq
from collections import deque

class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Adds a new vertex to the graph.
        Will not allow vertex to be added if a vertex of the same name exists in the graph.
        param v: graph vertex
        return: None
        """
        # do not allow a vertex of the same name to be added
        if v in self.adj_list:
            return

        self.adj_list[v] = []

    def add_edge(self, u: str, v: str) -> None:
        """
        Adds a new edge to the graph. Will create vertex when the passed in vertex is not in the graph.
        Will not allow duplicate edges to be made.
        param u: graph vertex
        param v: graph vertex
        return: None
        """
        # handle duplicate edges or u and v being the same vertex
        # since graph is undirected we only need to check connection in one direction
        if u == v or (v in self.adj_list and u in self.adj_list[v]):
            return
        
        if u not in self.adj_list:
            self.adj_list[u] = []
        
        if v not in self.adj_list:
            self.adj_list[v] = []
        
        self.adj_list[v].append(u)
        self.adj_list[u].append(v)
        
    def remove_edge(self, v: str, u: str) -> None:
        """
        Removes the edge between the passed-in vertices.
        param v: graph vertex
        param u: graph vertex
        return: None
        """
        if v not in self.adj_list or u not in self.adj_list or v not in self.adj_list[u]:
            return
        
        self.adj_list[u].remove(v)
        self.adj_list[v].remove(u)

    def remove_vertex(self, v: str) -> None:
        """
        Removes the vertex, and all edges incident upon it, from the graph.
        param v: graph vertex
        return: None
        """
        if v not in self.adj_list:
            return
        
        self.adj_list.pop(v)

        for key in self.adj_list:
            if v in self.adj_list[key]:
                self.adj_list[key].remove(v)

    def get_vertices(self) -> []:
        """
        Returns a list of all the vertices in the graph.
        """
        return [key for key in self.adj_list]

    def get_edges(self) -> []:
        """
        Returns a list of tuples containing each edge in the graph.
        Tuples will contain names of connected vertices.
        """
        edges = []
        seen = set()

        # loop over each vertex and its corresponding connections
        # add the vertex to a set to keep track of visited vertices
        # check connected vertices for set presence to ensure duplicate edges are not added
        for key in self.adj_list:
            seen.add(key)
            for val in self.adj_list[key]:
                if val not in seen:
                    edges.append((key, val))
        return edges


    def is_valid_path(self, path: []) -> bool:
        """
        Determines whether it is possible to travel from the first vertex to the last vertex over edges.
        An empty path is considered valid.
        param path: list of vertices
        return: True when path is valid, else False
        """
        # handle edge cases
        if len(path) == 0 or (len(path) == 1 and path[0] in self.adj_list):
            return True
        
        if len(path) == 1 and path[0] not in self.adj_list:
            return False

        # loop from 2nd element to last and check presence in previous elements connections
        # when a connection is not present we stop and return False
        # when end of loop is reached a valid path must be the case
        for i in range(1, len(path)):
            if path[i - 1] not in self.adj_list or path[i] not in self.adj_list[path[i - 1]]:
                return False
        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Performs a depth-first search of the graph and builds an in-order list of visited vertices.
        Adjacent vertices are pushed on to the stack in ascending order.
        param v_start: vertex to start the search from
        param v_end: vertex to stop the search at (defaults to None)
        return: list of vertices visited in the order they were visited
        """
        # handle when start vertex is not in the graph
        if v_start not in self.adj_list:
            return []

        # build necessary data structures
        vertices = []
        stack = []
        seen = set()

        stack.append(v_start)

        # break the loop when stack is empty, or when v_end has been encountered
        while len(stack) > 0 and v_end not in seen:
            item = stack.pop()
            if item not in seen:
                vertices.append(item)
                seen.add(item)

                # create a min heap of adjacent vertices and pop them off to add to the stack
                # this guarantees items are pushed to the stack in ascending order
                sorted_vertices = self.heapsort(self.adj_list[item])
                while len(sorted_vertices) > 0:
                    stack.append(sorted_vertices.pop())
        
        return vertices


    def bfs(self, v_start, v_end=None) -> []:
        """
        Performs a breadth-first search of the graph and builds an in-order list of visited vertices.
        Adjacent vertices are enqueued in ascending order.
        param v_start: vertex to start the search from
        param v_end: vertex to stop the search at (defaults to None)
        return: list of vertices visited in the order they were visited
        """
        if v_start not in self.adj_list:
            return []
        
        # build necessary data structures
        vertices = []
        queue = deque()
        seen = set()

        queue.append(v_start)

        # break the loop when queue is empty, or when v_end has been encountered
        while len(queue) > 0 and v_end not in seen:
            item = queue.popleft()
            if item not in seen:
                vertices.append(item)
                seen.add(item)

                sorted_vertices = self.heapsort(self.adj_list[item])
                for i in range(len(sorted_vertices)):
                    queue.append(sorted_vertices[i])

        return vertices

    def count_connected_components(self) -> int:
        """
        Counts the number of connected components in the graph.
        return: number of connected components
        """
        vertices = set()
        count = 0
        
        # loop over each vertex and check if it has been visited
        # if not, run DFS to get all connected components and increment count
        # take set union to update visited vertices
        # each call to DFS represents a new connected component
        for key in self.adj_list:
            if key not in vertices:
                count += 1
                new_vertices = set(self.dfs(key))
                vertices = vertices | new_vertices
        return count

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """

    def heapsort(self, lst: list) -> list:
        """
        Sorts the passed-in list in to a new list.
        param lst: list to sort
        return: sorted list
        """
        # transform copy of list in to a heap
        new_lst = list(lst)
        heapq.heapify(new_lst)

        # pop the min value continuously in to a new list
        return [heapq.heappop(new_lst) for _ in range(len(lst))]
   


if __name__ == '__main__':

    # print("\nPDF - method add_vertex() / add_edge example 1")
    # print("----------------------------------------------")
    # g = UndirectedGraph()
    # print(g)

    # for v in 'ABCDE':
    #     g.add_vertex(v)
    # print(g)

    # g.add_vertex('A')
    # print(g)

    # for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
    #     g.add_edge(u, v)
    # print(g)


    # print("\nPDF - method remove_edge() / remove_vertex example 1")
    # print("----------------------------------------------------")
    # g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    # g.remove_vertex('DOES NOT EXIST')
    # g.remove_edge('A', 'B')
    # g.remove_edge('X', 'B')
    # print(g)
    # g.remove_vertex('D')
    # print(g)


    # print("\nPDF - method get_vertices() / get_edges() example 1")
    # print("---------------------------------------------------")
    # g = UndirectedGraph()
    # print(g.get_edges(), g.get_vertices(), sep='\n')
    # g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    # print(g.get_edges(), g.get_vertices(), sep='\n')


    # print("\nPDF - method is_valid_path() example 1")
    # print("--------------------------------------")
    # g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    # test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    # for path in test_cases:
    #     print(list(path), g.is_valid_path(list(path)))


    # print("\nPDF - method dfs() and bfs() example 1")
    # print("--------------------------------------")
    # edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    # g = UndirectedGraph(edges)
    # test_cases = 'ABCDEGH'
    # for case in test_cases:
    #     print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    # print('-----')
    # for i in range(1, len(test_cases)):
    #     v1, v2 = test_cases[i], test_cases[-1 - i]
    #     print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()


    # print("\nPDF - method has_cycle() example 1")
    # print("----------------------------------")
    # edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    # g = UndirectedGraph(edges)
    # test_cases = (
    #     'add QH', 'remove FG', 'remove GQ', 'remove HQ',
    #     'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
    #     'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
    #     'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
    #     'add FG', 'remove GE')
    # for case in test_cases:
    #     command, edge = case.split()
    #     u, v = edge
    #     g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
    #     print('{:<10}'.format(case), g.has_cycle())