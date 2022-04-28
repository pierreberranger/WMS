from collections import namedtuple

Dimensions = namedtuple("Dimensions", "width length height")

class Package():

    def __init__(self, dimensions, status, package_type) -> None:
        self.status = status
        self.dimensions = dimensions
        self.package_type = package_type
        self.id = Package.new_id()
        
    @classmethod
    def new_id(cls, file: str="backend/MAX_ID.txt"):
        with open(file, mode='r') as file_content:
            max_id = int(file_content.readlines()[0]) + 1
        with open(file, mode='w') as file_content:
            file_content.write(f"{max_id}")
        return max_id

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return self.id

    # Pour modifier un package dans un Shipment à partir de l'id : 
    # shipment[id].status = status