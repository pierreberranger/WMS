import unittest

from models import Groupage, Package, Shipment, Container, Trip, TypedSet
import pickle_data as database

class TestTrip(unittest.TestCase):

    def setUp(self):
        self.TEST_DATA_FILE = 'test/testdata'
        database.load(self.TEST_DATA_FILE)
        self.shipment = Shipment(None, None, None, None, "shipment")
        self.shipment2 = Shipment(None, None, None, None, "shipment2")
        self.package1, self.package2, self.package3, self.package4, self.package5 = Package(None, 10, "OK", None), Package(None, 10, "OK", None), Package(None, 10, None, None), Package(None, 15, None, None), Package(None, 10, None, None)
        database.set_of_packages = TypedSet(Package, [self.package1, self.package2, self.package3, self.package5])
        self.container1 = Container(database.set_of_packages)
        self.container2 = Container(TypedSet(Package, [self.package4]))
        database.set_of_packages.add(self.package4)
        database.set_of_containers = TypedSet(Container, [self.container1, self.container2])
        database.set_of_shipments = TypedSet(Shipment, [self.shipment, self.shipment2])
        self.groupage = Groupage("transporter", TypedSet(Shipment, [self.shipment]), TypedSet(Container, [self.container1, self.container2]), trip_id=None)
        self.groupage1 = Groupage(None, TypedSet(Shipment), TypedSet(Container))
        database.set_of_groupages = TypedSet(Groupage, [self.groupage, self.groupage1])
        self.trip1 = Trip(None, TypedSet(Groupage, [self.groupage]))
        self.trip2 = Trip(None, None)
        database.set_of_trips = TypedSet(Trip, [self.trip1, self.trip2])

    def test_init(self):
        self.assertEqual(self.groupage.trip_id, self.trip1.id)

    def test_eq(self):
        other_trip = Trip(None, TypedSet(Groupage, [self.groupage]))
        self.assertFalse(other_trip == self.trip1)
        other_trip.id = self.trip1.id
        self.assertTrue(other_trip == self.trip1)

    def test_property_set_of_groupages(self):
        self.assertEqual(self.trip1.set_of_groupages, TypedSet(Groupage, [self.groupage]))
    
    def test_setter_set_of_groupages(self):
        self.trip1.set_of_groupages = TypedSet(Groupage, [self.groupage])
        self.assertEqual(self.trip1.set_of_groupages, TypedSet(Groupage, [self.groupage]))

    def test_property_set_of_containers(self):
        self.assertEqual(self.trip1.set_of_containers, TypedSet(Container, [self.container1, self.container2]))

    def test_property_weight(self):
        self.assertAlmostEqual(self.trip1.weight, self.groupage.weight)


    def tearDown(self):
        database.unload()