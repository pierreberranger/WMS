from datetime import datetime
from .shipment import Shipment, SetOfPackages

class InBoundShipment(Shipment):

    def __init__(self, arrival_date, status: str, id: int, set_of_packages: SetOfPackages, sender: str, adressee: str=""):
        self.arrival_date: datetime = arrival_date
        super().__init__(status, id, set_of_packages, adressee, sender)