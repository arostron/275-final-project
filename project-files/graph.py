"""
Directed Graph Class from 275 (Modified)

This graph class is a container that holds a set
of vertices and a list of directed edges.
Edges are modelled as tuples (u,v) of vertices.
A dictonary mapping vertices to their respective neighbour nodes is also present
"""

class Graph:
    def __init__(self, Vertices = set(), Edges = list()):
        """
        Construct a graph with a shallow copy of
        the given set of vertices and given list of edges.

        Efficiency: O(# vertices + # edges)

        >>> g = Graph({1,2,3}, [(1,2), (2,3)])
        >>> g.vertices == {1,2,3}
        True
        >>> g.edges == [(1,2), (2,3)]
        True
        >>> h1 = Graph()
        >>> h2 = Graph()
        >>> h1.add_vertex(1)
        >>> h1.vertices == {1}
        True
        >>> h2.vertices == set()
        True
        """

        self.vertices = set()
        self.edges = list()
        self.neighbour = dict()

        for v in Vertices:
            self.add_vertex(v)
        for e in Edges:
            self.add_edge(e)


    def add_vertex(self, v):
        """
        Add a vertex v to the graph.
        If v exists in the graph, do nothing.

        Efficiency: O(1)

        >>> g = Graph()
        >>> len(g.vertices)
        0
        >>> g.add_vertex(1)
        >>> g.add_vertex("vertex")
        >>> "vertex" in g.vertices
        True
        >>> 2 in g.vertices
        False
        """

        self.vertices.add(v)

    def add_edge(self, e):
        """
        Add edge e to the graph.
        Raise an exception if the endpoints of
        e are not in the graph.

        Efficiency: O(1)

        >>> g = Graph()
        >>> g.add_vertex(1)
        >>> g.add_vertex(2)
        >>> g.add_edge((1,2))
        >>> (1,2) in g.edges
        True
        >>> (2,1) in g.edges
        False
        >>> g.add_edge((1,2))
        >>> g.edges
        [(1, 2), (1, 2)]
        """

        if not self.is_vertex(e[0]) or not self.is_vertex(e[1]):
            raise ValueError("An endpoint is not in graph")
        self.edges.append(e)

    def is_vertex(self, v):
        """
        Check if vertex v is in the graph.
        Return True if it is, False if it is not.

        Efficiency: O(1) - Sweeping some discussion
        about hashing under the rug.

        >>> g = Graph({1,2})
        >>> g.is_vertex(1)
        True
        >>> g.is_vertex(3)
        False
        >>> g.add_vertex(3)
        >>> g.is_vertex(3)
        True
        """

        return v in self.vertices

    def is_edge(self, e):
        """
        Check if edge e is in the graph.
        Return True if it is, False if it is not.

        Efficiency: O(# edges)

        >>> g = Graph({1,2}, [(1,2)])
        >>> g.is_edge((1,2))
        True
        >>> g.is_edge((2,1))
        False
        >>> g.add_edge((1,2))
        >>> g.is_edge((1,2))
        True
        """

        return e in self.edges

    def neighbours(self, v):
        """
        Return a list of neighbours of v.
        A vertex u appears in this list as many
        times as the (v,u) edge is in the graph.

        If v is not in the graph, then
        raise a ValueError exception.

        Efficiency: O(# edges)

        >>> Edges = [(1,2),(1,4),(3,1),(3,4),(2,4),(1,2)]
        >>> g = Graph({1,2,3,4}, Edges)
        >>> g.neighbours(1)
        [2, 4, 2]
        >>> g.neighbours(4)
        []
        >>> g.neighbours(3)
        [1, 4]
        >>> g.neighbours(2)
        [4]
        """

        """ OLD NEIGHBOURS
        if not self.is_vertex(v):
            raise ValueError("Vertex not in graph")

        return [e[1] for e in self.edges if e[0] == v]
        """
        #print("asking for node...", v)
        return self.neighbour[v]
