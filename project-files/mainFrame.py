import classDef
import reader
import graph
import visualize
import solver
import time
import mapGenerator


def setup(filename="Map.h"):
	"""
	performs the extraction of the specified mapfile and creates two meta bush
	objects representing each room in the maze.
	"""
	map1, map2, w, h = reader.getRawMap(filename)
	busha = classDef.MetaBush(map1, w, h)
	bushb = classDef.MetaBush(map2, w, h)
	return busha, bushb

def renderGraph(g):
	"""
	Uses vizualize.py to render a graphical representation of the nodes and
	connections in a given graph g. g mush be an instance of the Graph class
	"""

	visualize.get_dot_format(g).render(view=True)

def main():
	"""
	Command line interface for user to interact with solver.py and MetaBush objects
	"""
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
			# if a random map was just created 'random' will access it
			g1, g2 = setup(random_name)
		else:
			g1, g2 = setup(map_file)

		# MetaBush's established from mazes corresponding to input

		# run the solver, wait for user to give the green light
		_ = input("About to run (quick) solver.py, press enter to continue")
		print()
		start = time.clock()
		print("Maps solveable?:", solver.checkMazes(g1, g2))
		print("Time Elapsed:", time.clock()-start)
		print()

		y_n = input("visualize player 1's map? (y/n): ")
		if y_n == 'y':
			# create a graph class from the meta bush objects
			graph_for_viz = graph.Graph(set(g1.nodes), g1.connect)
			# render the graph.....
			renderGraph(graph_for_viz)

		y_n = input("visualize player 2's map? (y/n): ")
		if y_n == 'y':
			# create a graph class from the meta bush objects
			graph_for_viz = graph.Graph(set(g2.nodes), g2.connect)
			# render the graph.....
			renderGraph(graph_for_viz)

		y_n = input("Again? (y/n): ")
		if y_n != 'y':
			return


if __name__ == '__main__':
	main()
