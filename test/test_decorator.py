import unittest

import pickle_data as database
from models import Shipment, Package, Dimensions, SetOfPackages, SetOfShipments

class TestDecorator(unittest.TestCase):

    def test_add_shipment(self):
        database.load("filename_test.txt")

        shipment = Shipment("status", SetOfPackages(), "adressee", "sender")
        database.set_of_shipments = SetOfShipments([shipment])
        shipment.set_of_packages.add(Package(Dimensions(1,2,3), "arrived", "classic", "machin")) 

        packages2, shipments2 = database.set_of_packages, database.set_of_shipments
        self.assertEqual(shipments2, SetOfShipments([shipment]))
        self.assertEqual(packages2, SetOfPackages())

    def tearDown(self):
        database.unload()
