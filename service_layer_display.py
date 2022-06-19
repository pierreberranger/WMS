from models import DropOff, TypedSet, Shipment, Package, Trip, Groupage, Container
import datetime, time
from service_layer import database

def set_of_packages(set_of_packages: TypedSet(Package) = None) -> None:
    if set_of_packages is None:
        set_of_packages = database.set_of_packages
    base = "{:<10}|{:<25}|{:<10}|{:<30}"
    header = base.format('id', 'description', 'status', "shipment_id")
    print(header)
    print('='*len(header))
    for package in set_of_packages:
        print(base.format(package.id, package.description,
              package.status, str(package.shipment_id)))


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
    base = "{:<10}|{:<25}|{:<10}|{:<10}|{:<20}"
    header = base.format('id', "description", 'sender', 'status', "arrival_date")
    print(header)
    print('='*len(header))
    for dropoff in set_of_dropoffs:
        print(base.format(dropoff.id, dropoff.description, dropoff.sender,
              dropoff.status, dropoff.arrival_date))

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
        print(base.format(groupage.id, groupage.freight_forwarder))

def set_of_containers(set_of_containers: TypedSet(Container) = None) -> None:
    if set_of_containers is None:
        set_of_containers = database.set_of_containers
    base = "{:<10}|{:<25}"
    header = base.format('id', 'groupage_id')
    print(header)
    print('='*len(header))
    for container in set_of_containers:
        print(base.format(container.id, container.groupage_id))

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

def groupage(groupage_id: str) -> None:
    groupage = database.set_of_groupages[groupage_id]
    groupage_informations = groupage.__dict__
    print(f"{groupage_informations}")
    print("\n")
    groupage_shipments = groupage.set_of_shipments
    print(
        f"The groupage {groupage_id} contains {len(groupage_shipments)} shipments, which are : ")
    print("\n")
    set_of_shipments(groupage_shipments)

def dropoff(dropoff_id: str) -> None:
    dropoff = database.set_of_dropoffs[dropoff_id]
    dropoff_informations = dropoff.__dict__
    print(f"{dropoff_informations}")
    print("\n")
    dropoff_packages = dropoff.set_of_packages
    print(
        f"The dropoff {dropoff_id} contains {len(dropoff_packages)} packages, which are : ")
    print("\n")
    set_of_packages(dropoff_packages)

def container(container_id: str) -> None:
    container = database.set_of_containers[container_id]
    container_informations = container.__dict__
    print(f"{container_informations}")
    print("\n")
    container_packages = container.set_of_packages
    print(
        f"The container {container_id} contains {len(container_packages)} packages, which are : ")
    print("\n")
    set_of_packages(container_packages)

def trip_packages(trip_id: str) -> None:
    trip = database.set_of_trips[trip_id]
    trip_informations = trip.__dict__
    print(f"{trip_informations}")
    print("\n")
    trip_packages = TypedSet(Package)
    for groupage in trip.set_of_groupages:
        for shipment in groupage.set_of_shipments:
            for package in shipment.set_of_packages:
                trip_packages.add(package)
    set_of_packages(trip_packages)

def trip_shipments(trip_id: str) -> None:
    trip = database.set_of_trips[trip_id]
    trip_informations = trip.__dict__
    print(f"{trip_informations}")
    print("\n")
    trip_groupages = trip.set_of_groupages
    for trip_groupage in trip_groupages:
        groupage(trip_groupage.id)
        print("\n")

def trip_groupages(trip_id: str) -> None:
    trip = database.set_of_trips[trip_id]
    trip_informations = trip.__dict__
    print(f"{trip_informations}")
    print("\n")
    trip_groupages = trip.set_of_groupages
    print(
        f"The trip {trip_id} contains {len(trip_groupages)} groupages, which are : ")
    print("\n")
    set_of_groupages(trip_groupages)

def trip_containers(trip_id: str) -> None:
    trip = database.set_of_trips[trip_id]
    trip_informations = trip.__dict__
    print(f"{trip_informations}")
    print("\n")
    trip_groupages = trip.set_of_groupages
    trip_containers = TypedSet(Container)
    for groupage in trip_groupages:
        for container in groupage.set_of_containers:
            trip_containers.add(container)
    print(
        f"The trip {trip_id} contains {len(trip_containers)} containers, which are : ")
    print("\n")
    set_of_containers(trip_containers)

def incoming_dates_list() -> list:
    incoming_dates = []
    for dropoff in database.set_of_dropoffs:
        incoming_dates.append(dropoff.arrival_date)
    incoming_dates.sort(key=lambda x: time.mktime(time.strptime(x,"%Y-%m-%d %H:%M")))
    return incoming_dates

def planning_incoming() -> None:
    print("\n")
    base = "{:<30}|{:<10}|{:<10}|{:<20}"
    header = base.format('Date', 'Dropoff id', 'Sender', "Description")
    print(header)
    print('='*len(header))
    incoming_dates = incoming_dates_list()
    for date in incoming_dates :
        for dropoff in database.set_of_dropoffs :
            
            if dropoff.arrival_date == date :
                print(base.format(date, dropoff.id, dropoff.sender,
                    dropoff.description))
    print("\n")
    