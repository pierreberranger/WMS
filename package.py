from collections import namedtuple
from itertools import count

Dimensions = namedtuple("Dimensions", "width length height")
Trip = set

class Package:

    __max_id : count = count()
    __shipment : dict[int] = dict() # compliqué 

    def __init__(self, dimensions, status, package_type):
        self.__dimensions : tuple = dimensions
        self.__status : str = status
        self.__package_type : str = package_type

    @classmethod
    def set_shipment(cls, id_iterator:count=count(), shipment:dict=dict()): #JAMAIS DE MUTABLE DANS LES PARAMETRES PAR DEFAUT D'UNE FONCTION/METHODE OMG
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
    def get_shipment(cls): # ??? pourquoi tout ce bazar avec shipment ? package.shipment fonctionnera très bien
        return cls.__shipment
    
    @classmethod 
    def delete(cls, id: int) -> None: # del package.shipment[id] est très clair...
        try:
            del cls.__shipment[id]
        except KeyError:
            raise KeyError("The shipment does not contain the id")

    def __eq__(self, other): # Si j'ai deux palettes de carrelage, elles sont "égales" ?
        return self.dimensions == other.dimensions and self.status == other.status \
                and self.package_type == other.package_type
    
    def set_status(self, new_status: str) -> None: #Pas besoin de getters/setters en python
        self.status = new_status

    def set_dimensions(self, new_dimensions: Dimensions) -> None:
        self.__dimensions = new_dimensions

    def set_package_type(self, new_package_type: str) -> None:
        self.__package_type = new_package_type

# Définitions des fonctions relatives aux voyages (Trip)

# Je ne comprends pas, vous avex avec Set une interface parfaitement claire, pourquoi l'emballer dans des fonctions qui font une ligne ?
# Quand vous voudrez faire évoluer le truc il sera bien assez tôt pour override les méthodes d'une classe qui hérite de Set !

def add_package_trip(trip: Trip, id: int) -> None:
    trip.add(id)
    
def remove_package_trip(trip: Trip, id: int) -> None:
    try:
        trip.remove(id)
    except KeyError:
        raise KeyError("The trip does not contain this id")
