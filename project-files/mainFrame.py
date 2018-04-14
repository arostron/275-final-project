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

		y_n = input("visualize player 1's map? (y/n): ")
		if y_n == 'y':
			graph_for_viz = graph.Graph(set(g1.nodes), g1.connect)
			# render the graph.....
			renderGraph(graph_for_viz)

		y_n = input("visualize player 2's map? (y/n): ")
		if y_n == 'y':
			graph_for_viz = graph.Graph(set(g2.nodes), g2.connect)
			# render the graph.....
			renderGraph(graph_for_viz)

		y_n = input("Again? (y/n): ")
		if y_n != 'y':
			return


if __name__ == '__main__':
	main()
