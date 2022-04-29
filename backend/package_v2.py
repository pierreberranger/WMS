from collections import namedtuple

Dimensions = namedtuple("Dimensions", "width length height")

def get_max_id(file="MAX_ID.txt"):
        with open(file, mode='r') as file_content:
            return int(file_content.readlines()[0]) 
def set_max_id(max_id, file="MAX_ID.txt"):
    with open(file, mode='w') as file_content:
            file_content.write(f"{max_id}")

class Package():

    def __init__(self, dimensions, status, package_type) -> None:
        self.status = status
        self.dimensions = dimensions
        self.package_type = package_type
        self.id = Package.new_id()
    
    

    @classmethod
    def new_id(cls, file: str="MAX_ID.txt"):
        next_id = get_max_id(file=file) +1
        set_max_id(next_id, file=file)
        return next_id

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return self.id
    
    def is_same_package(self, other):
        return self.dimensions == other.dimensions and self.status == other.status \
                and self.package_type == other.package_type and self.id == other.id

    # Pour modifier un package dans un Shipment à partir de l'id : 
    # shipment[id].status = status