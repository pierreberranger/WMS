from typing import Union
from .shipment import Shipment

class SetOfShipments(set):

    def __getitem__(self, id: int) -> Shipment:
        for shipment in self:
            if shipment.id == id:
                return shipment
        raise KeyError("This id does not exist")

    def remove(self, other: Union[int, Shipment]) -> None:
        if isinstance(other, shipment):
            super().remove(other)
        elif isinstance(other, int):
            for shipment in self.copy():
                if shipment.id == other:
                    super().remove(shipment)
                    return None
            raise KeyError("This id does not exist")
        else:
            
            raise ValueError("The argument must be an int or a Shipment")