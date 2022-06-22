from models import DropOff, TypedSet, Shipment, Package, Trip, Groupage, Container

from service_layer import database

def set_of_packages(set_of_packages: TypedSet(Package) = None) -> None:
    if set_of_packages is None:
        set_of_packages = database.set_of_packages
    base = "{:<10}|{:<25}|{:<10}|{:<30}"
    header = base.format('id', 'description', 'status', "shipment_id")
    print(header)
    print('='*len(header))
    for package in set_of_packages:
        print(base.format(str(package.id), str(package.description),
              str(package.status), str(package.shipment_id)))


def set_of_shipments(set_of_shipments: TypedSet(Shipment) = None) -> None:
    if set_of_shipments is None:
        set_of_shipments = database.set_of_shipments
    base = "{:<10}|{:<25}|{:<10}|{:<20}"
    header = base.format('id', 'description', 'status', "adressee")
    print(header)
    print('='*len(header))
    for shipment in set_of_shipments:
        print(base.format(shipment.id, shipment.description,
              shipment.status, shipment.adressee))

def set_of_dropoffs(set_of_dropoffs: TypedSet(DropOff) = None) -> None:
    if set_of_dropoffs is None:
        set_of_dropoffs = database.set_of_dropoffs
    base = "{:<10}|{:<25}|{:<10}|{:<20}"
    header = base.format('id', 'description', 'status', "arrival_date")
    print(header)
    print('='*len(header))
    for dropoff in set_of_dropoffs:
        print(base.format(dropoff.id, dropoff.description,
              dropoff.status, dropoff.arrival_date))

def set_of_containers(set_of_containers: TypedSet(Container) = None) -> None:
    if set_of_containers is None:
        set_of_containers = database.set_of_containers
    base = "{:<10}|{:<25}|{:<10}"
    header = base.format('id', 'dimensions', 'groupage_id')
    print(header)
    print('='*len(header))
    for container in set_of_containers:
        print(base.format(str(container.id), str(container.dimensions),
              str(container.groupage_id)))


def set_of_trips(set_of_trips: TypedSet(Trip) = None) -> None:
    if set_of_trips is None:
        set_of_trips = database.set_of_trips
    base = "{:<10}|{:<25}"
    header = base.format('id', 'ship_name')
    print(header)
    print('='*len(header))
    for trip in set_of_trips:
        print(base.format(trip.id, trip.ship_name))

def set_of_groupages(set_of_groupages: TypedSet(Groupage) = None) -> None:
    if set_of_groupages is None:
        set_of_groupages = database.set_of_groupages
    base = "{:<10}|{:<25}"
    header = base.format('id', 'freight_forwarder')
    print(header)
    print('='*len(header))
    for groupage in set_of_groupages:
        print(base.format(str(groupage.id), str(groupage.freight_forwarder)))

def shipment(shipment_id: str) -> None:
    shipment = database.set_of_shipments[shipment_id]
    shipment_informations = shipment.__dict__
    print(f"{shipment_informations}")
    print("\n")
    shipment_packages = shipment.set_of_packages
    print(
        f"The shipment {shipment_id} contains {len(shipment_packages)} packages, which are : ")
    print("\n")
    set_of_packages(shipment_packages)