from datetime import datetime
from pickle import dump
from models import Package, Shipment, ContainerStandard, ContainerPaletWide, Container, Groupage, Trip, TypedSet, DropOff, database, Dimensions

# 'test/testdata'
# 'test/filename_test.txt'
# 'testdata_loading'
# 'database.txt'
database.load("database.txt")

dimensions_euro_palet = Dimensions(120, 80, 10)

set_of_packages2 = TypedSet(Package)

all_dimensions = [Dimensions(110, 80, 10),
    Dimensions(120, 23, 10),
    Dimensions(100, 80, 10),
    Dimensions(200, 80, 10),
    Dimensions(200, 80, 10),
    Dimensions(200, 80, 10),
    Dimensions(200, 80, 10),
    Dimensions(200, 80, 10),
    Dimensions(200, 80, 10),
    Dimensions(105, 80, 10),
    Dimensions(105, 80, 10),
    Dimensions(100, 80, 10),
    Dimensions(200, 106, 10),
    Dimensions(240, 80, 10),
    Dimensions(205, 80, 10),
    Dimensions(220, 80, 10),
    Dimensions(215, 65, 10),
    Dimensions(145, 84, 10),
    Dimensions(200, 106, 10)]

# 19
for i,d in enumerate(all_dimensions):
    set_of_packages2.add(Package(d, 600, 'warehouse', 'OOG', description=f"Book n°{i+1}"))

shipment2 = Shipment('warehouse', set_of_packages2, adressee="Waterstone's Bookshop", description="Books", delivery_date=datetime(2022, 7, 14, 10, 0), departure_date_from_warehouse=datetime(2022, 7, 8))

set_of_packages1 = TypedSet(Package)

shoes = ["Flip-flops", "Baskets", "Sandals", "Boots", "High-heeled shoes"]
for i in range(5):
    set_of_packages1.add(Package(dimensions_euro_palet, 900, 'warehouse', 'EPAL', description= shoes[i]))

shipment1 = Shipment('warehouse', set_of_packages1, adressee="Shoes Shop", description="Shoes", delivery_date=datetime(2022, 7, 15, 10, 0), departure_date_from_warehouse=datetime(2022, 7, 8))


database.set_of_packages = set_of_packages1.union(set_of_packages2)


container1 = ContainerPaletWide()
container2 = ContainerPaletWide()
container3 = ContainerPaletWide()
container4 = ContainerPaletWide()
container5 = ContainerPaletWide()
container6 = ContainerPaletWide()
container7 = ContainerPaletWide()

database.set_of_containers = TypedSet(Container, [container1, container2, container3, container4, container5, container6, container7])

database.set_of_shipments = TypedSet(Shipment, [shipment1, shipment2])

database.save()