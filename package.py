from collections import namedtuple
from itertools import count

Dimensions = namedtuple("Dimensions", "width length height")
Trip = set[int]

class Package:

    __max_id : count = count()
    __shipment : dict[int] = dict()

    def __init__(self, dimensions, status, package_type):
        self.dimensions : tuple = dimensions
        self.status : str = status
        self.package_type : str = package_type

    @classmethod
    def set_shipment(cls, id_iterator:count=count(), shipment:dict=dict()):
        cls.__max_id = id_iterator
        cls.__shipment = shipment

    @classmethod # faire une version package.add_package() en plus
    def add_package(cls, dimensions: tuple , status: str, package_type: str) -> None:
        """
        Adds a package to the shipment
        """
        new_id : int = next(Package.__max_id) # automatic numbering
        new_package : Package = cls(dimensions, status, package_type)
        cls.__shipment[new_id] = new_package

    @classmethod
    def get_shipment(cls):
        return cls.__shipment
    
    @classmethod
    def delete(cls, id: int) -> None:
        try:
            del cls.__shipment[id]
        except KeyError:
            raise KeyError("The shipment does not contain the id")

    def __eq__(self, other):
        return self.dimensions == other.dimensions and self.status == other.status \
                and self.package_type == other.package_type
    
    def set_status(self, new_status: str) -> None:
        self.status = new_status

    def set_dimensions(self, new_dimensions: Dimensions) -> None:
        self.dimensions = new_dimensions

    def set_package_type(self, new_package_type: str) -> None:
        self.package_type = new_package_type

# Définitions des fonctions relatives aux voyages (Trip)

def add_package_trip(trip: Trip, id: int) -> None:
    trip.add(id)
    
def remove_package_trip(trip: Trip, id: int) -> None:
    try:
        trip.remove(id)
    except KeyError:
        raise KeyError("The trip does not contain this id")
