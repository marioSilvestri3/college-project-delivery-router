from model.package import Package


# Time Complexity: O(1)
# Space Complexity: O(1)
class Truck:
    MAXIMUM_PACKAGES = 16
    MILES_PER_HOUR = 18

    def __init__(self, id_):
        self.id = id_
        self.packages: list[Package] = []
        self.dispatch_time = None
