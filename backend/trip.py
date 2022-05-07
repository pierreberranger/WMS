from collections import namedtuple
from .shipment import Shipment
from collections import namedtuple

StopoverInfo = namedtuple("StopoverInfo", "time location")

class Trip(Shipment):
    
    def __init__(self, departure: StopoverInfo, arrival: StopoverInfo, transporter_id: int):
        self.departure = departure
        self.arrival = arrival
        self.transporter_id = transporter_id