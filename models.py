from collections import namedtuple
from typing import Union
import datetime

Dimensions = namedtuple("Dimensions", "width length height")

class FileIDGenerator:
    def __init__(self, filename: str):
        self.filename = filename
        # initialisation de vos trucs avec les fichiers

    def __next__(self) -> int:
        with open(self.filename, mode='r') as file_content:
            next_id = int(file_content.readlines()[0]) + 1
        with open(self.filename, mode='w') as file_content:
            file_content.write(f"{next_id}")
        return next_id

shipments_ids = FileIDGenerator("MAX_ID_Shipments.txt")
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

class SetOfPackages(set):

    def __getitem__(self, id: int) -> Package:
        for package in self:
            if package.id == id:
                return package
        raise KeyError("This id does not exist")

    def remove(self, other: Union[int, Package]) -> None:
        if isinstance(other, Package):
            super().remove(other)
        elif isinstance(other, int):
            for package in self.copy():
                if package.id == other:
                    super().remove(package)
                    return None
            raise KeyError("This id does not exist")
        else:
            
            raise ValueError("The argument must be an int or a Package")

class Shipment():

    def __init__(self, status: str, set_of_packages: SetOfPackages, adressee: str, sender: str, description: str="", id: int=None):
        self.status: str = status
        self.set_of_packages: SetOfPackages = set_of_packages
        self.adressee: str = adressee
        self.sender: str = sender
        if id == None:
            self.id = next(shipments_ids)
        else:
            self.id = id

class SetOfShipments(set):

    def __getitem__(self, id: int) -> Shipment:
        for shipment in self:
            if shipment.id == id:
                return shipment
        raise KeyError("This id does not exist")

    def remove(self, other: Union[int, Shipment]) -> None:
        if isinstance(other, Shipment):
            super().remove(other)
        elif isinstance(other, int):
            for shipment in self.copy():
                if shipment.id == other:
                    super().remove(shipment)
                    return None
            raise KeyError("This id does not exist")
        else:
            
            raise ValueError("The argument must be an int or a Shipment")


class OutBoundShipment(Shipment):

    def __init__(self, departure_date: datetime, expected_arrival_date: datetime, status: str, id: int, set_of_packages: SetOfPackages, adressee: str, sender: str=""):
        self.departure_date: datetime = departure_date
        self.expected_arrival_date: datetime = expected_arrival_date
        super().__init__(status, id, set_of_packages, adressee, sender)

class InBoundShipment(Shipment):

    def __init__(self, arrival_date, status: str, id: int, set_of_packages: SetOfPackages, sender: str, adressee: str=""):
        self.arrival_date: datetime = arrival_date
        super().__init__(status, id, set_of_packages, adressee, sender)