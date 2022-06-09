from datetime import datetime
from confirm import package
from models import Package, Dimensions, Shipment, DropOff, Groupage, Trip
import pickle_data as database



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

def access_to_the_package_informations_by_id(package_id: str) -> dict:
    package = database.set_of_packages[package_id]
    return {"dimensions": package.dimensions, "weight": package.weight, "status": package.status, "package_type": package.package_type, "description": package.description}

""" def add_one_package_by_id(id):
    new_package: Package = database.set_of_packages[id].__copy__()
    database.set_of_packages.add(new_package) """

def declare_dropoff_actual_arrival(dropoff_id, actual_arrival_date) -> None:
    dropoff = database.set_of_dropoffs[dropoff_id]
    dropoff.status = DropOff.statuses[1] 
    dropoff.arrival_date = actual_arrival_date 
    dropoff_packages = dropoff.set_of_packages
    for package in dropoff_packages: 
        package.status = Package.statuses[1]

def del_dropoff(id) -> None:
    database.set_of_dropoffs.remove(id)

def del_shipment(id) -> None:
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
    return groupage_id

def add_shipment_to_a_groupage(groupage_id: str, shipment_id: str) -> None:
    shipment_to_add = database.set_of_shipments[shipment_id]
    shipment_to_add.groupage_id = groupage_id

def declare_trip(ship_name: str) -> str:
    new_trip = Trip(ship_name)
    database.set_of_trips.add(new_trip)
    return new_trip.id

def add_shipment_to_a_trip(trip_id: str, groupage_id: str) -> None:
    groupage_to_add = database.set_of_groupages[groupage_id]
    groupage_to_add.trip_id = trip_id