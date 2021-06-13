# Graphs
Two Python modules that provide implementations of an undirected, unweighted graph and a directed, weighted graph.
The undirected, unweighted graph is represented as an adjacency list and the directed, weighted graph is represented as an adjancency matrix. 

## Undirected Graph Features
- Ability to add and remove vertices and edges from the graph
- Determines whether a provided path is valid or not
- Depth-first search
- Breadth-first search
- Count connected components
- Cycle detection

## Directed Graph Features
- Ability to add and remove vertices and edges from the graph
- Determines whether or a provided path is valid or not
- Depth-first search
- Breadth-first search
- Cycle detection
- Dijkstra's Algorithm to determine shortest path between vertices

## Technologies
- Python 3.8

## How To Use
Ensure Python 3.6 or greater is installed.  
```console
foo@bar:~$ python3 --version
```

Clone this repository.  
```console
foo@bar:~$ git clone https://github.com/dakotajunkman/Graphs
```
Import the desired class in to your Python file.
```python
from d_graph import DirectedGraph
```
```python
from ud_graph import UndirectedGraph
```
