from shipment_v2 import Shipment
from package_v2 import *
from csv import reader

def shipment_to_txt(PACKAGE_DATABASE: Shipment(), file="DATA_BASE.csv") -> None :
    with open (file, 'w', newline='') as csvfile :
        csvfile.write("id, width, length, height, status, package_type \n")
        for package in PACKAGE_DATABASE :
            dimensions = package.dimensions
            width = dimensions.width
            length = dimensions.length
            height = dimensions.height
            csvfile.write(f"{package.id}, {width}, {length}, {height}, {package.status}, {package.package_type} \n")

def txt_to_shipment(file="DATA_BASE.csv") -> Shipment :
    PACKAGE_DATABASE = Shipment()
    with open (file, newline='') as csvfile :
        lines_reader = reader(csvfile)
        head = next(lines_reader)
        for package_reader in lines_reader :
            id = int(package_reader[0])
            width = float(package_reader[1])
            length = float(package_reader[2])
            height = float(package_reader[3])
            status = package_reader[4]
            package_type = package_reader[5]
            dimensions = Dimensions(width, length, height)
            new_package = Package(dimensions, status, package_type)
            new_package.id = id
            set_max_id(get_max_id()-1)
            PACKAGE_DATABASE.add(new_package)
    return PACKAGE_DATABASE

""" PACKAGE_DATABASE = Shipment() # À stocker dans un fichier externe

package = Package(Dimensions(100, 55, 25), "delivered", "classic")
PACKAGE_DATABASE.add(package)

shipment_to_txt(PACKAGE_DATABASE)
PACKAGE_DATABASE2 = txt_to_shipment() """