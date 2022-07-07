from datetime import datetime
from pickle import dump
from models import Package, Shipment, ContainerStandard, ContainerPaletWide, Container, Groupage, Trip, TypedSet, DropOff, database, Dimensions

# 'test/testdata'
# 'test/filename_test.txt'
# 'testdata_loading'
# 'database.txt'
database.load("data/database.txt")

files = ["MAX_ID_Containers.txt", "MAX_ID_Packages.txt", "MAX_ID_Groupages.txt", "MAX_ID_Shipments.txt", "MAX_ID_Trips.txt", "MAX_ID_DropOffs.txt"]

for file in files:
    with open(f"data/{file}", "w") as f:
        f.write("0")

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


set_of_packages3 = TypedSet(Package)

liquids = ["Coca", "Orangina", "Orange Juice", "Beer", "Wine"]
for i in range(5):
    set_of_packages3.add(Package(dimensions_euro_palet, 900, 'warehouse', 'EPAL', description= liquids[i]))

shipment3 = Shipment('warehouse', set_of_packages3, adressee="Supermarket", description="Liquids", delivery_date=datetime(2022, 7, 15, 10, 0), departure_date_from_warehouse=datetime(2022, 7, 8))
database.set_of_packages = database.set_of_packages.union(set_of_packages3)


container1 = ContainerPaletWide()
container2 = ContainerPaletWide()
container3 = ContainerPaletWide()
container4 = ContainerPaletWide()
container5 = ContainerPaletWide()
container6 = ContainerPaletWide()
container7 = ContainerPaletWide()

database.set_of_containers = TypedSet(Container, [container1, container2, container3, container4, container5, container6, container7])

database.set_of_shipments = TypedSet(Shipment, [shipment1, shipment2, shipment3])

groupage = Groupage("transporter", TypedSet(Shipment, [shipment1]))
groupage2 = Groupage("transporter", TypedSet(Shipment, [shipment2]))

database.set_of_groupages = TypedSet(Groupage, [groupage, groupage2])

trip = Trip("Southern Liner", datetime(2022, 7, 8, 10), set_of_groupages=TypedSet(Groupage, [groupage, groupage2]))

database.set_of_trips.add(trip)

database.save()