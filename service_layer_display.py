import matplotlib
from matplotlib import container
from matplotlib.figure import Figure
from models import DropOff, TypedSet, Shipment, Package, Trip, Groupage, Container

from service_layer import database

from matplotlib import pyplot as plt
import os

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

def create_fig_container_load_output(container_ids: set[str], package_placements: list, groupage_id: str = None) -> None:
    nb_containers = len(container_ids)
    fig = plt.figure(figsize=(5*nb_containers, 7))
    plt.rc('font', **{'size': 5})

    for container_idx, container_id in enumerate(container_ids): 
        ax = fig.add_subplot(1, nb_containers, (container_idx+1))
        container_dimensions = database.set_of_containers[container_id].dimensions[:2]

        # Draw the container limits 
        plt.plot([0, container_dimensions[0], container_dimensions[0], 0, 0], 
                [0, 0, container_dimensions[1], container_dimensions[1], 0], '--r')

        for package_placement in package_placements:
            if package_placement[0] == container_id:
                container_id, x, y, w, l, package_id = package_placement
                x1, x2, x3, x4, x5 = x, x+w, x+w, x, x
                y1, y2, y3, y4, y5 = y, y, y+l, y+l,y

                plt.plot([x1,x2,x3,x4,x5],[y1,y2,y3,y4,y5], '--k')

                package = database.set_of_packages[package_id]
                plt.annotate(f"{package_id} ({package.shipment_id})", (x+w/3, y+l/2), color='b')

        ax.set_aspect('equal')
        ax.set_title(f"{container_id}", size=15, weight='bold')
        plt.axis('off')

    # espacement entre les subplots
    fig.tight_layout(pad=10.0)
    if not(groupage_id is None):
        plt.suptitle(f"{groupage_id}", size=20)

    return fig

def show_fig(container_ids: set[str], package_placements: list, groupage_id: str = None) -> None:
    _: Figure = create_fig_container_load_output(container_ids, package_placements, groupage_id)
    plt.show()

def plot_trip_loading_proposal(groupage_placements: dict) -> None:
    for groupage_id, groupage_placement in groupage_placements.items():
        _: Figure = create_fig_container_load_output(*groupage_placement, groupage_id)
        plt.show()

def save_trip_loading_proposal(groupage_placements: dict, trip_id: str) -> None:
    os.mkdir(f"trips/{trip_id}")
    for groupage_id, (containers_id, package_placements) in groupage_placements.items():
        for container_id in containers_id:
            _: Figure = create_fig_container_load_output(set([container_id]), package_placements, groupage_id)
            plt.savefig(f"trips/{trip_id}/{container_id}.png", dpi=300)

