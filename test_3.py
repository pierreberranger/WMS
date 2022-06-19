from models import Dimensions, Groupage, Package, Shipment, TypedSet, ContainerPaletWide, ContainerStandard, Container

from container_optimisation.container_loading import container_loading, plot_container_load_output
import pickle_data as database


import random

TEST_DATA_FILE = 'testdata_loading'
database.load(TEST_DATA_FILE)

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

""" Dimensions(110, 80, 10)
Dimensions(120, 23, 10)
Dimensions(100, 80, 10)
Dimensions(200, 80, 10)
Dimensions(200, 80, 10)
Dimensions(200, 80, 10)
Dimensions(200, 80, 10)
Dimensions(200, 80, 10)
Dimensions(200, 80, 10)
Dimensions(105, 80, 10)
Dimensions(105, 80, 10)
Dimensions(100, 80, 10)
Dimensions(200, 106, 10)
Dimensions(240, 80, 10)
Dimensions(205, 80, 10)
Dimensions(220, 80, 10)
dimensions10 = Dimensions(215, 65, 10)
dimensions11 = Dimensions(145, 84, 10)
dimensions12 = Dimensions(200, 106, 10) """

set_of_packages = TypedSet(Package)

# 19
for d in all_dimensions:
    set_of_packages.add(Package(d, None, None, None))

database.set_of_packages = set_of_packages

shipment = Shipment(None, set_of_packages, None, None, "shipment")

container1 = ContainerPaletWide()
container2 = ContainerStandard()
container3 = ContainerStandard()
container4 = ContainerStandard()
container5 = ContainerStandard()
container6 = ContainerStandard()
container7 = ContainerStandard()

available_containers_id = set([container1.id, container2.id, container3.id, container4.id, container5.id, container6.id, container7.id])

database.set_of_containers = TypedSet(Container, [container1, container2, container3, container4, container5, container6, container7])
database.set_of_shipments = TypedSet(Shipment, [shipment])

groupage = Groupage("transporter", TypedSet(Shipment, [shipment]))
database.set_of_groupages = TypedSet(Groupage, [groupage])

containers_id, package_placements = container_loading(groupage, available_containers_id)

plot_container_load_output(containers_id, package_placements)