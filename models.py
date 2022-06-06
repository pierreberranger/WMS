from collections import namedtuple
from typing import Type, Union
from datetime import datetime

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
trips_ids = FileIDGenerator("MAX_ID_Trips.txt")


class TypedSet(set):

    def __init__(self, cls, *args):
        self.cls = cls 
        if (not args) or all(self.cls == obj.__class__ for obj in args[0]):
            super().__init__(*args)
        else:
            raise TypeError(f"Expected type: {self.cls_name}")

    @property
    def cls_name(self) -> str:
        return self.cls.__name__

    def __getitem__(self, id: str):
        if id[0] != self.cls_name[0]:
            raise TypeError(f"Expected id pattern : '{self.cls_name[0]}*'")
        for object in self:
            if object.id == id:
                return object
        raise KeyError(f"This {self.cls_name.lower()} id does not exist")

    @with_save
    def remove(self, other) -> None:
        if isinstance(other, self.cls):
            super().remove(other)

        elif isinstance(other, str) and other[0] != self.cls_name[0]:
            raise TypeError(f"Expected id pattern : '{self.cls_name[0]}*'")
        elif isinstance(other, str):
            for object in self.copy():
                if object.id == other:
                    super().remove(object)
                    return None
            raise KeyError(f"This {self.cls_name.lower()} id does not exist")
        
        else:
            raise TypeError(f"The argument must be a string or a {self.cls_name}")

    @with_save
    def add(self, other) -> None:
        if isinstance(other, self.cls):
            super().add(other)
        else:
            raise TypeError(f"Expected type: {self.cls_name}")


class Package():
    statuses = ('inbound', 'warehouse', 'shipbound', 'shipped', 'transporter', 'delivered')
    types = ('EPAL', 'ISO20', 'OOG') # 20ISO Bug quand on crée le namedtuple dans available_choices

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

    def __copy__(self):
        """ package_copy = self.__class__.__new__(self.__class__)
        package_copy = 
        return package_copy """
        pass

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


class Shipment():

    def __init__(self, status: str, set_of_packages: TypedSet = None, adressee: str ="", sender: str = "", 
            description: str = "", bundle_id: int = None, shipment_type: str = ""):
        self.status: str = status
        self.adressee: str = adressee
        self.sender: str = sender
        self.description: str = description
        self.id: str = f"{shipment_type}S{next(shipments_ids)}"
        self.bundle_id: int = bundle_id

    @property
    def set_of_packages(self):
        if database.set_of_packages is None:
            return TypedSet(Package)
        else:
            return TypedSet(Package, (package for package in database.set_of_packages 
                                        if self.id in package.shipment_ids)
                    )
                            
    @set_of_packages.setter
    def set_of_packages(self, new_set_of_packages):
        for package in database.set_of_packages:
            package.shipment_ids.discard(self.id)
        for package in new_set_of_packages:
            package.shipment_ids.add(self.id)

    @property
    def weight(self) -> float:
        return sum(package.weight for package in self.set_of_packages)

    @with_save
    def __setattr__(self, __name: str, value: str) -> None:
        super().__setattr__(__name, value)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


class OutBoundShipment(Shipment):
    statuses = ('outbound', 'warehouse', 'delivered')

    def __init__(self, departure_date: datetime, expected_arrival_date: datetime, status: str, set_of_packages: TypedSet = None, adressee: str = "", sender: str = "", description: str = ""):
        self.departure_date: datetime = departure_date
        self.expected_arrival_date: datetime = expected_arrival_date
        super().__init__(status, set_of_packages, adressee, sender, description, shipment_type="O")


class InBoundShipment(Shipment):
    statuses = ('warehouse', 'inbound')

    def __init__(self, arrival_date, status: str,set_of_packages: TypedSet = None, sender: str = "", adressee: str = "", description: str = ""):
        self.arrival_date: datetime = arrival_date
        super().__init__(status,set_of_packages, adressee, sender, description, shipment_type="I")


class Bundle:

    def __init__(self, transporter: str, set_of_shipments: TypedSet = None, 
            set_of_containers: TypedSet = None, trip_id: int = None) -> None:
        self.id = f"B{next(bundles_ids)}"
        if not(set_of_shipments is None):
            for shipment in set_of_shipments:
                shipment.bundle_id = self.id
        if not(set_of_containers is None):
            for container in set_of_containers:
                container.bundle_id = self.id
        self.transporter = transporter
        self.trip_id = trip_id

    @property
    def set_of_shipments(self) -> TypedSet:
        if database.set_of_shipments is None:
            return TypedSet(Shipment)
        else:
            return TypedSet(Shipment, (shipment for shipment in database.set_of_shipments 
                            if self.id == shipment.bundle_id)
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
    def set_of_containers(self) -> TypedSet:
        if database.set_of_containers is None:
            return TypedSet(Container)
        else:
            return TypedSet(Container, (container for container in database.set_of_containers 
                            if self.id == container.bundle_id)
                )

    @set_of_containers.setter
    def set_of_containers(self, new_set_of_containers):
        for container in database.set_of_containers:
            if container.bundle_id == self.id:
                container.bundle_id = None
            container.bundle_id = None
        for container in new_set_of_containers:
            container.bundle_id = self.id

    @property
    def weight(self) -> float:
        return sum(container.weight for container in self.set_of_containers)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

class Container:
    
    empty_container_weight = 3800

    def __init__(self, set_of_packages: TypedSet = None, bundle_id: int = None) -> None:
        self.id: str = f"C{next(containers_ids)}"
        if not(set_of_packages is None):
            for package in set_of_packages:
                package.container_id = self.id
        self.bundle_id = bundle_id
    
    @property
    def set_of_packages(self) -> TypedSet:
        if database.set_of_packages is None:
            return TypedSet(Package)
        else:
            return TypedSet(Package, (package for package in database.set_of_packages 
                            if self.id == package.container_id)
                )

    @set_of_packages.setter
    def set_of_packages(self, new_set_of_packages):
        for package in database.set_of_packages:
            if package.container_id == self.id:
                package.container_id = None
        for package in new_set_of_packages:
            package.container_id = self.id

    @property
    def weight(self) -> float:
        return sum(package.weight for package in self.set_of_packages) + Container.empty_container_weight

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

class Trip:
    
    def __init__(self, ship_name: str, set_of_bundles: TypedSet = None) -> None:
        self.id: str = f"T{next(trips_ids)}"
        if not(set_of_bundles is None):
            for bundle in set_of_bundles:
                bundle.trip_id = self.id
        self.ship_name = ship_name
    
    @property
    def set_of_bundles(self) -> TypedSet:
        if database.set_of_bundles is None:
            return TypedSet(Bundle)
        else:
            return TypedSet(Bundle, (bundle for bundle in database.set_of_bundles 
                            if self.id == bundle.trip_id)
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
    def set_of_containers(self) -> TypedSet:
        if database.set_of_containers is None:
            return TypedSet(Container)
        else:
            return TypedSet(Container).union(*(bundle.set_of_containers for bundle in self.set_of_bundles))

    @property
    def weight(self) -> float:
        """The weight is in kg"""
        return sum(bundle.weight for bundle in self.set_of_bundles)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id