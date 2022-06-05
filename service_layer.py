from datetime import datetime
from confirm import package
from models import SetOfPackages, Package, Dimensions, InBoundShipment, OutBoundShipment
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

def declare_inshipment(inshipment_informations: dict) -> str:
    new_inshipment = InBoundShipment(**inshipment_informations)
    database.set_of_shipments.add(new_inshipment)
    return new_inshipment.id

def register_package_in_a_shipment_by_id(package_id: str, shipment_id: str) -> None:
    package_to_add: Package = database.set_of_packages[package_id]
    package_to_add.shipment_ids.add(shipment_id)

def access_to_the_package_informations_by_id(package_id: str) -> dict:
    package = database.set_of_packages[package_id]
    return {"dimensions": package.dimensions, "weight": package.weight, "status": package.status, "package_type": package.package_type, "description": package.description}

""" def add_one_package_by_id(id):
    new_package: Package = database.set_of_packages[id].__copy__()
    database.set_of_packages.add(new_package) """

def declare_inshipment_actual_arrival(inshipment_id, actual_arrival_date) -> None:
    inshipment = database.set_of_shipments[inshipment_id]
    inshipment.status = InBoundShipment.statuses[0] 
    inshipment.arrival_date = actual_arrival_date 
    inshipment_packages = inshipment.set_of_packages
    for package in inshipment_packages: 
        package.status = Package.statuses[1]

def del_inshipment(id) -> None:
    database.set_of_shipments.remove(id)

def declare_outshipment(outshipment_informations) -> str:
    outshipment = OutBoundShipment(**outshipment_informations)
    database.set_of_shipments.add(outshipment)
    return outshipment.id
    
def declare_outshipment_actual_departure(actual_departure_date: datetime, outshipment_id: str) -> None:
    outshipment: OutBoundShipment = database.set_of_shipments[outshipment_id]
    outshipment.departure_date = actual_departure_date
    outshipment.status = OutBoundShipment.statuses[0]
    outshipment_packages = outshipment.set_of_packages
    for package in outshipment_packages:
        package.status = Package.statuses[2]

def declare_outshipment_actual_delivery(actual_delivery_date: datetime, outshipment_id: str) -> None:
    outshipment = database.set_of_shipments[outshipment_id]
    outshipment.expected_arrival_date = actual_delivery_date
    outshipment.status = OutBoundShipment.statuses[2]
    outshipment_packages = outshipment.set_of_packages
    for package in outshipment_packages:
        package.status = Package.statuses[5]