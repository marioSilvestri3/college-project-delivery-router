from datetime import datetime
from enum import Enum


class PackagePriority(Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3


class PackageStatus(Enum):
    HUB = 1
    EN_ROUTE = 2
    DELIVERED = 3


# Time Complexity: O(1)
# Space Complexity: O(1)
class Package:

    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def __init__(self, id_, address, city, zip_, deadline, weight, notes,
                 priority: PackagePriority = PackagePriority.LOW):
        self.id = int(id_)
        self.address = address
        self.city = city
        self.zip = zip_
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.priority: PackagePriority = priority
        self.dispatched_time = None
        self.available_time = None
        self.delivered_time = None
        self.truck = None

    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def print_package_status(self, time_: datetime):
        print("Package " + str(self.id) + " at " + time_.strftime("%H:%M"))
        print("Delivery address: " + str(self.address) + ", " + str(self.city) + ", " + str(self.zip))
        print("Weight: " + str(self.weight))
        print("Deadline: " + str(self.deadline))
        if self.notes != "":
            print("Notes: " + str(self.notes))
        print("Dispatch: Truck " + str(self.truck.id) + ", leaving warehouse at " +
              str(self.truck.dispatch_time.strftime("%H:%M")))
        status = "Warehouse; delivery scheduled for " + self.delivered_time.strftime("%H:%M")

        if time_ > self.dispatched_time:
            status = "En Route on truck " + str(self.truck.id) + "; delivery scheduled for " + \
                     self.delivered_time.strftime("%H:%M")
        if time_ > self.delivered_time:
            status = "Delivered at " + self.delivered_time.strftime("%H:%M")
        print("Status: " + status + "\n")
