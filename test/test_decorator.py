import unittest

import pickle_data as database
from models import Shipment, Package, Dimensions, TypedSet
class TestDecorator(unittest.TestCase):

    def test_add_shipment(self):
        database.load("test/filename_test.txt")

        shipment = Shipment("status", TypedSet(Package), "adressee", "sender")
        database.set_of_shipments = TypedSet(Shipment, [shipment])
        shipment.set_of_packages.add(Package(Dimensions(1,2,3), "arrived", "classic", "machin")) 

        packages2, shipments2 = database.set_of_packages, database.set_of_shipments
        self.assertEqual(shipments2, TypedSet(Shipment, [shipment]))
        self.assertEqual(packages2, TypedSet(Package))

    def tearDown(self):
        database.unload()
