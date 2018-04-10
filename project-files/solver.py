from classDef import *
from mainFrame import *
from queue import deque as Q
import bit
from random import randint
from graph import Graph
import breadth_first_search


def checkMazes(g1, g2):
    """
    This function takes in two 'MetaBush' graphs, and checks if it is possible
    for players to escape the maze.

    a cloud of the gameStates is created then traversed.
    a games State graph or cloud, consists of nodes which repersent every possible
    game State
    Node example: (x1,y1,x2,y2,[State variables])
    """

    color_code = {"RED":0,"ORANGE":1,'PINK':2,'WHITE':3,'YELLOW':4,'GREEN':5,'TEAL':6,'BLUE':7}
    q = Q()
    empty_q = Q()
    nodes = set()
    # add the start node to the q along with staring conditions
    q.append((g1.start, g2.start, 0))

    while q != empty_q:
        #pop the queue
        curr = q.popleft()
        A, B, State = curr[0], curr[1], curr[2]
        #break the if you find the end
        if A == g1.end and B == g2.end:
            return True

        #skip if node already in nodes
        if curr in nodes:
            continue

        nodes.add(curr)

        #find all the valid nodes
        # find the class representations of the current nodes
        Anode, Bnode = g1.translate[A], g2.translate[B]
        # get the connections list from each node
        connect1, connect2 = Anode.connect, Bnode.connect
        #for each connection tuple in connection list
        for des in connect1:
            #get the node of the destination
            des_node = g1.translate[des]

            # if the destination door is closed skip the destination
            if isinstance(des_node,Door):
                if (not bit.testBit(State,color_code[des_node.color]) and not des_node.inverse)\
                or (bit.testBit(State,color_code[des_node.color]) and des_node.inverse):
                    #regular door is closed 0, or inverse door and 1
                    continue

            if isinstance(Anode,Button): # if start is a button
                if isinstance(des_node,Door): # and the destination is a door
                    if Anode.color == des_node.color:
                        continue
                if isinstance(B,Door):
                    if g2.translate[B].color == des_node.color:
                        #player killed
                        continue
                State = bit.toggleBit(State,color_code[Anode.color]) # toggle getting off button


            # need to calculate State as a result of getting onto something
            if isinstance(des_node,Button) or isinstance(des_node,Switch):
                State = bit.toggleBit(State,color_code[des_node.color])
                if isinstance(B,Door):
                    if g2.translate[B].color == des_node.color:
                        #player killed
                        continue
            q.append((des, B, State))

        # moving off of B
        for des in connect2:
            des_node = g2.translate[des]
            if isinstance(Bnode,Button):
                if isinstance(des_node,Door):
                    if Bnode.color == des_node.color:
                        continue
                if isinstance(A,Door):
                    if g1.translate[A].color == des_node.color:
                        #player killed
                        continue
                State = bit.toggleBit(State,color_code[Bnode.color])
            if isinstance(des_node,Door):
                if (not bit.testBit(State,color_code[des_node.color]) and not des_node.inverse)\
                or (bit.testBit(State,color_code[des_node.color]) and des_node.inverse):
                    #regular door is closed, or inverse door and 1
                    continue

            # need to calculate State beforehand
            if isinstance(des_node,Button) or isinstance(des_node,Switch):
                State = bit.toggleBit(State,color_code[des_node.color])
                # is the player dead?
                # if the other player is standing on a closed door then skip
                if isinstance(A,Door):
                    if g1.translate[A].color == des_node.color:
                        #player killed
                        continue
            q.append((A, des, State))

    #endpoint hasnt been found and all possibilities have been processed
    return False

