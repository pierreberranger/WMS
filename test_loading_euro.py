from models import Dimensions, Groupage, Package, Shipment, TypedSet, ContainerPaletWide, ContainerStandard, Container

from container_optimisation.container_loading import container_loading, validate_container_loading_proposal
from display import show_fig
import pickle_data as database


TEST_DATA_FILE = 'testdata_loading'
database.load(TEST_DATA_FILE)


dimensions_euro_palet = Dimensions(120, 80, 10)

set_of_packages1 = TypedSet(Package)

for _ in range(10):
    set_of_packages1.add(Package(dimensions_euro_palet, None, None, None))

shipment1 = Shipment(None, set_of_packages1)

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
for d in all_dimensions:
    set_of_packages2.add(Package(d, None, None, None))

database.set_of_packages = set_of_packages1.union(set_of_packages2)

shipment2 = Shipment(None, set_of_packages2)

container1 = ContainerPaletWide()
container2 = ContainerPaletWide()
container3 = ContainerPaletWide()
container4 = ContainerPaletWide()
container5 = ContainerPaletWide()
container6 = ContainerPaletWide()
container7 = ContainerPaletWide()

available_containers_id = set([container1.id, container2.id, container3.id, container4.id, container5.id, container6.id, container7.id])

database.set_of_containers = TypedSet(Container, [container1, container2, container3, container4, container5, container6, container7])

database.set_of_shipments = TypedSet(Shipment, [shipment1, shipment2])

groupage = Groupage("transporter", TypedSet(Shipment, [shipment1, shipment2]))
database.set_of_groupages = TypedSet(Groupage, [groupage])

containers_id, package_placements = container_loading(groupage, available_containers_id)

validate_container_loading_proposal(package_placements)

""" 
for container in database.set_of_containers:
    print(f"\n{container.id=}:")
    set_of_packages(container.set_of_packages) 
"""

show_fig(containers_id, package_placements)