# Mario Silvestri III
import csv
from model.location import Location
from model.package import Package

"""
Utility functions for extracting data from csv files into formats applicable for Package and Location classes.
"""


# Import distances data csv file.
# Time Complexity: O(N)
# Space Complexity: O(N^2)
def get_location_data():
    distance_table = []

    with open('data/distance.csv', newline='') as distance_csv:
        reader = csv.reader(distance_csv)

        # Time Complexity: O(N) [loops once for each row of data]
        # Space Complexity: O(N) [adds one row to distance table for each row of data]
        for index, row in enumerate(reader):
            row.insert(0, str(index))
            distance_table.extend([row])

        location_list: list[Location] = []

        # Time Complexity: O(N)
        # Space Complexity: O(N^2) [each additional location adds N distances to its list of locations]
        for index, location in enumerate(distance_table):
            location = [i for i in location if i]
            location_list.append(Location(location[0], location[1], location[2],
                                          location[3], [float(i) for i in location[4:-1]]))
        return location_list


# Import packages data csv file.
# Time Complexity: O(N)
# Space Complexity: O(N)
def get_package_data():
    package_table = []
    package_list: list[Package] = []

    with open('data/package.csv', newline='') as package_csv:
        reader = csv.reader(package_csv)

        for row in reader:
            package_table.extend([row])

        for index, package in enumerate(package_table):
            package_list.append(Package(package[0], package[1],
                                        package[2], package[4], package[5],
                                        package[6], package[7]))

    return package_list
