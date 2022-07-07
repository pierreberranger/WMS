import unittest

from models import Package, TypedSet, Shipment
import data.pickle_data as database

class TestShipment(unittest.TestCase):

    def setUp(self):
        self.TEST_DATA_FILE = 'test/testdata'
        database.load(self.TEST_DATA_FILE)
        self.package1, self.package2, self.package3 = Package(None, 10, "OK", None), Package(None, 10, "OK", None), Package(None, 10, None, None)
        self.shipment = Shipment(None, TypedSet(Package, [self.package1, self.package2, self.package3]))
        database.set_of_packages = TypedSet(Package, [self.package1, self.package2, self.package3, Package(None, 10, None, None)])
        database.set_of_shipments = TypedSet(Shipment, [self.shipment])

    def test_eq(self):
        new_shipment = Shipment("shipment1", None, None, None, None,)
        new_shipment2 = Shipment("shipment2", None, None, None, None)
        self.assertFalse(new_shipment == new_shipment2)
        new_shipment2.id = new_shipment.id
        self.assertTrue(new_shipment == new_shipment2)

    def test_property_set_of_packages(self):
        self.assertEqual(self.shipment.set_of_packages, TypedSet(Package, [self.package1, self.package2, self.package3]))
    
    def test_setter_set_of_packages(self):
        self.shipment.set_of_packages = TypedSet(Package, [self.package1, self.package3])
        self.assertEqual(self.shipment.set_of_packages, TypedSet(Package, [self.package1, self.package3]))

    def test_property_weight(self):
        self.shipment.set_of_packages = TypedSet(Package, [self.package1, self.package3])
        self.assertAlmostEqual(self.shipment.weight, self.package1.weight + self.package3.weight)

    def tearDown(self):
        database.unload()