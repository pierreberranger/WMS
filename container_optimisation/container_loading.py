from typing import Tuple
from models import Groupage, Container, Package, Shipment, Dimensions, Trip
import pickle_data as database
from matplotlib import pyplot as plt

from rectpack import newPacker, SkylineMwfl, GuillotineBssfSas, MaxRectsBaf, SkylineBlWm

def container_loading(groupage: Groupage, available_containers_id: set[str]) -> Tuple[set[str], list]:
    """Given a groupage and a set of available_container_ids, loads containers with the given groupage.
    Returns:
    - a set of the used container ids
    - the placement of each package within those containers"""


    rectangles = [(package.dimensions.width, package.dimensions.length, package.id) for shipment in groupage.set_of_shipments
                                                for package in shipment.set_of_packages]
    

    bins = [database.set_of_containers[container_id].dimensions[:2] for container_id in available_containers_id]

    packer = newPacker(pack_algo=SkylineBlWm, sort_algo=lambda rectlist: sorted(rectlist, reverse=True, 
        key=lambda width_length_id: (database.set_of_packages[width_length_id[2]].shipment_id, 
                                        width_length_id[0]*width_length_id[1])))

    # Add the rectangles to packing queue
    for width, length,id in rectangles:
        packer.add_rect(width,length,id)

    # Add the bins where the rectangles will be placed
    for b in bins:
        packer.add_bin(*b)

    # Start packing
    packer.pack()

    package_placements = packer.rect_list()

    for i, container_id in enumerate(available_containers_id):
        for j, package_placement in enumerate(package_placements):
            if package_placement[0] == i:
                _, *args = package_placement
                package_placements[j] = tuple([container_id, *args])

    return {package_placement[0] for package_placement in package_placements}, package_placements

def trip_loading(trip_id: str, available_containers_id: set[str]) -> dict:
    trip: Trip = database.set_of_trips[trip_id]
    groupage_placements = dict()
    for groupage in trip.set_of_groupages:
        groupage_placements[groupage.id] = container_loading(groupage, available_containers_id)
        available_containers_id = available_containers_id.difference(groupage_placements[groupage.id][0])
    return groupage_placements

def validate_container_loading_proposal(package_placements: list) -> None:
    for container_id, _, _, width, length, package_id in package_placements:
        package: Package = database.set_of_packages[package_id]
        package.dimensions = Dimensions(width, length, package.dimensions.height)
        package.container_id = container_id

def validate_trip_loading_proposal(groupage_placements: dict) -> None:
    for groupage_id, (containers_id, package_placements) in groupage_placements.items():
        for container_id in containers_id:
            container =  database.set_of_containers[container_id]
            container.groupage_id = groupage_id
        validate_container_loading_proposal(package_placements)