def slowCheckMazes(g1, g2):
    """
    Slow check mazes takes in two 'MetaBush' representations of two maze rooms
    and returns if it is possible for both players to escape the mazeself.

    To compute this slowCheckMazes creates a graph of every possible game State
    O(#nodes in g1 * #nodes in g1 * 2^state variables)
    The graph is also populated by valid transitions between nodes. Once the
    'cloud' graph has been computed with all possible moves, a Modified
    breadth_first_search is called to see if there exists a path of valid
    movements between start and end nodes.

    Solver does not work on trivial mazes

    PSEUDO FOR SUPER CLOUD
    consider node a (from g1) and node b (from g2)

        add starting nodes (include every possible starting State variables)

        move off of a to every possible
            find all possible destinations
            calculate the resulting State variables
            add the destination node
            add the edge between the existing nodes

        move off of a to every possible
            find all possible destinations
            calculate the resulting State variables
            add the destination node
            add the edge between the existing nodes
    """
    cloud = Graph()
    nodes = set()
    edges = []

    color_code = {"RED":0,"ORANGE":1,'PINK':2,'WHITE':3,'YELLOW':4,'GREEN':5,'TEAL':6,'BLUE':7}

    print("starting slow solver graph generation\nThis could take a while...")
    for a in g1.nodes:
        for b in g2.nodes:
            # for all a and b, add each start point
            for State in range(2**8):
                # for each State variables possible
                cloud.add_vertex((a,b,State))
                OG_State = State
                #establish neighbours list in graph
                cloud.neighbour[(a,b,State)] = []

                #get a list of neighbouring nodes to pair nodes a and b
                connect1, connect2 = g1.translate[a].connect, g2.translate[b].connect

                #calculate all moves off of A
                for des in connect1:
                    #get the node of the destination
                    des_node = g1.translate[des]
                    # if the destination door is closed skip the destination
                    if des_node.node_type == "door":
                        if (not bit.testBit(State,color_code[des_node.color]) and not des_node.inverse)\
                        or (bit.testBit(State,color_code[des_node.color]) and des_node.inverse):
                            #regular door is closed 0, or inverse door and 1
                            continue

                    # if start is a button
                    if isinstance(a,Button):
                        if isinstance(des_node,Door): # and the destination is a door
                            if a.color == des_node.color:
                                continue
                        State = bit.toggleBit(State,color_code[a.color]) # toggle getting off button

                    # need to calculate State as a result of getting onto something
                    if isinstance(des_node,Button) or isinstance(des_node,Switch):
                        State = bit.toggleBit(State,color_code[des_node.color])
                        if isinstance(b,Door):
                            if g2.translate[b].color == des_node.color:
                                #player killed
                                continue

                    # add the destination node, the edge, and a neighbour to the graph
                    cloud.add_vertex((des, b, State))
                    cloud.add_edge(((a,b,OG_State),(des, b, State)))
                    cloud.neighbour[(a,b,OG_State)].append((des, b, State))

                #move off B (Same process as a but moving off of B)
                for des in connect2:
                    des_node = g2.translate[des]
                    if isinstance(b,Button):
                        if isinstance(des_node,Door):
                            if b.color == des_node.color:
                                continue
                        State = bit.toggleBit(State,color_code[b.color])
                    if isinstance(des_node,Door):
                        if (not bit.testBit(State,color_code[des_node.color]) and not des_node.inverse)\
                        or (bit.testBit(State,color_code[des_node.color]) and des_node.inverse):
                            #regular door is closed, or inverse door and 1
                            continue

                    # need to calculate State beforehand
                    if isinstance(des_node,Button) or isinstance(des_node,Switch):
                        State = bit.toggleBit(State,color_code[des_node.color])
                        if isinstance(a,Door):
                            if g1.translate[a].color == des_node.color:
                                #player killed
                                continue
                    cloud.add_vertex((a, des, State))
                    cloud.add_edge( ((a,b,OG_State),(a, des, State)) )
                    cloud.neighbour[(a,b,OG_State)].append( (a, des, State) )

    # cloud now created, run breadth_first_search
    #print("the number of nodes is:",len(cloud.vertices), "expected:", (len(g1.nodes) * len(g2.nodes) * 256))
    print("Cloud calculated. Running breadth_first_search")
    breadth_first_search.breadth_first_search(cloud, (g1.start,g2.start,0), g1.end, g2.end)
