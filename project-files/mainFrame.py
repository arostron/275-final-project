import classDef
import reader
import graph
import visualize


def setup(filename="Map.h"):
	map1, map2, w, h = reader.getRawMap(filename)
	busha = classDef.MetaBush(map1, w, h)
	bushb = classDef.MetaBush(map2, w, h)
	return busha, bushb

def produceVisableGraph(tree):
	"""
	Extracts the nodes and edges from a given tree then returns the graph
	"""
	nodes = set()
	edges = list()

	def crawl(current):
		nodes.add(current.node_type +" @ " + str(current.coord))
		for kid in current.children:
			edges.append((current.node_type +" @ " + str(current.coord), kid.node_type +" @ " + str(kid.coord)))
			crawl(kid)

	crawl(tree.start)
	return graph.Graph(nodes, edges)


def renderGraph(g):
	"""
	Bring up a PDF of the given graph g
	"""
	visualize.get_dot_format(g).render(view=True)


if __name__ == '__main__':
	tree1, tree2 = setup()

	# the old way of redering graphs
	"""
	tree1.nodes.append((7,0)) # manually adding in the start node
	graph_for_viz = graph.Graph(set(tree1.nodes), tree1.connect)
	# render the graph.....
	renderGraph(graph_for_viz)
	"""

	# a new way of rendering graphs...?

	renderGraph(produceVisableGraph(tree1))
