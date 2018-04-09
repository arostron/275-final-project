import classDef
import reader
import graph
import visualize
import solver


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
		# add a node
		if hasattr(current, "color"):
			nodes.add(current.node_type + " " + current.color +" @\n" + str(current.coord))
		else:
			nodes.add(current.node_type +" @ " + str(current.coord))

		# for all kids add an edge to the kid
		for kid in current.children:
			if not (hasattr(current, "color") or hasattr(kid, "color")):
				#neither node has a color, add it as such
				edges.append((\
				current.node_type +" @ " + str(current.coord), \
				kid.node_type +" @ " + str(kid.coord) \
				))
			elif hasattr(current, "color") and hasattr(kid, "color"):
				# both have color
				edges.append((\
				current.node_type + " " + current.color +" @\n" + str(current.coord), \
				kid.node_type + " " + kid.color +" @\n" + str(kid.coord) \
				))

			elif hasattr(current, "color"):
				# only parent has color
				edges.append((\
				current.node_type + " " + current.color +" @\n" + str(current.coord), \
				kid.node_type +" @ " + str(kid.coord) \
				))
			else:
				# only kid has color
				edges.append((\
				current.node_type +" @ " + str(current.coord), \
				kid.node_type + " " + kid.color +" @\n" + str(kid.coord) \
				))
			#crawl to all children
			crawl(kid)

	crawl(tree.start)
	return graph.Graph(nodes, edges)

def renderGraph(g):
	"""
	Bring up a PDF of the given graph g
	"""

	# the old way of redering graphs
	"""
	tree1.nodes.append((7,0)) # manually adding in the start node
	graph_for_viz = graph.Graph(set(tree1.nodes), tree1.connect)
	# render the graph.....
	renderGraph(graph_for_viz)
	"""

	visualize.get_dot_format(g).render(view=True)

def runSolver(filename = "Map.h"):
	tree1, tree2 = setup(filename)
	print(solver.checkMazes(tree1,tree2))



if __name__ == '__main__':
	#runSolver(input("Name of map file"))
	g1, g2 = setup("Test.h")
	print(solver.checkMazes(g1, g2))
	solver.slowCheckMazes(g1, g2)
	"""
	graph_for_viz = graph.Graph(set(tree1.nodes), tree1.connect)
	# render the graph.....
	renderGraph(graph_for_viz)
	"""
