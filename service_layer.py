from datetime import datetime
from models import Package, Shipment, DropOff, Groupage, Trip, TypedSet, ContainerPaletWide, ContainerStandard
import pickle_data as database

from copy import deepcopy


def load():
    filename = "database.txt"
    database.load(filename)

def save_and_quit():
    # save the data in a text file
    database.save()

def add_one_package(package_informations: dict) -> str:
    new_package = Package(**package_informations)
    database.set_of_packages.add(new_package)
    return new_package.id

def del_one_package(id: str) -> None:
    database.set_of_packages.remove(id)

def change_package_status(id: str, new_status: str) -> None:
    database.set_of_packages[id].status = new_status

def declare_dropoff(dropoff_informations: dict) -> str:
    new_dropoff = DropOff(**dropoff_informations)
    database.set_of_dropoffs.add(new_dropoff)
    return new_dropoff.id

def declare_shipment(shipment_informations: dict) -> str:
    new_shipment = Shipment(**shipment_informations)
    database.set_of_shipments.add(new_shipment)
    return new_shipment.id

def register_package_in_a_dropoff_by_id(package_id: str, dropoff_id: str) -> None:
    package_to_add: Package = database.set_of_packages[package_id]
    package_to_add.dropoff_id = dropoff_id

def register_package_in_a_shipment_by_id(package_id: str, shipment_id: str) -> None:
    package_to_add: Package = database.set_of_packages[package_id]
    package_to_add.shipment_id = shipment_id

def add_one_package_by_id(id: str) -> str: 
    new_package: Package = deepcopy(database.set_of_packages[id])
    database.set_of_packages.add(new_package)
    return new_package.id

def declare_dropoff_actual_arrival(dropoff_id: str, actual_arrival_date: datetime) -> None:
    dropoff = database.set_of_dropoffs[dropoff_id]
    dropoff.status = DropOff.statuses[1] 
    dropoff.arrival_date = actual_arrival_date 
    dropoff_packages = dropoff.set_of_packages
    for package in dropoff_packages: 
        package.status = Package.statuses[1]

def update_dropoff_arrival_date(dropoff_id: str, actual_arrival_date: datetime) -> None:
    dropoff = database.set_of_dropoffs[dropoff_id]
    dropoff.arrival_date = actual_arrival_date 

def del_dropoff(id: str) -> None:
    database.set_of_dropoffs.remove(id)

def remove_package_from_dropoff(package_id: str, dropoff_id: str) -> None:
    package = database.set_of_packages[package_id]
    if package.dropoff_id == dropoff_id :
        package.dropoff_id = None
    else :
        print("Pay attention, the package you want to remove is not in the dropoff you indicate.")


def del_shipment(id: str) -> None:
    database.set_of_shipments.remove(id)

def declare_shipment_actual_departure_from_warehouse(actual_departure_date_from_warehouse: datetime, shipment_id: str) -> None:
    shipment: Shipment = database.set_of_shipments[shipment_id]
    shipment.departure_date_from_warehouse = actual_departure_date_from_warehouse
    shipment.status = Shipment.statuses[2]
    shipment_packages = shipment.set_of_packages
    for package in shipment_packages:
        package.status = Package.statuses[2]

def declare_shipment_actual_delivery(actual_delivery_date: datetime, shipment_id: str) -> None:
    shipment = database.set_of_shipments[shipment_id]
    shipment.delivery_date = actual_delivery_date
    shipment.status = Shipment.statuses[3]
    shipment_packages = shipment.set_of_packages
    for package in shipment_packages:
        package.status = Package.statuses[5]

def declare_groupage(freight_forwarder: str) -> str:
    new_groupage = Groupage(freight_forwarder)
    database.set_of_groupages.add(new_groupage)
    return new_groupage.id

def add_shipment_to_a_groupage(groupage_id: str, shipment_id: str) -> None:
    shipment_to_add = database.set_of_shipments[shipment_id]
    shipment_to_add.groupage_id = groupage_id

def declare_trip(ship_name: str) -> str:
    new_trip = Trip(ship_name)
    database.set_of_trips.add(new_trip)
    return new_trip.id
    
def add_groupage_to_a_trip(trip_id: str, groupage_id: str) -> None:
    groupage_to_add = database.set_of_groupages[groupage_id]
    groupage_to_add.trip_id = trip_id

def del_groupage(groupage_id: str) -> None:
    database.set_of_groupages.remove(groupage_id)

def del_trip(trip_id: str) -> None:
    database.set_of_trips.remove(trip_id)

def load_packages_in_trip(trip_id: str) -> None:
    trip_packages = TypedSet(Package)
    trip = database.set_of_trips[trip_id]
    for groupage in trip.set_of_groupages:
        for shipment in groupage.set_of_shipments:
            for package in shipment.set_of_packages:
                trip_packages.add(package)
    for package in trip_packages :
        package.status = Package.statuses[3]

def weight_trip(trip_id: str) -> float:
    trip = database.set_of_trips[trip_id]
    trip_groupages = trip.set_of_groupages
    total_weight = 0
    for groupage in trip_groupages:
        groupage_id = groupage.id
        for container in groupage.set_of_containers:
            if container.groupage_id == groupage_id:
                total_weight += container.weight
    return total_weight

def add_groupage_to_trip(trip_id: str, groupage_id: str) -> None:
    groupage_to_add = database.set_of_groupages[groupage_id]
    groupage_to_add.trip_id = trip_id

def del_groupage_from_trip(groupage_id: str) -> None:
    groupage_to_del = database.set_of_groupages[groupage_id]
    groupage_to_del.trip_id = None

def add_container_to_database(type_container: str) -> str:
    if type_container == "standard" :
        new_container = ContainerStandard()
        database.set_of_containers.add(new_container) 
    elif type_container == "palet_wide":
        new_container = ContainerPaletWide()
        database.set_of_containers.add(new_container)
    return new_container.id

def del_container_from_database(container_id: str) -> None:
    container_to_del = database.set_of_containers[container_id]
    database.set_of_containers.remove(container_to_del.id)

def available_containers(nb_container_wide, nb_container_standard) -> set[str]:
    nb_container_wide_choosen = 0
    nb_container_standard_choosen = 0
    available_containers = set()
    for container_id, class_name in ((str(c.id), c.__class__.__name__) for c in database.set_of_containers if (c.groupage_id is None)):
        if  class_name == "ContainerPaletWide" and nb_container_wide_choosen < nb_container_wide:
            nb_container_wide_choosen += 1
            available_containers.add(container_id)

        elif class_name == "ContainerStandard" and nb_container_standard_choosen < nb_container_standard:
            nb_container_standard_choosen += 1
            available_containers.add(container_id)

        if (nb_container_standard_choosen == nb_container_standard) and (nb_container_wide_choosen == nb_container_wide):
            return available_containers