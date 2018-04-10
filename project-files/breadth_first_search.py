from graph import Graph
from collections import deque
import random, time

def breadth_first_search(graph, s, p1end, p2end):
  """
  Taken from 275 google drive and slightly modified
  Given a graph (an instance of Digraph) and a vertex s
  in the graph, and endpoints of the desired route, breadth_first_search Returns
  a boolean value representing if the path is present in the graph

  A dictionary "reached" whose keys are all vertices
  reachable from s and where reached[v] is the predecessor of v in the search.
  The exception is reached[s] == s.
  """

  reached = {s:s}
  todo = deque([s])

  while todo: # condition is true if and only if todo is not empty
    curr = todo.popleft()

    for nbr in graph.neighbours(curr):
      if nbr not in reached:
        reached[nbr] = curr

        # if one of the neighbours contains both players on the end tiles
        if nbr[0] == p1end and nbr[1] == p2end:
            print("True")
            return True
        todo.append(nbr)

  print("False")
  return False



def get_path(reached, start, end):
  """
  Return a path from start to end, given a search tree.

  reached:
    A dictionary representing a search tree of a search
    initiated from the vertex "start".
  start:
    The vertex that was the start of the search that constructed
    the search tree
  end:
    The desired endpoint of the search

  Returns a list of vertices starting at vertex start and ending at vertex end
  representing a path between these vertices (the path in the search tree).
  If the vertex "end" was not reached (i.e. is not a key in reached),
  this simply returns the empty list []

  # the example in the docstring test is the search tree run on the graph
  # drawn using graphviz above, starting from vertex 3

  >>> reached = {3:3, 1:3, 4:3, 2:4}
  >>> get_path(reached, 3, 2)
  [3, 4, 2]
  >>> get_path(reached, 3, 3)
  [3]
  >>> get_path(reached, 3, 5)
  []
  """

  if end not in reached:
    return []

  path = [end]

  while end != start:
    end = reached[end]
    path.append(end)

  path.reverse()

  return path


def test_random_graph(num_vertices):
  """
  Constructs a random graph with the given number of vertices where
  each vertex has 10 random outgoing edges.

  Then it runs the search and reports the time taken by the search.
  """
  print("Constructing random graph with", num_vertices, "vertices")
  print("and", 10*num_vertices, "edges.")

  vertices = set(range(num_vertices))

  edges = []
  for v in vertices:
    # for each vertex, create 10 random outgoing edges, we are not concerned
    # about duplicate edges or loops
    edges += [(v, random.randrange(num_vertices)) for x in range(10)]

    random_graph = Graph(vertices, edges)

  print("Starting search...")
  start = time.time()
  reached = breadth_first_search(random_graph, 0)
  end = time.time()
  print("Done!\nElapsed time in seconds:", end-start)
  print("Number of vertices reached:", len(reached))


if __name__ == "__main__":
  import doctest
  doctest.testmod()
