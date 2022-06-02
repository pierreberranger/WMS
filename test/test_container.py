import unittest

from models import Bundle, Package, SetOfShipments, Shipment, SetOfPackages, SetOfContainers, Container
import pickle_data as database

class TestContainer(unittest.TestCase):

    def setUp(self):
        self.TEST_DATA_FILE = 'testdata'
        database.load(self.TEST_DATA_FILE)
        self.shipment = Shipment(None, None, None, None, "shipment")
        self.shipment2 = Shipment(None, None, None, None, "shipment2")
        self.package1, self.package2, self.package3, self.package4, self.package5 = Package(None, 10, "OK", None, shipment_ids={self.shipment.id}), Package(None, 10, "OK", None, shipment_ids={self.shipment.id, "er"}), Package(None, 10, None, None, shipment_ids={"er"}), Package(None, 15, None, None, shipment_ids=None), Package(None, 10, None, None, shipment_ids=None)
        database.set_of_packages = SetOfPackages([self.package1, self.package2, self.package3, self.package5])
        self.container1 = Container(database.set_of_packages)
        self.container2 = Container(SetOfPackages([self.package4]))
        database.set_of_packages.add(self.package4)
        database.set_of_containers = SetOfContainers([self.container1, self.container2])
        database.set_of_shipments = SetOfShipments([self.shipment, self.shipment2])
        self.bundle = Bundle("transporter", SetOfShipments([self.shipment]), SetOfContainers([self.container1, self.container2]), trip_id=None)

    def test_init(self):
        self.assertEqual(self.package4.container_id, self.container2.id)
        self.assertEqual(self.package1.container_id, self.container1.id)
        self.assertEqual(self.package2.container_id, self.container1.id)
        self.assertEqual(self.package3.container_id, self.container1.id)
        self.assertEqual(self.package5.container_id, self.container1.id)

    def test_eq(self):
        other_container = Container(SetOfPackages([self.package4]))
        self.assertFalse(other_container == self.container2)
        other_container.id = self.container2.id
        self.assertTrue(other_container == self.container2)

    def test_property_set_of_packages(self):
        self.assertEqual(self.container1.set_of_packages, SetOfPackages([self.package1, self.package2, self.package3, self.package5]))
    
    def test_setter_set_of_packages(self):
        self.container2.set_of_packages = SetOfPackages([self.package1, self.package3])
        self.assertEqual(self.container2.set_of_packages, SetOfPackages([self.package1, self.package3]))

    def test_property_weight(self):
        self.assertAlmostEqual(self.container1.weight, self.package1.weight + self.package2.weight + self.package3.weight + self.package5.weight)

    def tearDown(self):
        database.unload()