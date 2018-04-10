class MetaBush:
    def __init__(self,map_array, width, height):

        self.nodes = set()
        # translate maps tuple pairs to actual node objects
        self.translate = dict()
        # Connections is a list of all edges in the graph
        self.connect = []
        self.start = None
        self.end = None

        # dictionary for color conversion
        self.convert = {0:"RED",1:"ORANGE",2:'PINK',3:'WHITE',4:'YELLOW',5:'GREEN',6:'TEAL',7:'BLUE'}

        # color based dictionary storage of nodes
        self.grasses = []
        self.doors = {"RED":[],"ORANGE":[],'PINK':[],'WHITE':[],'YELLOW':[],'GREEN':[],'TEAL':[],'BLUE':[]}
        self.switchs = {"RED":[],"ORANGE":[],'PINK':[],'WHITE':[],'YELLOW':[],'GREEN':[],'TEAL':[],'BLUE':[]}
        self.buttons = {"RED":[],"ORANGE":[],'PINK':[],'WHITE':[],'YELLOW':[],'GREEN':[],'TEAL':[],'BLUE':[]}

        #where the magic happens...
        self.mapToMetaBush(map_array, width, height)

    def mapToMetaBush(self, map_array, width, height):
        """
        take in an int array repressenting the two maps as well as their individual
        heights and widths. map_array should be extracted from reader.py
        """

        def grassFlood(x,y,node):
            """
            recursive floodfill for grasstiles (and start and end tiles)
            """
            node.contained_coords.append((x,y))
            if map_array[x][y] == 7:
                self.start = node.coord
            if map_array[x][y] == 6:
                self.end = node.coord
            map_array[x][y] += 1000
            surround = [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]
            for pair in surround:
                if (pair[0] < 0) or (pair[1] < 0) or (pair[0] >= width) or (pair[1] >= height):
                    continue
                if map_array[pair[0]][pair[1]] in {0,6,7}:
                    grassFlood(pair[0],pair[1],node)


        #Grass run O(n + m), m is # of grass tiles flood fill
        for i in range(width):
            for j in range(height):
                # for all values, if grass, floodfill to construct grass node
                if map_array[i][j] in {0,6,7}:
                    new_grass = Grass(i,j)
                    self.nodes.add((i,j))
                    self.grasses.append(new_grass)
                    self.translate[(i,j)] = new_grass
                    grassFlood(i,j,new_grass)

        # Map run O(n)
        #0grass -- 1wall -- 3switch -- 4door -- 5Pp -- 6end -- 7 Player start
        for i in range(width):
            for j in range(height):
                val = map_array[i][j]
                type = (val % 10)
                if type == 3:
                    new = Switch(i,j,self.convert[(val - type)//10])
                    self.nodes.add((i,j))
                    self.switchs[self.convert[(val - type)//10]].append((i,j))
                    self.translate[(i,j)] = new
                if type == 4:
                    new = Door(i,j,self.convert[((val - type)//10) % 10],val > 100)
                    self.nodes.add((i,j))
                    self.doors[self.convert[((val - type)//10) % 10]].append((i,j))
                    self.translate[(i,j)] = new
                if type == 5:
                    new = Button(i,j,self.convert[(val - type)//10])
                    self.nodes.add((i,j))
                    self.buttons[self.convert[(val - type)//10]].append((i,j))
                    self.translate[(i,j)] = new

        #Connections run O(n)
        for i in range(width):
            for j in range(height):
                # for all tiles
                val = map_array[i][j]
                type = (val % 10)
                if (type in {0,1,6,7}):
                    # if grass, door, or start , or finish skip
                    continue
                surround = [(i+1,j),(i,j+1),(i-1,j),(i,j-1)]
                for pair in surround:
                    if (pair[0] < 0) or (pair[1] < 0) or (pair[0] >= width) or (pair[1] >= height):
                        continue
                    # for all valid neighbours of current tile create an edge
                    if map_array[pair[0]][pair[1]] % 10 in {0,6,7}:
                        for item in self.grasses:
                            if (pair[0],pair[1]) in item.contained_coords:
                                self.connect.append(((i,j),item.coord))
                                self.connect.append((item.coord,(i,j)))
                                self.translate[item.coord].connect.append((i,j))
                                self.translate[(i,j)].connect.append(item.coord)
                                break
                    elif map_array[pair[0]][pair[1]] % 10 in {3,4,5}:
                        self.connect.append(((i,j),(pair[0],pair[1])))
                        self.translate[(i,j)].connect.append((pair[0],pair[1]))

#node definitions
class Node:
    def __init__(self,X,Y,node_type):
        self.connect = list() # Sub nodes
        self.coord = (X,Y)
        self.node_type = node_type

class Grass(Node):
    def __init__(self,X,Y,grass_type = "grass"):
        super().__init__(X,Y,grass_type)
        self.contained_coords = []
        self.color = None

class Door(Node):
    def __init__(self,X,Y,color,inverse):
        super().__init__(X,Y,"door")
        self.color = color
        self.inverse = inverse

class Switch(Node):
    def __init__(self,X,Y,color):
        super().__init__(X,Y, "switch")
        self.color = color

class Button(Node):
    def __init__(self,X,Y,color):
        super().__init__(X,Y, "button")
        self.color = color
