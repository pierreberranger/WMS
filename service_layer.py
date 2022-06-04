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

def register_package_in_a_inshipment():
    pass