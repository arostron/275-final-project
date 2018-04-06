from graph import Graph
import sys

try:
  import graphviz
except:
  print()
  print("*"*40)
  print("Error importing graphviz.")
  print("To install it on the VM, type:")
  print("      sudo pip3 install graphviz")
  print("and enter cmput274 as the password.")
  print()
  print("To install in Google Colaboratory, execute a block with these two commands:")
  print("      !apt-get -qq install -y graphviz")
  print("      !pip install graphviz")
  print("*"*40)
  print()
  sys.exit(0)

def get_dot_format(graph):
  """
  Converts an instance of our Graph class to an instance
  of the graphviz class Digraph, which can then be displayed in a block via

  graphviz.Source(return_value)

  Assumes each vertex of g can be converted to a string via str().
  """

  dot = graphviz.Digraph()

  dot.attr('node', shape='circle')

  for u in graph.vertices:
    dot.node(str(u))
    for v in graph.neighbours(u):
      dot.edge(str(u), str(v))

  return dot

if __name__ == "__main__":
    # runs a simple test, try your own!
    my_graph = Graph({1, 2, 3, 4, 5})
    my_graph.add_edge((3, 4))
    my_graph.add_edge((2, 4))
    my_graph.add_edge((4, 2))
    my_graph.add_edge((3, 1))

    print(my_graph.neighbours(3))


    dot = get_dot_format(my_graph)

    # saves two files for the graph image in the working directory
    dot.render(view=True)

    # this won't work on Google Colaboratory, there you should use
    # graphviz.source(dot)
