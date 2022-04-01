from collections import namedtuple 
from copy import deepcopy # To deepcopy dicts

packageConstructor = namedtuple("package_detail", ["id", "size", "status", "kind"])

package_type = tuple[int, tuple[float, float, float], str, str]
shipment = dict[int, package_type]

def addPackage(shipment: shipment, available_id_list: list[int], width :float, length: float, height: float, status: str, kind: str) -> tuple[list[int], shipment]:
    """
    Add a package to the shipment
    """
    new_id: int
    new_id_list: list[int]
    new_id, new_id_list = attributeId(available_id_list)
    new_package: package_type = {new_id: packageConstructor(id=new_id, size=(width, length, height), status=status, kind=kind)}
    new_shipment: shipment = deepcopy(shipment)
    new_shipment[new_id] = new_package
    return new_id_list, new_shipment

def attributeId(available_id_list: list[int]) -> tuple[int, list[int]]:
    """
    Generate a new unique id and updates the list of available ids
    available_id_list[0] is the minimal int such that any other int greater is unused
    """
    new_ids_list : list[int] = available_id_list.copy()
    last_id : int = new_ids_list.pop()
    match new_ids_list:
        case []:
            return last_id, [last_id + 1]
        case _:
            return last_id, new_ids_list