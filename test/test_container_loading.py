from models import Dimensions, Groupage, Package, Shipment, TypedSet, ContainerPaletWide, ContainerStandard, Container

from container_optimisation.container_loading import container_loading
from interface.display import show_fig
import data.pickle_data as database


TEST_DATA_FILE = 'testdata_loading'
database.load(TEST_DATA_FILE)


dimensions1 = Dimensions(200, 200, 10)
dimensions2 = Dimensions(220, 240, 10)
dimensions3 = Dimensions(180, 170, 10)
dimensions4 = Dimensions(200, 250, 10)
dimensions5 = Dimensions(200, 200, 10)

package1, package2, package3, package4, package5 = Package(dimensions1, 10, "OK", None), Package(dimensions2, 10, "OK", None), Package(dimensions3, 10, None, None), Package(dimensions4, 15, None, None), Package(dimensions5, 10, None, None)
database.set_of_packages = TypedSet(Package, [package1, package2, package3, package4, package5])

shipment = Shipment(None, TypedSet(Package, [package1, package2, package3]), None, None, "shipment")
shipment2 = Shipment(None, TypedSet(Package, [package4, package5]), None, None, "shipment2")

container1 = ContainerPaletWide()
container2 = ContainerStandard()
container3 = ContainerStandard()
container4 = ContainerStandard()
container5 = ContainerStandard()
container6 = ContainerStandard()
container7 = ContainerStandard()


available_containers_id = set([container1.id, container2.id, container3.id, container4.id, container5.id, container6.id, container7.id])


database.set_of_containers = TypedSet(Container, [container1, container2, container3, container4, container5, container6, container7])
database.set_of_shipments = TypedSet(Shipment, [shipment, shipment2])

groupage = Groupage("transporter", TypedSet(Shipment, [shipment, shipment2]))
database.set_of_groupages = TypedSet(Groupage, [groupage])

containers_id, package_placements = container_loading(groupage, available_containers_id)

show_fig(containers_id, package_placements)