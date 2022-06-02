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
bundles_ids = FileIDGenerator("MAX_ID_Bundles.txt")
containers_ids = FileIDGenerator("MAX_ID_Containers.txt")


class Package():
    statuses = ('stored', 'inbound', 'outbound', 'delivered')
    types = ('EPAL', '20ISO', 'OOG')

    def __init__(self, dimensions: Dimensions, weight : float, status: str, package_type: str, description: str = "", 
                    id=None, shipment_ids=None, container_id = None) -> None:
        self.status = status
        self.dimensions = dimensions
        self.weight = weight
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
        self.container_id = container_id

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

    def __init__(self, status: str, set_of_packages: SetOfPackages = None, adressee: str ="", sender: str = "", 
            description: str = "", bundle_id: int = None, shipment_type: str = ""):
        self.status: str = status
        self.adressee: str = adressee
        self.sender: str = sender
        self.description: str = description
        self.id = f"{shipment_type}S{next(shipments_ids)}"
        self.bundle_id: int = bundle_id

    @property
    def set_of_packages(self):
        if database.set_of_packages is None:
            return SetOfPackages()
        else:
            return SetOfPackages(package for package in database.set_of_packages 
                            if self.id in package.shipment_ids
                )
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
    statuses = ('outbound', 'warehouse', 'delivered')

    def __init__(self, departure_date: datetime, expected_arrival_date: datetime, status: str, set_of_packages: SetOfPackages = None, adressee: str = "", sender: str = "", description: str = ""):
        self.departure_date: datetime = departure_date
        self.expected_arrival_date: datetime = expected_arrival_date
        super().__init__(status, set_of_packages, adressee, sender, description, shipment_type="O")
        


class InBoundShipment(Shipment):
    statuses = ('warehouse', 'inbound')

    def __init__(self, arrival_date, status: str,set_of_packages: SetOfPackages = None, sender: str = "", adressee: str = "", description: str = ""):
        self.arrival_date: datetime = arrival_date
        super().__init__(status,set_of_packages, adressee, sender, description, shipment_type="I")

class SetOfContainers(SetOfSomething):
    
    pass

class SetOfBundles(SetOfSomething):
    
    pass

class SetOfTrips(SetOfSomething):
    
    pass

class Bundle:

    def __init__(self, transporter: str, set_of_shipments: SetOfShipments = None, trip_id: int = None) -> None:
        self.id = f"B{next(bundles_ids)}"
        if not(set_of_shipments is None):
            for shipment in set_of_shipments:
                shipment.bundle_id = self.id
        self.transporter = transporter
        self.trip_id = trip_id
    
    @property
    def set_of_shipments(self):
        if database.set_of_shipments is None:
            return SetOfShipments()
        else:
            return SetOfShipments(shipment for shipment in database.set_of_shipments 
                            if self.id == shipment.bundle_id
                )

    @set_of_shipments.setter
    def set_of_shipments(self, new_set_of_shipments):
        for shipment in database.set_of_shipments:
            if shipment.bundle_id == self.id:
                shipment.bundle_id = None
            shipment.bundle_id = None
        for shipment in new_set_of_shipments:
            shipment.bundle_id = self.id

    @property
    def set_of_containers(self):
        if database.set_of_containers is None:
            return SetOfContainers()
        else:
            return SetOfContainers(container for container in database.set_of_containers 
                            if self.id == container.bundle_id
                )

    @set_of_containers.setter
    def set_of_containers(self, new_set_of_containers):
        for container in database.set_of_containers:
            if container.bundle_id == self.id:
                container.bundle_id = None
            container.bundle_id = None
        for container in new_set_of_containers:
            container.bundle_id = self.id


class Container:
    
    def __init__(self, set_of_packages: SetOfPackages = None, bundle_id: int = None) -> None:
        self.id: str = f"C{next(containers_ids)}"
        if not(set_of_packages is None):
            for package in set_of_packages:
                package.container_id = self.id
        self.bundle_id = bundle_id
    
    @property
    def set_of_packages(self):
        if database.set_of_packages is None:
            return SetOfPackages()
        else:
            return SetOfPackages(package for package in database.set_of_packages 
                            if self.id == package.container_id
                )

    @set_of_packages.setter
    def set_of_packages(self, new_set_of_packages):
        for package in database.set_of_packages:
            if package.container_id == self.id:
                package.container_id = None
        for package in new_set_of_packages:
            package.container_id = self.id



class Trip:
    
    def __init__(self, transporter: str, set_of_packages: SetOfPackages = None, trip_id: int = None) -> None:
        self.id: str = f"C{next(containers_ids)}"
        if not(set_of_packages is None):
            for package in set_of_packages:
                package.container_id = self.id
        self.transporter = transporter
    
    @property
    def set_of_bundles(self):
        if database.set_of_bundles is None:
            return SetOfBundles()
        else:
            return SetOfBundles(bundle for bundle in database.set_of_bundles 
                            if self.id == bundle.trip_id
                )

    @set_of_bundles.setter
    def set_of_bundles(self, new_set_of_bundles):
        for bundle in database.set_of_bundles:
            if bundle.trip_id == self.id:
                bundle.trip_id = None
            bundle.trip_id = None
        for bundle in new_set_of_bundles:
            bundle.trip_id = self.id

    @property
    def set_of_containers(self):
        if database.set_of_containers is None:
            return SetOfContainers()
        else:
            return SetOfContainers().union(*(bundle.set_ofcontainers for bundle in self.set_of_bundles))
