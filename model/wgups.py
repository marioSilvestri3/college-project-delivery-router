import datetime
import string
from typing import Optional

from model.chaining_hash_table import ChainingHashTable
from model.location import Location, get_distance
from model.package import Package, PackagePriority
from model.truck import Truck


# The main class for the programs. Integrates all objects and data structures to manage the truck routes.
# Time Complexity: O(N^2) [iterating through packages list for each package]
# Space Complexity: O(N^2) [each additional location increases number of connections exponentially]
class WGUPS:

    # Time Complexity: O(N) [number of packages + number of trucks]
    # Space Complexity: O(N^2) [each additional location N must have N distances to other locations]
    def __init__(self, locations: list[Location], packages: list[Package], trucks):
        self.locations = locations  # Space Complexity: O(N^2)
        self.packages = ChainingHashTable()
        for p in packages:
            self.packages.insert_(p.id, p)
        self.time = datetime.time(8, 00)
        self.trucks = [Truck(i + 1) for i in range(trucks)]

    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def load_truck(self, truck_id, package_id, priority: PackagePriority = PackagePriority.LOW):
        package = self.packages.lookup_(package_id)
        package.priority = priority
        package.truck = self.trucks[truck_id - 1]
        self.trucks[truck_id - 1].packages.append(package)
        print("\tTruck " + str(truck_id) + " loaded with package " + str(package_id))

    # Time Complexity: O(N)
    # Space Complexity: O(1)
    def get_location_id(self, package: Package):
        for loc in self.locations:
            if loc.address == package.address:
                return loc.id

    # Time Complexity: O(N)
    # Space Complexity: O(1)
    def get_location(self, package: Package):
        for loc in self.locations:
            if loc.address == package.address:
                return loc

    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def get_distance(self, location_id1, location_id2):
        return get_distance(self.locations, location_id1, location_id2)

    # Splits the list of packages by priority level, then runs the nearest neighbor algorithm on each list.
    # Time Complexity: O(N^2)
    # Space Complexity: O(N)
    def generate_route(self, truck_id, start_time: datetime):

        self.trucks[truck_id - 1].dispatch_time = start_time

        high_priority = []
        medium_priority = []
        low_priority = []

        for package in self.trucks[truck_id - 1].packages:
            package.dispatched_time = start_time
            if package.priority == PackagePriority.HIGH:
                high_priority.append(package)
            elif package.priority == PackagePriority.MEDIUM:
                if filter(lambda x: x.id == package.address, high_priority):
                    high_priority.append(package)
                else:
                    medium_priority.append(package)
            else:
                if filter(lambda x: x.id == package.address, high_priority):
                    high_priority.append(package)
                elif filter(lambda x: x.id == package.address, medium_priority):
                    medium_priority.append(package)
                else:
                    low_priority.append(package)

        high_priority_route, time = self.nearest_neighbor(high_priority, self.locations[0].id, start_time)
        medium_priority_route, time = self.nearest_neighbor(medium_priority, high_priority_route[-1][0], time)
        low_priority_route, time = self.nearest_neighbor(low_priority, medium_priority_route[-1][0], time)

        route = high_priority_route + medium_priority_route + low_priority_route
        back_to_hq = self.get_distance(route[-1][0], 0)
        route.append((0, "back_to_hq", back_to_hq))
        time = time + datetime.timedelta(minutes=back_to_hq / Truck.MILES_PER_HOUR * 60)

        return route, time

    # Time Complexity: O(N^2) [number of packages * number of packages / 2]
    # Space Complexity: O(N)
    def nearest_neighbor(self, packages: list[Package], start_location_id, start_time: datetime):
        remaining_packages = packages  # Space: O(N) [n = number of packages]
        route = []  # Space: O(N) [n = number of packages]
        current_time = start_time
        current_location_id = start_location_id

        if len(remaining_packages) == 0:
            route = [(current_location_id, None, 0)]
            return route, current_time

        # loop through all remaining packages to find the one that is closest to the current location. when a package
        # is found, return that package id to the route as well as distance and time, then remove
        # that package from the remaining packages and keep looping until the list is empty.
        # Time Complexity: O(N^2) [number of packages * number of packages/2]
        # Space Complexity: O(N) [number of packages to route]
        while len(remaining_packages) > 0:

            next_package: Optional[Package] = None
            next_location_id = None

            # loop through each package to find the closest location
            for package in remaining_packages:  # Time: O(N) [n = number of packages]
                if package.available_time and package.available_time > current_time:
                    # This conditional stops package #9 with the incorrect address from being updated until 10:20am
                    # per the task assumptions
                    continue
                location_id = self.get_location_id(package)
                if next_package is None:
                    next_package = package
                    next_location_id = self.get_location_id(next_package)
                    continue
                if location_id == current_location_id:
                    package.delivered_time = current_time
                    route.append((self.get_location_id(package), package.id, 0))
                    remaining_packages.remove(package)
                    continue
                if self.get_distance(current_location_id, location_id) \
                        < self.get_distance(current_location_id, next_location_id):
                    next_package = package
                    next_location_id = self.get_location_id(package)

            # we have the closest location, now update the current location, remove the package from the remaining
            # packages, and update the delivery time and miles traveled

            distance = self.get_distance(current_location_id, next_location_id)
            route.append((next_location_id, next_package.id, distance))
            minutes_to_travel = distance / Truck.MILES_PER_HOUR * 60
            current_time = current_time + datetime.timedelta(minutes=minutes_to_travel)
            next_package.delivered_time = current_time

            current_location_id = next_location_id
            remaining_packages.remove(next_package)  # Time Complexity: O(N)

        return route, current_time

    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def get_package_status(self, user_input: string):
        try:
            package_id, time = user_input.split()
            package_id = int(package_id)
            hours, minutes = time.split(':')
            at_datetime = datetime.datetime(1, 1, 1, int(hours), int(minutes))
            package = self.packages.lookup_(package_id)
            package.print_package_status(at_datetime)
        except:
            print("Input error")

    # Time Complexity: O(N log N) [packages.sort()]
    # Space Complexity: O(N) [packages.sort()]
    def get_all_package_statuses(self, input_time: string):
        try:
            hours, minutes = input_time.split(':')
            input_time = datetime.datetime(1, 1, 1, int(hours), int(minutes))
            packages = self.packages.get_all()
            packages.sort(key=lambda x: x.id)  # Python algorithm Timsort, hybrid of merge and insertion sort.
            for package in packages:
                package.print_package_status(input_time)
        except:
            print("Input error")
