from classDef import *
from mainFrame import *
from queue import deque as Q


def checkMazes(g1, g2):
    """
    This function takes in two 'MetaBush' graphs, and checks if it is possible
    for players to escape the maze.

    a cloud of the gamestates is created then traversed.
    a games state graph or cloud, consists of nodes which repersent every possible
    game state
    Node example: (x1,y1,x2,y2,[state variables])
    """
    # TODO...

    """
    PSEUDO FOR SUPER CLOUD
    consider node a (from g1) and node b (from g2)

        add starting nodes (include every possible starting state variables)

        move off of a to every possible
            find all possible destinations
            calculate the resulting state variables
            add the destination node
            add the edge between the existing nodes

        move off of a to every possible
            find all possible destinations
            calculate the resulting state variables
            add the destination node
            add the edge between the existing nodes
    """

    """
    while (queu not empty):
        pop the queue
        #break the if you find the end
        skip if node already in nodes
        find all the valid nodes #HOW WE DO THIS EH
        add edges between valid destinations # MIGHT NOT NEED THIS
        add the destinations to the queue
    """
    q = Q()

    
