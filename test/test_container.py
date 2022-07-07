import unittest

from models import Groupage, Package, Shipment, TypedSet, Container
import data.pickle_data as database

class TestContainer(unittest.TestCase):

    def setUp(self):
        self.TEST_DATA_FILE = 'test/testdata'
        database.load(self.TEST_DATA_FILE)
        self.shipment = Shipment("shipment", None, None, None, None)
        self.shipment2 = Shipment("shipment2", None, None, None, None)
        self.package1, self.package2, self.package3, self.package4, self.package5 = Package(None, 10, "OK", None), Package(None, 10, "OK", None), Package(None, 10, None, None), Package(None, 15, None, None), Package(None, 10, None, None)
        database.set_of_packages = TypedSet(Package, [self.package1, self.package2, self.package3, self.package5])
        self.container1 = Container(database.set_of_packages)
        self.container2 = Container(TypedSet(Package, [self.package4]))
        database.set_of_packages.add(self.package4)
        database.set_of_containers = TypedSet(Container, [self.container1, self.container2])
        database.set_of_shipments = TypedSet(Shipment, [self.shipment, self.shipment2])
        self.groupage = Groupage("transporter", TypedSet(Shipment, [self.shipment]), TypedSet(Container, [self.container1, self.container2]), trip_id=None)
    
    def test_init(self):
        self.assertEqual(self.package4.container_id, self.container2.id)
        self.assertEqual(self.package1.container_id, self.container1.id)
        self.assertEqual(self.package2.container_id, self.container1.id)
        self.assertEqual(self.package3.container_id, self.container1.id)
        self.assertEqual(self.package5.container_id, self.container1.id)

    def test_eq(self):
        other_container = Container(TypedSet(Package, [self.package4]))
        self.assertFalse(other_container == self.container2)
        other_container.id = self.container2.id
        self.assertTrue(other_container == self.container2)

    def test_property_set_of_packages(self):
        self.assertEqual(self.container1.set_of_packages, TypedSet(Package, [self.package1, self.package2, self.package3, self.package5]))
    
    def test_setter_set_of_packages(self):
        self.container2.set_of_packages = TypedSet(Package, [self.package1, self.package3])
        self.assertEqual(self.container2.set_of_packages, TypedSet(Package, [self.package1, self.package3]))

    def test_property_weight(self):
        self.assertAlmostEqual(self.container1.weight, self.container1.tare_weight + self.package1.weight + self.package2.weight + self.package3.weight + self.package5.weight)

    def tearDown(self):
        database.unload()