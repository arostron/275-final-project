class MetaBush:
    def __init__(self,map_array, width, height):
        # A dictionary of nodes with the tuple names as keys
        print("---------------")
        self.nodes = []
        # A dictionary connect
        self.connect = []
        #
        self.start = None

        self.convert = {0:"RED",1:"ORANGE",2:'PINK',3:'WHITE',4:'YELLOW',5:'GREEN',6:'TEAL',7:'BLUE'}

        self.grasses = []
        self.doors = {"RED":[],"ORANGE":[],'PINK':[],'WHITE':[],'YELLOW':[],'GREEN':[],'TEAL':[],'BLUE':[]}
        self.switchs = {"RED":[],"ORANGE":[],'PINK':[],'WHITE':[],'YELLOW':[],'GREEN':[],'TEAL':[],'BLUE':[]}
        self.buttons = {"RED":[],"ORANGE":[],'PINK':[],'WHITE':[],'YELLOW':[],'GREEN':[],'TEAL':[],'BLUE':[]}
        self.state = {"RED":False,"ORANGE":False,'PINK':False,'WHITE':False,'YELLOW':False,'GREEN':False,'TEAL':False,'BLUE':False}

        self.mapToMetaBush(map_array, width, height)

    def mapToMetaBush(self,map_array, width, height):
        '''
        DESCRIPTION
        This function converts a given map into a MetaBush.

        ARGUMENTS
        The Map consists of an array of row arrays.
        '''
        # TODO implement the fill sorting algorithem
        '''
        Flood-fill (node, target-color, replacement-color):
        If target-color is equal to replacement-color, return.
        If the color of node is not equal to target-color, return.
        Set the color of node to replacement-color.
        Perform Flood-fill (one step to the south of node, target-color, replacement-color).
        Perform Flood-fill (one step to the north of node, target-color, replacement-color).
        Perform Flood-fill (one step to the west of node, target-color, replacement-color).
        Perform Flood-fill (one step to the east of node, target-color, replacement-color).
        '''
        def flood(x,y,pastnode):
            value = map_array[x][y]
            point_type = value % 10
            if value >= 1000:
                #if here an if component.... (not grass)
                if point_type != 0:
                    print("Connection?")
                    self.connect.append((pastnode.coord,(x,y)))
                return

            map_array[x][y] += 1000
            color = self.convert[(((value - point_type)//10)%10)]
            inverse = value >= 100

            self.nodes.append((x,y))
            self.connect.append((pastnode.coord,(x,y)))

            #0grass -- 1wall -- 3switch -- 4door -- 5Pp -- 6end -- 7 Player start
            if point_type == 0 and not isinstance(pastnode, Grass):
                # grass
                #print("process grass")
                new_node = Grass(x,y)
                self.grasses.append((x,y))
                pastnode.children.append(new_node)
                pastnode = new_node
            elif point_type == 4:
                # Door
                #print("process door")
                new_node = Door(x,y,color,inverse)
                self.doors[color].append((x,y))
                pastnode.children.append(new_node)
                pastnode = new_node
            elif point_type == 3:
                # swith
                #print("process switch")
                new_node = Switch(x,y,color)
                self.switchs[color].append((x,y))
                pastnode.children.append(new_node)
                pastnode = new_node
            elif point_type == 5:
                # Button
                #print("process button")
                new_node = Button(x,y,color)
                self.buttons[color].append((x,y))
                pastnode.children.append(new_node)
                pastnode = new_node
            elif point_type == 6:
                #print("process end")
                new_node = Grass(x,y,"end")
                pastnode.children.append(new_node)
                pastnode = new_node

            # list of 4 destinations //
            # if the destination is invalid remove it (filed or bounds or wall)
            # if element is a component move to the back of the list
            # if its grass do the recursion call

            for element in order_destination(x,y):
                flood(element[0], element[1], pastnode)


        def order_destination(x,y):
            """
            look at all adjacent tiles and order them in order of proper recursion call

            returns a list of co-ordinates of appropreate calls
            """
            adj = []
            adj.append((x+1,y))
            adj.append((x,y+1))
            adj.append((x-1,y))
            adj.append((x,y-1))

            order = []

            for point in adj: # types each point
                i, j = point[0], point[1]
                if (i < 0) or (i >= width) or (j < 0) or (j >= height):
                    # Out of bounds, dont add to order
                    continue
                value = map_array[i][j]
                if (value >= 1000):
                    #print("cats")
                    continue
                if (value == 1) or (value == 7):
                    continue

                point_type = value % 10
                if point_type == 0:
                    # point is grass
                    order.insert(0, point)
                else:
                    order.append(point)
            return order

            """flood(x+1,y,pastnode)
            flood(x,y+1,pastnode)
            flood(x,y-1,pastnode)
            flood(x-1,y,pastnode)"""


        #   during translation find the start and end points and flag them

        for i in range(width):
            for j in range(height):
                if map_array[i][j] == 7:
                    self.start = Grass(i,j,"start")
                    stuff = order_destination(i,j)
                    for element in stuff:
                        flood(element[0], element[1], self.start)
                    return


class Node:
    def __init__(self,X,Y,node_type):
        self.children = list() # Sub nodes
        self.coord = (X,Y)
        self.node_type = node_type

class Grass(Node):
    def __init__(self,X,Y,grass_type = "grass"):
        super().__init__(X,Y,grass_type)

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
