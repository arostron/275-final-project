from classDef import *
from mainFrame import *
from queue import deque as Q
import bit
from random import randint


def checkMazes(g1, g2):
    """
    This function takes in two 'MetaBush' graphs, and checks if it is possible
    for players to escape the maze.

    a cloud of the gameStates is created then traversed.
    a games State graph or cloud, consists of nodes which repersent every possible
    game State
    Node example: (x1,y1,x2,y2,[State variables])
    """
    # TODO...

    """
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
                    if Anode.color == des_node.color: # why not combine these?******** 
                        continue
                State = bit.toggleBit(State,color_code[Anode.color]) # toggle getting off button



            # need to calculate State as a result of getting onto something
            if isinstance(des_node,Button) or isinstance(des_node,Switch):
                State = bit.toggleBit(State,color_code[des_node.color])
            q.append((des, B, State))


        for des in connect2:
            des_node = g2.translate[des]
            if isinstance(Bnode,Button):
                if isinstance(des_node,Door):
                    if Bnode.color == des_node.color:
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
            q.append((A, des, State))
            #print("{}".format("qwertyuiopasdfghjklzxcvbnm1234567890"[randint(0,len("qwertyuiopasdfghjklzxcvbnm1234567890")-1)]))
        #add edges between valid destinations # MIGHT NOT NEED THIS???

    return False
