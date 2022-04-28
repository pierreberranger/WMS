from backend import Package, Shipment, Trip
from package import Dimensions

PACKAGE_DATABASE = Shipment() # À stocker dans un fichier externe

package = Package(Dimensions(100, 55, 25), "delivered", "classic")
PACKAGE_DATABASE.add(package)

print(PACKAGE_DATABASE)
# if __name__ == '__main__':