from models import SetOfPackages, SetOfShipments, Shipment

from service_layer import database

def set_of_packages(set_of_packages: SetOfPackages = None) -> None:
    if set_of_packages is None:
        set_of_packages = database.set_of_packages
    base = "{:<10}|{:<25}|{:<10}|{:<30}"
    header = base.format('id', 'description', 'status', "shipment_ids")
    print(header)
    print('='*len(header))
    for package in set_of_packages:
        print(base.format(package.id, package.description,
              package.status, str(package.shipment_ids)))


def set_of_shipments(set_of_shipments: SetOfShipments = None) -> None:
    if set_of_shipments is None:
        set_of_shipments = database.set_of_shipments
    base = "{:<10}|{:<25}|{:<10}|{:<20}|{:<20}"
    header = base.format('id', 'description', 'status', "adressee", "sender")
    print(header)
    print('='*len(header))
    for shipment in set_of_shipments:
        print(base.format(shipment.id, shipment.description,
              shipment.status, shipment.adressee, shipment.sender))


def shipment(shipment_id: str) -> None:
    shipment = database.set_of_shipments[shipment_id]
    shipment_informations = shipment.__dict__
    print(f"{shipment_informations}")
    print("\n")
    set_of_packages = shipment.set_of_packages
    print(
        f"The shipment {shipment_id} contains {len(set_of_packages)} packages, which are : ")
    print("\n")
    set_of_packages(set_of_packages)