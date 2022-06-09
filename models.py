from collections import namedtuple
from datetime import datetime
from copy import deepcopy

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
dropoff_ids = FileIDGenerator("MAX_ID_DropOffs.txt")
groupages_ids = FileIDGenerator("MAX_ID_Groupages.txt")
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

    def __reduce__(self):
        return (self.__class__, (self.cls, super().__reduce__()[1][0])) # On récupère [x for x in self]

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
                    id: str = None, dropoff_id: str = None, shipment_id: str = None, container_id: str = None) -> None:
        self.status = status
        self.dimensions = dimensions
        self.weight = weight
        self.package_type = package_type
        self.shipment_id = shipment_id
        self.description = description
        if id is None:
            self.id = f"P{next(packages_ids)}"
        else:
            self.id = id
        self.container_id = container_id
        self.dropoff_id = dropoff_id

    def __deepcopy__(self, memo=None):
        new_dict = deepcopy(self.__dict__, memo)
        del new_dict["id"]
        del new_dict["shipment_id"]
        del new_dict["dropoff_id"]
        del new_dict["container_id"]
        print(new_dict)
        return Package(**new_dict)

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
    statuses = ('inbound', 'warehouse', 'outbound', 'delivered')

    def __init__(self, status: str, set_of_packages: TypedSet = None, adressee: str ="", departure_date_from_warehouse: datetime = None, 
            delivery_date: datetime = None, description: str = "", groupage_id: int = None):
        self.status: str = status
        self.adressee: str = adressee
        self.description: str = description
        self.id: str = f"S{next(shipments_ids)}"
        self.groupage_id: int = groupage_id
        self.departure_date_from_warehouse: datetime = departure_date_from_warehouse
        self.delivery_date: datetime = delivery_date
        if not(set_of_packages is None):
            for package in set_of_packages:
                package.shipment_id = self.id

    @property
    def set_of_packages(self):
        if database.set_of_packages is None:
            return TypedSet(Package)
        else:
            return TypedSet(Package, [package for package in database.set_of_packages 
                                        if self.id == package.shipment_id]
                    )
                            
    @set_of_packages.setter
    def set_of_packages(self, new_set_of_packages) -> None:
        for package in database.set_of_packages:
            package.shipment_id = None
        for package in new_set_of_packages:
            package.shipment_id = self.id

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


class DropOff:
    statuses = ('inbound', 'warehouse')

    def __init__(self, status: str, sender:str, set_of_packages: TypedSet = None, 
                    arrival_date: datetime = None, description: str = ""):
        self.status = status
        self.sender = sender
        self.arrival_date: datetime = arrival_date
        self.description: str = description
        self.id: str = f"D{next(dropoff_ids)}"
        if not(set_of_packages is None):
            for package in set_of_packages:
                package.dropoff_id = self.id

    @property
    def set_of_packages(self):
        if database.set_of_packages is None:
            return TypedSet(Package)
        else:
            return TypedSet(Package, [package for package in database.set_of_packages 
                                        if self.id == package.dropoff_id]
                    )
                            
    @set_of_packages.setter
    def set_of_packages(self, new_set_of_packages):
        for package in database.set_of_packages:
            package.dropoff_id = None
        for package in new_set_of_packages:
            package.dropoff_id = self.id

    @with_save
    def __setattr__(self, __name: str, value: str) -> None:
        super().__setattr__(__name, value)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

class Groupage:

    def __init__(self, freight_forwarder: str, set_of_shipments: TypedSet = None, 
            set_of_containers: TypedSet = None, trip_id: int = None) -> None:
        self.id = f"B{next(groupages_ids)}"
        if not(set_of_shipments is None):
            for shipment in set_of_shipments:
                shipment.groupage_id = self.id
        if not(set_of_containers is None):
            for container in set_of_containers:
                container.groupage_id = self.id
        self.freight_forwarder = freight_forwarder
        self.trip_id = trip_id

    @property
    def set_of_shipments(self) -> TypedSet:
        if database.set_of_shipments is None:
            return TypedSet(Shipment)
        else:
            return TypedSet(Shipment, [shipment for shipment in database.set_of_shipments 
                            if self.id == shipment.groupage_id]
                )

    @set_of_shipments.setter
    def set_of_shipments(self, new_set_of_shipments):
        for shipment in database.set_of_shipments:
            if shipment.groupage_id == self.id:
                shipment.groupage_id = None
            shipment.groupage_id = None
        for shipment in new_set_of_shipments:
            shipment.groupage_id = self.id

    @property
    def set_of_containers(self) -> TypedSet:
        if database.set_of_containers is None:
            return TypedSet(Container)
        else:
            return TypedSet(Container, [container for container in database.set_of_containers 
                            if self.id == container.groupage_id]
                )

    @set_of_containers.setter
    def set_of_containers(self, new_set_of_containers):
        for container in database.set_of_containers:
            if container.groupage_id == self.id:
                container.groupage_id = None
            container.groupage_id = None
        for container in new_set_of_containers:
            container.groupage_id = self.id

    @property
    def weight(self) -> float:
        return sum(container.weight for container in self.set_of_containers)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

class Container:
    
    empty_container_weight = 3800

    def __init__(self, set_of_packages: TypedSet = None, groupage_id: int = None) -> None:
        self.id: str = f"C{next(containers_ids)}"
        if not(set_of_packages is None):
            for package in set_of_packages:
                package.container_id = self.id
        self.groupage_id = groupage_id
    
    @property
    def set_of_packages(self) -> TypedSet:
        if database.set_of_packages is None:
            return TypedSet(Package)
        else:
            return TypedSet(Package, [package for package in database.set_of_packages 
                            if self.id == package.container_id]
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
    
    def __init__(self, ship_name: str, set_of_groupages: TypedSet = None) -> None:
        self.id: str = f"T{next(trips_ids)}"
        if not(set_of_groupages is None):
            for groupage in set_of_groupages:
                groupage.trip_id = self.id
        self.ship_name = ship_name
    
    @property
    def set_of_groupages(self) -> TypedSet:
        if database.set_of_groupages is None:
            return TypedSet(Groupage)
        else:
            return TypedSet(Groupage, [groupage for groupage in database.set_of_groupages 
                            if self.id == groupage.trip_id]
                )

    @set_of_groupages.setter
    def set_of_groupages(self, new_set_of_groupages):
        for groupage in database.set_of_groupages:
            if groupage.trip_id == self.id:
                groupage.trip_id = None
            groupage.trip_id = None
        for groupage in new_set_of_groupages:
            groupage.trip_id = self.id

    @property
    def set_of_containers(self) -> TypedSet:
        if database.set_of_containers is None:
            return TypedSet(Container)
        else:
            return TypedSet(Container).union(*(groupage.set_of_containers for groupage in self.set_of_groupages))

    @property
    def weight(self) -> float:
        """The weight is in kg"""
        return sum(groupage.weight for groupage in self.set_of_groupages)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id