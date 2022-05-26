# Time Complexity: O(N)
# Space Complexity: O(N) [a list of locations will have a space complexity of N^2]
class Location:
    # Time Complexity: O(1)
    # Space Complexity: O(N)
    def __init__(self, id_, name, address, zip_, distances):
        self.id = int(id_)
        self.name = name
        self.address = address
        self.zip = zip_
        self.distances = distances
        self.time = None

    def __getitem__(self, item):
        return self


# Time Complexity: O(N)
# Space Complexity: O(1)
def get_location(locations: list[Location], id_: int):
    for p in locations:
        if p.id == id_:
            return p


# Time Complexity: O(1) [max() is an O(N) function but in this case N is always two]
# Space Complexity: O(1)
def get_distance(locations: list[Location], id1, id2):
    """ Gets the distance between two locations. The function depends on the structure of the csv file; Each
    location's id is equal to its index, and each location contains a list of distances all lower-indexed locations.
    Therefore, the higher of the two location id's is chosen for the first index and the lower location id is the
    index in the higher location index's list of distances. """
    return locations[max(id1, id2)].distances[min(id1, id2)]
