import unittest

from models import Bundle, Package, Shipment, TypedSet, Container
import pickle_data as database

class TestBundle(unittest.TestCase):

    def setUp(self):
        self.TEST_DATA_FILE = 'test/testdata'
        database.load(self.TEST_DATA_FILE)
        self.shipment = Shipment(None, None, None, None, "shipment")
        self.shipment2 = Shipment(None, None, None, None, "shipment2")
        self.package1, self.package2, self.package3, self.package4, self.package5 = Package(None, 10, "OK", None, shipment_ids={self.shipment.id}), Package(None, 10, "OK", None, shipment_ids={self.shipment.id, "er"}), Package(None, 10, None, None, shipment_ids={"er"}), Package(None, 15, None, None, shipment_ids=None), Package(None, 10, None, None, shipment_ids=None)
        database.set_of_packages = TypedSet(Package, [self.package1, self.package2, self.package3, self.package5])
        self.container1 = Container(database.set_of_packages)
        self.container2 = Container(TypedSet(Package, [self.package4]))
        database.set_of_packages.add(self.package4)
        database.set_of_containers = TypedSet(Container, [self.container1, self.container2])
        database.set_of_shipments = TypedSet(Shipment, [self.shipment, self.shipment2])
        self.bundle = Bundle("transporter", TypedSet(Shipment, [self.shipment]), TypedSet(Container, [self.container1, self.container2]), trip_id=None)
    
    def test_init(self):
        self.assertEqual(self.container1.bundle_id, self.bundle.id)
        self.assertEqual(self.container2.bundle_id, self.bundle.id)
        self.assertEqual(self.shipment.bundle_id, self.bundle.id)

    def test_eq(self):
        other_bundle = Bundle("autre_transporter", TypedSet(Shipment, [self.shipment]), trip_id=None)
        self.assertFalse(other_bundle == self.bundle)
        other_bundle.id = self.bundle.id
        self.assertTrue(other_bundle == self.bundle)

    def test_property_set_of_shipments(self):
        self.assertEqual(self.bundle.set_of_shipments, TypedSet(Shipment, [self.shipment]))
    
    def test_setter_set_of_shipments(self):
        self.bundle.set_of_shipments = TypedSet(Shipment, [self.shipment2])
        self.assertEqual(self.bundle.set_of_shipments, TypedSet(Shipment, [self.shipment2]))

    def test_property_set_of_containers(self):
        self.assertEqual(self.bundle.set_of_containers, TypedSet(Container, [self.container1, self.container2]))

    def test_property_weight(self):
        self.assertAlmostEqual(self.bundle.weight, self.container1.weight + self.container2.weight)


    def tearDown(self):
        database.unload()