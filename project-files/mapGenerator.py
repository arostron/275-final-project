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

def createMapFile(w=16,h=12):
    """
    randomly generates a map.h file, returns the name of the file (mapXXXX.h)
    """
    #VALID TILES ARE...
    #3,4,5 endings
    # 6,7 start
    #100 on 4s
    # 3,4,5,7,6,2,0,1 ten's

    valid_tiles = ['0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '03','13','23','33',\
    '43','53','63','73','04','14','24','34','44','54','64','74','104','114',\
    '124','134','144','154','164','174']

    selected_tiles = []
    #randomly select tiles
    for i in range(w*h*2):
        selected_tiles.append(valid_tiles[randint(0,len(valid_tiles)-1)])

    #generate start and end points
    start_spot = randint(0,len(valid_tiles)-1)
    end_spot = randint(0,len(valid_tiles)-1)
    while start_spot == end_spot:
        start_spot = randint(0,len(valid_tiles)-1)
        end_spot = randint(0,len(valid_tiles)-1)

    # start and end are not the same, add to selected tiles
    selected_tiles[start_spot] = '6'
    selected_tiles[end_spot] = '7'

    #map finished, substitute in numbers then replace '()' for c++
    mapString = bracketTemplate.format(*selected_tiles)
    mapString = mapString.replace('(', '{')
    mapString = mapString.replace(')', '}')

    title = "Map{}.h".format(randint(1111,9999))
    with open(title,'w') as file:
        file.write(mapString)
        print("Created file:", title)

    return title