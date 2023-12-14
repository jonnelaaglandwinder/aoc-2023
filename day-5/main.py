import re, sys
from dataclasses import dataclass
from typing import Union, Iterable
from functools import reduce

def intersection(a: Union[range, slice], b: Union[range, slice]):
    if type(a) != range and type(a) != slice:
        raise Exception("a is not a range or slice", a)
    if type(b) != range and type(b) != slice:
        raise Exception("b is not a range or slice", b)
        
    rng = range(max(a.start, b.start), min(a.stop, b.stop))

    return rng if rng.start < rng.stop else None

@dataclass
class Mapping:
    source_range: range
    destination_range: range
    
    def __contains__(self, key: int):
        return key in self.source_range

    def __getitem__(self, key: Union[int, slice, range, tuple]):
        if type(key) == int:
            if key in self.source_range:
                return key - self.source_range.start + self.destination_range.start

            return None
    
        if type(key) == slice or type(key) == range:
            rng = intersection(self.source_range, key)

            if rng:
                return range(rng.start - self.source_range.start + self.destination_range.start, rng.stop - self.source_range.start + self.destination_range.start)
            
            return None
        
        if type(key) == tuple:
            return tuple(map(self.__getitem__, key))

    def __len__(self):
        return len(self.source_range)

    def intersects(self, rng: Union[range, slice]):
        return intersection(self.source_range, rng) is not None

    def slice_by_source(self, rng: Union[range, slice]):
        source_range = intersection(self.source_range, rng)

        return Mapping(source_range, self[source_range]) if source_range else None

    def parse(s: str):
        destination_start, source_start, length = map(int, s.split(" "))

        return Mapping(range(source_start, source_start + length + 1), range(destination_start, destination_start + length + 1))

@dataclass
class Map:
    entries: list[Mapping]

    def __getitem__(self, key: Union[int, slice, range, tuple, Mapping, list]):
        if type(key) == int:
            return self.map_key(key)
        
        if type(key) == slice or type(key) == range:
            return self.get_mappings(key)
        
        if type(key) == tuple:
            return tuple(map(self.__getitem__, key))

        if isinstance(key, Mapping):
            return self.get_mappings(key.destination_range)

        try:
            it = iter(key)

            def flatten(x):
                if isinstance(x, Iterable) and not isinstance(x, str):
                    return [a for i in x for a in flatten(i)]
                else:
                    return [x]
                
            return flatten([self.__getitem__(k) for k in it])
        except TypeError:
            raise Exception("Invalid key", key)
        

    def get_mapping(self, key: int):
        for entry in self.entries:
            if key in entry:
                return entry
        
        return None

    def get_source_range(self, key: int):
        mapping = self.get_mapping(key)

        return mapping.source_range if mapping else None
                
    def get_destination_range(self, key: int):
        mapping = self.get_mapping(key)

        return mapping.destination_range if mapping else None

    def get_mappings(self, rng: Union[range, slice]):
        mappings = [x for x in [entry.slice_by_source(rng) for entry in self.entries] if x]

        gaps = list(find_gaps([m.source_range for m in mappings], rng))
        gap_mappings = [Mapping(rng, rng) for rng in gaps]

        return sorted(mappings + gap_mappings, key=lambda m: m.source_range.start)
    
    def map_key(self, key: int):
        mapping = self.get_mapping(key)

        return mapping[key] if mapping else None

    def parse(s: str):
        entries = list(map(Mapping.parse, s.split("\n")))

        return Map(entries)

def find_gaps(ranges: Iterable[Union[range, slice]], span: Union[range, slice]):
    ranges_sorted = sorted(ranges, key=lambda r: r.start)

    i = span.start
    j = 0

    while i < span.stop:
        if j >= len(ranges_sorted):
            yield range(i, span.stop)
            break

        rng = ranges_sorted[j]

        if i < rng.start:
            yield range(i, rng.start)

        i = rng.stop
        j += 1


class Almanac():
    seeds: list[range]
    seed_to_soil: Map
    soil_to_fertilizer: Map
    fertilizer_to_water: Map
    water_to_light: Map
    light_to_temperature: Map
    temperature_to_humidity: Map
    humidity_to_location: Map

    def parse_file(s: str):
        blocks = s.split("\n\n")
        seeds = parse_seeds(blocks[0])
        maps = {name: map for name, map in map(parse_map, blocks[1:])}

        return Almanac(
            seeds=seeds,
            seed_to_soil=maps["seed-to-soil"],
            soil_to_fertilizer=maps["soil-to-fertilizer"],
            fertilizer_to_water=maps["fertilizer-to-water"],
            water_to_light=maps["water-to-light"],
            light_to_temperature=maps["light-to-temperature"],
            temperature_to_humidity=maps["temperature-to-humidity"],
            humidity_to_location=maps["humidity-to-location"]
        )

def parse_map(s: str):
    lines = s.split("\n")
    match = re.match(r"^([^\s]+) map:$", lines[0])

    if match:
        name = match.group(1)
        map = Map.parse("\n".join(lines[1:]))

        return name, map
    
    raise Exception("Invalid block, expected map", s)

def parse_seeds(s: str):
    match = re.match(r"^seeds: (.+)$", s)

    if not match:
        raise Exception("Invalid block, expected seeds", s)

    match_ranges = re.finditer(r"(\d+)\s+(\d+)", match.group(1))

    if not match_ranges:
        raise Exception("Invalid block, expected seed ranges", s)

    return [range(start, start+length+1) for start, length in map(lambda x: (int(x.group(1)), int(x.group(2))), match_ranges)]

def main():
    data = sys.stdin.read()

    almanac = Almanac.parse_file(data)

    locations = reduce(
        lambda x, map: map[x],
        [
            almanac.seed_to_soil,
            almanac.soil_to_fertilizer,
            almanac.fertilizer_to_water,
            almanac.water_to_light,
            almanac.light_to_temperature,
            almanac.temperature_to_humidity,
            almanac.humidity_to_location
        ],
        almanac.seeds
    )
    
    lowest = min(locations, key=lambda l: l.destination_range.start)
    print('lowest location number: ', lowest.destination_range.start)

if __name__ == "__main__":
    main()