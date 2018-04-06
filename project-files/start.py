import reader
import classDef


def setup(filename="Map.h"):
	map1, map2, w, h = reader.getRawMap(filename)
	busha = classDef.MetaBush(map1, w, h)
	bushb = classDef.MetaBush(map2, w, h)
	return busha, bushb
