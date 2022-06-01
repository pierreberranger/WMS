from collections import namedtuple
from typing import Union
from datetime import datetime
from pickle import dump

Dimensions = namedtuple("Dimensions", "width length height")
from pickle_data import with_save
import pickle_data as database

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
    statuses = ('stored', 'inbound', 'outbound', 'delivered')
    types = ('EPAL', '20ISO', 'OOG')

    def __init__(self, dimensions: Dimensions, status: str, package_type: str, description: str = "", shipment_ids: set = None, id: str = None) -> None:
        self.status = status
        self.dimensions = dimensions
        self.package_type = package_type
        if shipment_ids is None:
            self.shipment_ids = set()
        else:
            self.shipment_ids = shipment_ids
        self.description = description
        if id is None:
            self.id = f"P{next(packages_ids)}"
        else:
            self.id = id

    @with_save
    def __setattr__(self, __name: str, value: str) -> None:
        super().__setattr__(__name, value)

    def __eq__(self, other):
        if isinstance(other, Package):
            return self.id == other.id
        elif isinstance(other, int):
            return self.id == other
        else:
            raise ValueError(
                "A Package can only be compared to a Package or an int")

    def __hash__(self):
        return hash(self.id)

    def is_same_package(self, other) -> bool:
        return self.dimensions == other.dimensions and self.status == other.status \
            and self.package_type == other.package_type and self.id == other.id


SetOfPackages = set


class Shipment():

    def __init__(self, status: str, set_of_packages: SetOfPackages = None, adressee: str ="", sender: str = "", description: str = ""):
        self.status: str = status
        self.adressee: str = adressee
        self.sender: str = sender
        self.description: str = description
        self.id = f"S{next(shipments_ids)}"
        if not(set_of_packages is None):
            for package in set_of_packages:
                package.shipment_ids.add(self.id)

    @property
    def set_of_packages(self):
        if database.set_of_packages is None:
            return SetOfPackages()
        else:
            return {package for package in database.set_of_packages 
                            if self.id in package.shipment_ids
                }
    @set_of_packages.setter
    def set_of_packages(self, new_set_of_packages):
        for package in database.set_of_packages:
            package.shipment_ids.discard(self.id)
        for package in new_set_of_packages:
            package.shipment_ids.add(self.id)
        

    @with_save
    def __setattr__(self, __name: str, value: str) -> None:
        super().__setattr__(__name, value)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


class SetOfSomething(set):

    def __getitem__(self, id: str) -> Union[Package, Shipment]:
        for object in self:
            if object.id == id:
                return object
        raise KeyError("This id does not exist")

    @with_save
    def remove(self, other: Union[str, Union[Package, Shipment]]) -> None:
        if isinstance(other, Shipment) or isinstance(other, Package):
            super().remove(other)
        elif isinstance(other, str):
            for object in self.copy():
                if object.id == other:
                    super().remove(object)
                    return None
            raise KeyError("This id does not exist")
        else:

            raise ValueError("The argument must be a string or a Package/Shipment ")

    @with_save
    def add(self, other: Union[str, Union[Package, Shipment]]):
        super().add(other)

class SetOfPackages(SetOfSomething):

    pass


class SetOfShipments(SetOfSomething):

    pass


class OutBoundShipment(Shipment):
    statuses = ('inbound', 'stocked', 'delivered')

    def __init__(self, departure_date: datetime, expected_arrival_date: datetime, status: str, set_of_packages: SetOfPackages = None, adressee: str = "", sender: str = "", description: str = ""):
        self.departure_date: datetime = departure_date
        self.expected_arrival_date: datetime = expected_arrival_date
        super().__init__(status, set_of_packages, adressee, sender, description)
        self.id = "0" + self.id


class InBoundShipment(Shipment):
    statuses = ('stocked', 'outbound')

    def __init__(self, arrival_date, status: str,set_of_packages: SetOfPackages = None, sender: str = "", adressee: str = "", description: str = ""):
        self.arrival_date: datetime = arrival_date
        super().__init__(status,set_of_packages, adressee, sender, description)
        self.id = "I" + self.id