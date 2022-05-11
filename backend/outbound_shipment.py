from .shipment import Shipment, SetOfPackages
from datetime import datetime

class OutBoundShipment(Shipment):

    def __init__(self, departure_date: datetime, expected_arrival_date: datetime, status: str, id: int, set_of_packages: SetOfPackages, adressee: str, sender: str=""):
        self.departure_date: datetime = departure_date
        self.expected_arrival_date: datetime = expected_arrival_date
        super().__init__(status, id, set_of_packages, adressee, sender)