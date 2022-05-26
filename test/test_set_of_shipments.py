import unittest
import datetime

from models import SetOfPackages, InBoundShipment, OutBoundShipment, SetOfShipments, shipments_ids, Package, Dimensions, packages_ids
import pickle_data as data

class TestSetOfShipments(unittest.TestCase):

    def setUp(self):
        self.TEST_DATA_FILE = 'testdata'
        data.load(self.TEST_DATA_FILE)
        self.first_id = "S" + str(next(packages_ids) + 1)
        self.database1 = SetOfPackages([Package(dimensions=Dimensions(1, 2, 4), status="shipped", package_type="classic"),
                                        Package(dimensions=Dimensions(
                                            1, 2, 3), status="delivered", package_type="classic"),
                                        Package(dimensions=Dimensions(
                                            1, 2, 3), status="shipped", package_type="big-bag"),
                                        ])
        self.database2 = SetOfPackages([Package(dimensions=Dimensions(3, 4, 5), status="shipped", package_type="classic"),
                                        Package(dimensions=Dimensions(
                                            3, 4, 5), status="delivered", package_type="classic"),
                                        Package(dimensions=Dimensions(
                                            3, 4, 5), status="shipped", package_type="big-bag"),
                                        ])
        self.shipment1 = InBoundShipment(id=next(shipments_ids), arrival_date=datetime.datetime(
            2022, 5, 11, 16, 34), status="coming", set_of_packages=self.database1, sender="Renault", adressee="EntrepotNostos1")
        self.shipment2 = OutBoundShipment(id=next(shipments_ids), departure_date=datetime.datetime(2022, 5, 12, 16, 34), expected_arrival_date=datetime.datetime(
            2022, 5, 11, 16, 34), status="left", set_of_packages=self.database2, sender="EntrepotNostos1", adressee="Jo")
        self.first_shipment_id = "S" + str(next(shipments_ids) - 3)
        self.set_of_shipments = SetOfShipments(
            [self.shipment1, self.shipment2])

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
            self.set_of_shipments.remove("S"+str(next(shipments_ids)))
        self.assertEqual(err.exception.args[0], "This id does not exist")

    def tearDown(self):
        data.unload()