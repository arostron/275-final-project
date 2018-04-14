from random import randint

bracketTemplate = \
"""#ifndef _Map_h
#define _Map_h

uint8_t map1[2][16][12] = ((
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{})),(
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{}),
({},{},{},{},{},{},{},{},{},{},{},{})));

#endif"""

def createMapFileRandom(w=16,h=12):
    """
    Randomly generates a map.h file, returns the name of the file (MapXXXX.h)
    This randomly generated maze file could be solveable or unsolvable.
    map naming is simply random, there is no see generation usedself.

    Map generation works by selecting a set of vaid tiles, then .formats
    those tile (integer values representing different tiles) into a default
    template for map files.
    """

    valid_tiles = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', \
     '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', \
     '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', \
     '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', \
     '03','13','23','33',\
     '05','15','25','35','45','55','65','75',\
    '43','53','63','73','04','14','24','34','44','54','64','74',\
    '104','114','124','134','144','154','164','174']


    selected_tiles = []
    #randomly select tiles
    for i in range(w*h*2):
        selected_tiles.append(valid_tiles[randint(0,len(valid_tiles)-1)])

    #randomly insert the start and enpoints for the graph
    selected_tiles[randint(0,((w*h)//2))] = '6'
    selected_tiles[randint(0+((w*h)//2),((w*h)//2)+((w*h)//2))] = '7'
    selected_tiles[randint(0+((w*h)//2)+((w*h)//2),((w*h)//2)+((w*h)//2)+((w*h)//2))] = '6'
    selected_tiles[randint(0+((w*h)//2)+((w*h)//2)+((w*h)//2),((w*h)//2)+((w*h)//2)+((w*h)//2)+((w*h)//2))] = '7'

    #map finished, substitute in numbers then replace '()' for c++
    mapString = bracketTemplate.format(*selected_tiles)
    mapString = mapString.replace('(', '{')
    mapString = mapString.replace(')', '}')

    # generate map file with random name and selected tiles
    title = "Map{}.h".format(randint(1111,9999))
    with open(title,'w') as file:
        file.write(mapString)
        print("Created file:", title)

    return title

if __name__ == '__main__':
    createMapFileRandom()
