from backend import SetOfPackages, Dimensions, Package, Shipment
from csv import reader

def set_of_packages_to_txt(PACKAGE_DATABASE: SetOfPackages, file="DATA_BASE.csv") -> None :
    with open (file, 'w', newline='') as csvfile :
        csvfile.write("id, width, length, height, status, package_type \n")
        for package in PACKAGE_DATABASE :
            dimensions = package.dimensions
            width = dimensions.width
            length = dimensions.length
            height = dimensions.height
            csvfile.write(f"{package.id}, {width}, {length}, {height}, {package.status}, {package.package_type} \n")

def txt_to_set_of_packages(file="DATA_BASE.csv") -> SetOfPackages :
    package_database = SetOfPackages()
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
            new_package = Package(dimensions, status, package_type, id=id)
            new_package.id = id
            package_database.add(new_package)
    return package_database

""" PACKAGE_DATABASE = Shipment() # À stocker dans un fichier externe

package = Package(Dimensions(100, 55, 25), "delivered", "classic")
PACKAGE_DATABASE.add(package)

shipment_to_txt(PACKAGE_DATABASE)
PACKAGE_DATABASE2 = txt_to_shipment() """