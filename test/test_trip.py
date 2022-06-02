import unittest

from models import Bundle, Package, SetOfBundles, SetOfShipments, SetOfTrips, Shipment, SetOfPackages, SetOfContainers, Container, Trip
import pickle_data as database

class TestTrip(unittest.TestCase):

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
        self.bundle1 = Bundle(None, SetOfShipments(), SetOfContainers())
        database.set_of_bundles = SetOfBundles([self.bundle, self.bundle1])
        self.trip1 = Trip(None, SetOfBundles([self.bundle]))
        self.trip2 = Trip(None, None)
        database.set_of_trips = SetOfTrips([self.trip1, self.trip2])

    def test_init(self):
        self.assertEqual(self.bundle.trip_id, self.trip1.id)

    def test_eq(self):
        other_trip = Trip(None, SetOfBundles([self.bundle]))
        self.assertFalse(other_trip == self.trip1)
        other_trip.id = self.trip1.id
        self.assertTrue(other_trip == self.trip1)

    def test_property_set_of_bundles(self):
        self.assertEqual(self.trip1.set_of_bundles, SetOfBundles([self.bundle]))
    
    def test_setter_set_of_bundles(self):
        self.trip1.set_of_bundles = SetOfBundles([self.bundle])
        self.assertEqual(self.trip1.set_of_bundles, SetOfBundles([self.bundle]))

    def test_property_set_of_containers(self):
        self.assertEqual(self.trip1.set_of_containers, SetOfContainers([self.container1, self.container2]))

    def test_property_weight(self):
        self.assertAlmostEqual(self.trip1.weight, self.bundle.weight)


    def tearDown(self):
        database.unload()