import classDef
import reader
import graph
import visualize
import solver
import time
import mapGenerator


def setup(filename="Map.h"):
	map1, map2, w, h = reader.getRawMap(filename)
	busha = classDef.MetaBush(map1, w, h)
	bushb = classDef.MetaBush(map2, w, h)
	return busha, bushb

def oldproduceVisableGraph(tree):
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
	current way to do it 
	y_n = input("visualize g1? (y/n): ")
	if y_n == 'y':
		graph_for_viz = graph.Graph(set(g1.nodes), g1.connect)
		# render the graph.....
		renderGraph(graph_for_viz)
	"""

	# the old way of redering graphs
	"""
	tree1.nodes.append((7,0)) # manually adding in the start node
	graph_for_viz = graph.Graph(set(tree1.nodes), tree1.connect)
	# render the graph.....
	renderGraph(graph_for_viz)
	"""

	visualize.get_dot_format(g).render(view=True)

def main():
	while True:
		print("--------------------")

		# possibly generate a random map file
		y_n = input("Create random map file? (y/n): ")
		if y_n == 'y':
			random_name = mapGenerator.createMapFileRandom()
			print("File also accesable as'random' in next prompt")

		#call setup on input filename
		map_file = input("Name of map file: ")
		if map_file == "":
			g1, g2 = setup()
		elif map_file == "random":
			g1, g2 = setup(random_name)
		else:
			g1, g2 = setup(map_file)

		# MetaBush's established

		# run the fast solver
		_ = input("About to run (quick) solver.py, press enter to continue")
		print()
		start = time.clock()
		print("Maps solveable?:", solver.checkMazes(g1, g2))
		print("Time Elapsed:", time.clock()-start)
		print()

		# prompt to run the slow solver
		y_n = input("Check solveable with slow algorithm? (y/n): ")
		if y_n == 'y':
			print()
			start = time.clock()
			solver.slowCheckMazes(g1, g2)
			print("Time Elapsed:", time.clock()-start)
			print()

		y_n = input("Again? (y/n): ")
		if y_n != 'y':
			return


if __name__ == '__main__':
	main()
