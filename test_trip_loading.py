from models import Dimensions, Groupage, Package, Shipment, TypedSet, ContainerPaletWide, ContainerStandard, Container, Trip

from container_optimisation.container_loading import trip_loading, validate_trip_loading_proposal
import pickle_data as database
from service_layer_display import plot_trip_loading_proposal, save_trip_loading_proposal, set_of_containers, set_of_groupages


TEST_DATA_FILE = 'testdata_loading'
database.load(TEST_DATA_FILE)


dimensions_euro_palet = Dimensions(120, 100, 10)

set_of_packages1 = TypedSet(Package)

for _ in range(20):
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

container1 = ContainerStandard()
container2 = ContainerStandard()
container3 = ContainerStandard()
container4 = ContainerStandard()
container5 = ContainerStandard()
container6 = ContainerStandard()
container7 = ContainerStandard()

available_containers_id = set([container1.id, container2.id, container3.id, container4.id, container5.id, container6.id, container7.id])

database.set_of_containers = TypedSet(Container, [container1, container2, container3, container4, container5, container6, container7])

database.set_of_shipments = TypedSet(Shipment, [shipment1, shipment2])

groupage = Groupage("transporter", TypedSet(Shipment, [shipment1]))
groupage2 = Groupage("transporter", TypedSet(Shipment, [shipment2]))

database.set_of_groupages = TypedSet(Groupage, [groupage, groupage2])

trip = Trip("Southern Liner", TypedSet(Groupage, [groupage, groupage2]))

database.set_of_trips.add(trip)

groupage_placements = trip_loading(trip.id, available_containers_id)

validate_trip_loading_proposal(groupage_placements)

plot_trip_loading_proposal(groupage_placements)

save_trip_loading_proposal(groupage_placements, trip.id)

# set_of_groupages(database.set_of_groupages)

""" for g in database.set_of_groupages:
    set_of_containers(g.set_of_containers) """