from collections import namedtuple
from .file_id_generator import FileIDGenerator

Dimensions = namedtuple("Dimensions", "width length height")

packages_ids = FileIDGenerator("MAX_ID_Packages.txt")

class Package():

    def __init__(self, dimensions: Dimensions, status: str, package_type: str, description: str="", shipment_id=None, id=None) -> None:
        self.status = status
        self.dimensions = dimensions
        self.package_type = package_type
        self.shipment_id = shipment_id
        self.description = description
        if id == None:
            self.id = next(packages_ids)
        else:
            self.id = id

    def __eq__(self, other):
        if isinstance(other, Package):
            return self.id == other.id
        elif isinstance(other, int):
            return self.id == other
        else:
            raise ValueError("A Package can only be compared to a Package or an int") 

    def __hash__(self):
        return self.id
    
    def is_same_package(self, other) -> bool:
        return self.dimensions == other.dimensions and self.status == other.status \
                and self.package_type == other.package_type and self.id == other.id

    # Pour modifier un package dans un Shipment à partir de l'id : 
    # shipment[id].status = status