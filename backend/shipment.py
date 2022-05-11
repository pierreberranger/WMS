from .set_of_packages import SetOfPackages
from .file_id_generator import FileIDGenerator

shipments_ids = FileIDGenerator("MAX_ID_Shipments.txt")


class Shipment():

    def __init__(self, status: str, set_of_packages: SetOfPackages, adressee: str, sender: str, description: str="", id: int=None):
        self.status: str = status
        self.set_of_packages: SetOfPackages = set_of_packages
        self.adressee: str = adressee
        self.sender: str = sender
        if id == None:
            self.id = next(shipments_ids)
        else:
            self.id = id