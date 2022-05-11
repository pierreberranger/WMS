from models import SetOfPackages, Dimensions, Package
from csv import reader

# code to be adapted, it is not the last version

def set_of_packages_to_txt(PACKAGE_DATABASE: SetOfPackages, file="DATA_BASE.csv") -> None :
    with open (file, 'w', newline='') as csvfile :
        csvfile.write("id, width, length, height, status, package_type \n")
        for package in PACKAGE_DATABASE :
            width, length, height = package.dimensions
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
            status = package_reader[4].strip()
            package_type = package_reader[5].strip()
            dimensions = Dimensions(width, length, height)
            new_package = Package(dimensions, status, package_type, id=id)
            new_package.id = id
            package_database.add(new_package)
    return package_database

def display_packages(packages: SetOfPackages):
    base = "{:<10}|{:<25}|{:<10}"
    header = base.format('id','description','status')
    print(header)
    print ('='*len(header))
    for package in packages:
        print(base.format(package.id, package.description, package.status))



""" PACKAGE_DATABASE = Shipment() # À stocker dans un fichier externe

package = Package(Dimensions(100, 55, 25), "delivered", "classic")
PACKAGE_DATABASE.add(package)

shipment_to_txt(PACKAGE_DATABASE)
PACKAGE_DATABASE2 = txt_to_shipment() """