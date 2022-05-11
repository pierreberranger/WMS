from .set_of_packages import SetOfPackages
from .inbound_shipment import InBoundShipment
from .outbound_shipment import OutBoundShipment
from .set_of_shipments import SetOfShipments, shipments_ids
from .package import Package, Dimensions, packages_ids
from datetime import datetime

import unittest

class TestSetOfShipments(unittest.TestCase):
    
    def setUp(self):
        self.first_id = next(packages_ids) + 1
        self.database1 = SetOfPackages( [Package( dimensions=Dimensions(1,2,4), status="shipped", package_type="classic"),
                        Package(dimensions=Dimensions(1,2,3), status="delivered", package_type="classic"),
                        Package(dimensions=Dimensions(1,2,3), status="shipped", package_type="big-bag"),
        ])
        self.database2 = SetOfPackages( [Package( dimensions=Dimensions(3,4,5), status="shipped", package_type="classic"),
                        Package(dimensions=Dimensions(3,4,5), status="delivered", package_type="classic"),
                        Package(dimensions=Dimensions(3,4,5), status="shipped", package_type="big-bag"),
        ])
        self.shipment1 = InBoundShipment(arrival_date=datetime(2022, 5, 11, 16, 34), status="coming", set_of_packages=self.database1, sender="Renault", adressee="EntrepotNostos1")
        self.shipment2 = OutBoundShipment(departure_date=datetime(2022, 5, 12, 16, 34), status="left", set_of_packages=self.database2, sender="EntrepotNostos1", adressee="Jo")
        self.first_shipment_id = next(shipments_ids) - 3
        self.set_of_shipments = SetOfShipments(self.shipment1, self.shipment2)

    def test_get_item(self):
        shipment_id1 = self.shipment1.id
        self.assertEqual(self.set_of_shipments[shipment_id1], self.shipment1)
        with self.assertRaises(KeyError) as err:
            self.set_of_shipments[next(shipments_ids)]
        self.assertEqual(err.exception.args[0], "This id does not exist")

    def test_remove(self):
        shipment_to_remove = self.set_of_shipments[self.first_shipment_id]
        self.set_of_shipments.remove(self.first_shipment_id)
        self.assertFalse(shipment_to_remove in self.set_of_shipments)
        with self.assertRaises(KeyError) as err:
            self.set_of_shipments.remove(next(shipments_ids))
        self.assertEqual(err.exception.args[0], "This id does not exist")
