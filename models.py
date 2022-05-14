from collections import namedtuple
from typing import Union
from datetime import datetime
from pickle import load, dump

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
    statuses = ('stored','inbound','outbound','delivered')
    types = ('EPAL','20ISO','OOG')

    def __init__(self, dimensions: Dimensions, status: str, package_type: str, description: str="", shipment_id=None, id=None) -> None:
        self.status = status
        self.dimensions = dimensions
        self.package_type = package_type
        self.shipment_id = shipment_id
        self.description = description
        if id == None:
            self.id = f"P{next(packages_ids)}"
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
        return int("0" + self.id[1:])
    
    def is_same_package(self, other) -> bool:
        return self.dimensions == other.dimensions and self.status == other.status \
                and self.package_type == other.package_type and self.id == other.id

    # Pour modifier un package dans un Shipment à partir de l'id : 
    # shipment[id].status = status

SetOfPackages = set

class Shipment():

    def __init__(self, status: str, set_of_packages: SetOfPackages, adressee: str, sender: str, description: str="", id: int=None):
        self.status: str = status
        self.set_of_packages: SetOfPackages = set_of_packages
        self.adressee: str = adressee
        self.sender: str = sender
        self.description: str = description
        if id == None:
            self.id = f"S{next(shipments_ids)}"
        else:
            self.id = id
        
    def __hash__(self):
        return int("1" + self.id[1:])

class SetOfSomething(set):

    def __getitem__(self, id: str) -> Union[Package, Shipment]:
        for object in self:
            if object.id == id:
                return object
        raise KeyError("This id does not exist")

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
            
            raise ValueError(f"The argument must be a string or a Package/Shipment ")

class SetOfPackages(SetOfSomething):

    pass

class SetOfShipments(SetOfSomething):

    pass



class OutBoundShipment(Shipment):
    statuses = ('inbound','stocked')

    def __init__(self, departure_date: datetime, expected_arrival_date: datetime, status: str, id: int, set_of_packages: SetOfPackages, adressee: str, sender: str=""):
        self.departure_date: datetime = departure_date
        self.expected_arrival_date: datetime = expected_arrival_date
        super().__init__(status, id, set_of_packages, adressee, sender)

class InBoundShipment(Shipment):
    statuses = ('stocked', 'outbound')

    def __init__(self, arrival_date, status: str, id: int, set_of_packages: SetOfPackages, sender: str, adressee: str=""):
        self.arrival_date: datetime = arrival_date
        super().__init__(status, id, set_of_packages, adressee, sender)


class PickleRepository:

    def __init__(self, filepath, set_of_packages, set_of_shipments):
        self.filepath = filepath
        self.set_of_packages = set_of_packages
        self.set_of_shipments = set_of_shipments
    
    def add(self, object : Union[Package, Shipment]):
        if isinstance(object, Package):
            self.set_of_packages.add(object)
        elif isinstance(object, Shipment):
            self.set_of_shipments.add(object)
        
        with open(self.filepath, "wb") as file:
            dump(object, file)
        

    def remove(self, object : Union[Package, Shipment, str]):
        if isinstance(object, Package) or object[0]=="P":
            self.set_of_packages.remove(object)
        elif isinstance(object, Shipment) or object[0]=="S":
            self.set_of_shipments.remove(object)
        else:
            raise TypeError("the given object has to be a Shipment (or Shipment id)/ Package (or Package id)")
        with open(self.filepath, "wb") as file:
            dump(object, file)
        
    def __getitem__(self, id : str):
        if not(isinstance(id, str)):
            raise TypeError("the given object has to be a str Shipment id) or Package id")
        elif id[0]=="P":
            self.set_of_packages[id]
        elif id[0]=="S":
            self.set_of_shipments[id]
        else:
            raise TypeError("the given id has to be a  Shipment id) or Package id")
