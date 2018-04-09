class MetaBush:
    def __init__(self,map_array, width, height):
        # A dictionary of nodes with the tuple names as keys
        print("---------------")
        self.nodes = set()
        self.translate = dict()
        # A dictionary connect
        self.connect = []
        #
        self.start = None

        self.convert = {0:"RED",1:"ORANGE",2:'PINK',3:'WHITE',4:'YELLOW',5:'GREEN',6:'TEAL',7:'BLUE'}

        self.grasses = [] #elements of this dictionary
        self.doors = {"RED":[],"ORANGE":[],'PINK':[],'WHITE':[],'YELLOW':[],'GREEN':[],'TEAL':[],'BLUE':[]}
        self.switchs = {"RED":[],"ORANGE":[],'PINK':[],'WHITE':[],'YELLOW':[],'GREEN':[],'TEAL':[],'BLUE':[]}
        self.buttons = {"RED":[],"ORANGE":[],'PINK':[],'WHITE':[],'YELLOW':[],'GREEN':[],'TEAL':[],'BLUE':[]}
        self.state = {"RED":False,"ORANGE":False,'PINK':False,'WHITE':False,'YELLOW':False,'GREEN':False,'TEAL':False,'BLUE':False}

        #print(map_array)
        self.mapToMetaBush(map_array, width, height)

    def mapToMetaBush(self, map_array, width, height):

        def grassFlood(x,y,node):
            node.contained_coords.append((x,y))
            if map_array[x][y] == 7:
                self.start = node.coord
            map_array[x][y] += 1000
            surround = [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]
            for pair in surround:
                if (pair[0] < 0) or (pair[1] < 0) or (pair[0] >= width) or (pair[1] >= height):
                    continue
                if map_array[pair[0]][pair[1]] in {0,6,7}:
                    grassFlood(pair[0],pair[1],node)


        #Grass run
        for i in range(width):
            for j in range(height):
                if map_array[i][j] in {0,6,7}:
                    new_grass = Grass(i,j)
                    self.nodes.add((i,j))
                    self.grasses.append(new_grass)
                    grassFlood(i,j,new_grass)

        # Map run
        #0grass -- 1wall -- 3switch -- 4door -- 5Pp -- 6end -- 7 Player start
        for i in range(width):
            for j in range(height):
                val = map_array[i][j]
                type = (val % 10)
                if type == 3:
                    new = Switch(i,j,self.convert[(val - type)//10])
                    self.nodes.add((i,j))
                    self.translate[(i,j)] = new
                if type == 4:
                    new = Door(i,j,self.convert[((val - type)//10) % 10],val > 100)
                    self.nodes.add((i,j))
                    self.translate[(i,j)] = new
                if type == 5:
                    new = Button(i,j,self.convert[(val - type)//10])
                    self.nodes.add((i,j))
                    self.translate[(i,j)] = new

        #Connections run
        for i in range(width):
            for j in range(height):
                val = map_array[i][j]
                type = (val % 10)
                if (type in {0,1,6,7}):
                    continue
                surround = [(i+1,j),(i,j+1),(i-1,j),(i,j-1)]
                for pair in surround:
                    if (pair[0] < 0) or (pair[1] < 0) or (pair[0] >= width) or (pair[1] >= height):
                        continue
                    if map_array[pair[0]][pair[1]] % 10 in {0,6,7}:
                        for item in self.grasses:
                            if (pair[0],pair[1]) in item.contained_coords:
                                self.connect.append(((i,j),item.coord))
                                self.connect.append((item.coord,(i,j)))
                                break
                    elif map_array[pair[0]][pair[1]] % 10 in {3,4,5}:
                        self.connect.append(((i,j),(pair[0],pair[1])))


        pass

class Node:
    def __init__(self,X,Y,node_type):
        self.children = list() # Sub nodes
        self.coord = (X,Y)
        self.node_type = node_type

class Grass(Node):
    def __init__(self,X,Y,grass_type = "grass"):
        super().__init__(X,Y,grass_type)
        self.contained_coords = []

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
