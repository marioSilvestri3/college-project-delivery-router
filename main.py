# Mario Silvestri III - 000941631
import datetime

from model.package import PackagePriority
from model.wgups import WGUPS
from util.csv_reader import get_location_data, get_package_data


# initiate WGUPS with location data and package data from cvs files and two trucks
# Time Complexity: O(N^2)
# Space Complexity: O(N^2)
wgups = WGUPS(get_location_data(), get_package_data(), 3)

print("Welcome to WGUPS")
print("Time is " + str(wgups.time))
print("Packages in warehouse: " + str(len(wgups.packages)))

input_ = input("Press Q to quit, R to generate routes\n")

# Starts the process of generating routes using the nearest neighbor algorithm.
# Time Complexity: O(N^2) [number of packages * number of packages / 2]
# Space Complexity: O(N^2) [number of packages * number of packages]
if input_ == "R":
    print()
    print("All packages will be delivered based on delivery time constraints and then distance from current location "
          "using the nearest neighbor algorithm.\n")
    print("Constraints:")
    print("\tPackages 3, 18, 36, and 38 must go on truck 2")
    print("\tPackages 14, 15, and 19 must go together")
    print("\tPackages 6, 25, 28, and 32 are delayed, and must be dispatched after 9:05am")
    print("\tPackage 9 address is incorrect and won't be available until 10:20am")
    print("\tPackage 15 must be delivered by 9:00am")
    print("\tPackages 1, 6, 13, 14, 16, 20, 25, 29, 30, 31, 34, 37, and 40 must be delivered by 10:30am\n")

    print("Load the packages that must go on truck 2")
    wgups.load_truck(2, 3, PackagePriority.MEDIUM)
    wgups.load_truck(2, 18, PackagePriority.MEDIUM)
    wgups.load_truck(2, 36, PackagePriority.MEDIUM)
    wgups.load_truck(2, 38, PackagePriority.MEDIUM)

    print("\nLet's take care of the early deliveries and load them on truck 1 to go out at 8:00am")
    wgups.load_truck(1, 1, PackagePriority.MEDIUM)
    wgups.load_truck(1, 13, PackagePriority.MEDIUM)  # So it can be delivered with 15 and 19
    wgups.load_truck(1, 14, PackagePriority.MEDIUM)
    wgups.load_truck(1, 16, PackagePriority.MEDIUM)
    wgups.load_truck(1, 20, PackagePriority.MEDIUM)
    wgups.load_truck(1, 29, PackagePriority.MEDIUM)
    wgups.load_truck(1, 30, PackagePriority.MEDIUM)
    wgups.load_truck(1, 31, PackagePriority.MEDIUM)
    wgups.load_truck(1, 34, PackagePriority.MEDIUM)
    wgups.load_truck(1, 37, PackagePriority.MEDIUM)
    wgups.load_truck(1, 40, PackagePriority.MEDIUM)

    print("\nPackages 6, 25, 28, and 32 are late, so we'll load them on truck 2 to send out at 9:05, "
          "and prioritize package 25 since it has an early deadline.")
    wgups.load_truck(2, 25, PackagePriority.HIGH)
    wgups.load_truck(2, 6, PackagePriority.MEDIUM)
    wgups.load_truck(2, 28, PackagePriority.MEDIUM)
    wgups.load_truck(2, 32, PackagePriority.MEDIUM)

    print("\nPackages 15 and 19 have to go out with package 14 on truck 1. Package 15 "
          "has an early deadline so it's set to high priority.")

    wgups.load_truck(1, 15, PackagePriority.HIGH)
    wgups.load_truck(1, 19, PackagePriority.MEDIUM)

    print("Lets fill up truck 2 with its maximum of 16 packages at low priority. Truck 1 will finish its early "
          "delivery and then the driver will come back for truck 3. Package 9 won't be available to deliver until "
          "10:20 when the correct address comes in.")

    wgups.load_truck(2, 2, PackagePriority.LOW)
    wgups.load_truck(2, 4, PackagePriority.LOW)
    wgups.load_truck(2, 5, PackagePriority.LOW)
    wgups.load_truck(2, 7, PackagePriority.LOW)
    wgups.load_truck(2, 8, PackagePriority.LOW)
    wgups.load_truck(2, 10, PackagePriority.LOW)
    wgups.load_truck(2, 11, PackagePriority.LOW)
    wgups.load_truck(2, 12, PackagePriority.LOW)

    wgups.load_truck(3, 9)

    # Time Complexity: O(1) -> O(N) [based on hash table bucket size / collision frequency]
    # Space Complexity: O(1)
    wgups.packages.lookup_(9).available_time = datetime.datetime(1, 1, 1, 10, 20)

    wgups.load_truck(3, 17)
    wgups.load_truck(3, 21)
    wgups.load_truck(3, 22)
    wgups.load_truck(3, 23)
    wgups.load_truck(3, 24)
    wgups.load_truck(3, 26)
    wgups.load_truck(3, 27)
    wgups.load_truck(3, 33)
    wgups.load_truck(3, 35)
    wgups.load_truck(3, 39)

    print("\nHere's how the packages are loaded: ")
    print("\tTruck 1: " + str(sorted(p.id for p in wgups.trucks[0].packages)))
    print("\tTruck 2: " + str(sorted(p.id for p in wgups.trucks[1].packages)))
    print("\tTruck 3: " + str(sorted(p.id for p in wgups.trucks[2].packages)))

    print("\nHere's the order of the packages delivered: ")
    # Time Complexity: O(N^2) [number of packages * number of packages / 2]
    # Space Complexity: O(N^2) [number of packages * number of packages]
    truck1, wgups.time = wgups.generate_route(1, datetime.datetime(1, 1, 1, 8))
    truck2, truck2_return_time = wgups.generate_route(2, datetime.datetime(1, 1, 1, 9, 5))
    truck3, wgups.time = wgups.generate_route(3, wgups.time)

    total_miles = 0

    # Time Complexity: O(N) [number of packages]
    # Space Complexity: O(1)
    for tuple_ in truck1:
        total_miles += tuple_[2]

    for tuple_ in truck2:
        total_miles += tuple_[2]

    for tuple_ in truck3:
        total_miles += tuple_[2]

    print("\tTruck 1: " + str([tuple_[1] for tuple_ in truck1 if tuple_[1] is not None]))
    print("\tTruck 2: " + str([tuple_[1] for tuple_ in truck2 if tuple_[1] is not None]))
    print("\tTruck 3: " + str([tuple_[1] for tuple_ in truck3 if tuple_[1] is not None]) + "\n")

    print("Total miles traveled: " + "{:.2f}".format(total_miles) + "\n")

# Enables the user to view the status of packages.
# Time Complexity: O(N log N)
# Space Complexity: O(N)
while input_ != "Q":
    input_ = input("Q to Quit. P for package status. A for all package statuses.\n\n")

    # Time Complexity: O(1)
    # Space Complexity: O(1)
    if input_ == "P":
        print("Enter Package ID and time in HH:MM (24h) for package status. \nExamples: 1 09:05, 24 13:35\n")
        input_ = input()
        print()
        wgups.get_package_status(input_)

    # Time Complexity: O(N log N)
    # Space Complexity: O(N)
    if input_ == "A":
        print("Enter time in HH:MM (24h) for all package statuses at that time. \nExamples: 09:05, 13:35")
        input_ = input()
        print()
        wgups.get_all_package_statuses(input_)

