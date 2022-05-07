from .set_of_packages import SetOfPackages

class Shipment():

    def __init__(self, status: str, id: int, set_of_packages: SetOfPackages, adressee: str, sender: str):
        self.status: str = status
        self.id: int = id
        self.set_of_packages: SetOfPackages = set_of_packages
        self.adressee: str = adressee
        self.sender: str = sender