from collections import namedtuple 
from itertools import count
from copy import deepcopy # To deepcopy dicts

packageConstructor = namedtuple("package_detail", ["id", "size", "status", "kind"]) # C'est maladroit, en fait un namedtuple c'est quasiment comme une définition de classe.

# suggestion alternative
Package = namedtuple("Package", ["id", "dimensions", "status", "type"]) #il faut se dire que le namedtuple va finir par devenir une classe (probablement) -> l' habitude est de suivre les conventions (voir PEP8) 
Dimensions = namedtuple("Dimensions", "width length height")

package_type = tuple[int, tuple[float, float, float], str, str]
shipment = dict[int, package_type] # on stocke 2 fois l'id ?

# L'id est propre au package ? dans ce cas le dict est superflu : j'ai déjà un id !

# Si je comprends bien le shipment est un ensemble de packages, dans ce cas on peut tout simplement utiliser un set.


shipment = set() # Le set va me donner "gratuitement" une interface explicite que je peux utiliser sans avoir à définir un milliard d'autres fonctions
shipment.add(Package(1234,(1200,800,1000),"In Transit","EURO Pallet")) 


# pas mal le fonctionnel pur :-)
def addPackage(shipment: shipment, available_id_list: list[int], width :float, length: float, height: float, status: str, kind: str) -> tuple[list[int], shipment]:
    """
    Add a package to the shipment
    """
    new_id: int
    new_id_list: list[int]
    new_id, new_id_list = attributeId(available_id_list) # voir les commentaires sur la fonction attributeId plus bas
    new_package: package_type = {new_id: packageConstructor(id=new_id, size=(width, length, height), status=status, kind=kind)}
    new_shipment: shipment = deepcopy(shipment) # Pourquoi une deepcopy ?
    new_shipment[new_id] = new_package
    return new_id_list, new_shipment

def attributeId(available_id_list: list[int]) -> tuple[int, list[int]]:
    """
    Generate a new unique id and updates the list of available ids
    available_id_list[0] is the minimal int such that any other int greater is unused
    """

    # Note ; A la limite c'est même carrément dangereux parce qu'on n'est pas à l'abri de réattribuer un numéro supprimé par le passé.
    
    # Bon là clairement vous vous cassez la tête pour rien !
    # Déjà parce que :
    # return max(ids) + 1
    # Et surtout parce que la manière "pythonic" de faire ça est plutôt d'avoir un generator dont on appelle les valeurs quand on en a besoin...
    # ce qui évitera de se trimbaler une "liste d'ids disponibles" 


    new_ids_list : list[int] = available_id_list.copy()
    last_id : int = new_ids_list.pop()
    match new_ids_list:
        case []:
            return last_id, [last_id + 1]
        case _:
            return last_id, new_ids_list

# Et on a tout ce qu'il faut dans la librairie standard :) 
available_ids = count() # count() renvoie un itérateur qui... compte. Voir Ramalho pour mieux comprendre les itérateurs

# si on veut un nouvel id :

for i in range(10):
    new_never_attributed_before_id = next(available_ids)
    print(new_never_attributed_before_id) 
    # On commence à faire tourner le compteur, comme ça il commencera à 10 plus tard


# Donc ma suggestion pour faire l'équivalent de votre code
def add_package(shipment, dimensions: tuple , status: str, package_type: str) -> set:
    """
    Adds a package to the shipment
    """

    new_id = next(available_ids)
    new_package = Package(new_id,dimensions,status,package_type)
    new_shipment = set(shipment) # Shallow Copy 
    new_shipment.add(new_package)
    return new_shipment

# Exercice : trouver comment (indice : Package deviendrait une vraie classe, qui peut tout à fait hériter de la def de Package en tant que namedtuple !)
# on pourrait automatiser la numérotation des Packages à l'instantiation !