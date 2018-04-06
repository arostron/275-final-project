from classDef import *

def getRawMap(filename="Map.h"):
    """
    DESCRIPTION
    This function acceses the cpp header file the arduino uses to load the map
    then returns the array parsed from that file

    ARGUMENTS
    filename = target filename, default Map.h

    ASSUMPTIONS
    target file follows the specific format:
    1) the first 3 lines are irrelevent
    2) the 4th line contains 4 numbers, the last two are the height and width of
    the map
    3) the file only contains relavant data up to a blank line
    4) lines between the first relevenat line and first blank line contain
    a list of comma separated numbers, the program removes non numerical
    characters padding this list separating the comma separated values
    """
    with open(filename,'r') as file:


        file.readline()
        file.readline()
        file.readline()
        #chop of first 3 lines
        first_line = file.readline()

        # REALLY BAD STRIPPING OF NUMBERE COULD BE OPTIMIZED

        while not first_line[-1].isnumeric(): # clear off right till number
            first_line = first_line[:-1]

        while not first_line[0].isnumeric(): #
            first_line = first_line[1:]
        first_line = first_line[1:]
        while not first_line[0].isnumeric(): #
            first_line = first_line[1:]
        first_line = first_line[1:]
        while not first_line[0].isnumeric(): #
            first_line = first_line[1:]
        first_line = first_line[1:]
        while not first_line[0].isnumeric(): # clear off first 3 left numbers
            first_line = first_line[1:]

        width = int(first_line[:2])
        height = int(first_line[-2:])
        #print("w:{}, h:{}".format(width,height))

        # width and height parsed

        parsed_map_line = []
        map_array1 = []
        map_array2 = []
        for i in range(width):
            map_array1.append([])
            map_array2.append([])

        for i in range(2 * width):
            line = file.readline()
            if line is "\n": break # read every line in the file until empty line reached
            line = line[1:-1] # cut off first bracket
            while not line[-1].isnumeric(): # clear off right till number
                line = line[:-1]
            parsed_map_line = line.split(',') # one line of char list of numbers in array
            if i < width:
                for j in range(height):
                    map_array1[i].append(int(parsed_map_line[j]))
            else:
                for j in range(height):
                    map_array2[i - width].append(int(parsed_map_line[j]))

        # int arrays of maps parsed now

        return map_array1, map_array2, width, height


if __name__ == '__main__':
    print("Getting array:")
    map_array1, map_array2, width, height = getRawMap()
    print("Width:",width)
    print("Height",height)
    print("Array 1:")
    for i in range(height):
        print(map_array1[i])
    print("Array 2:")
    for i in range(height):
        print(map_array2[i])

    main = MetaBush(map_array1,width,height)
    print("Main nodes: ")
    print(main.nodes)
    print(main.start)
