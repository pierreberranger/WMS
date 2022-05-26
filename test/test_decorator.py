from tkinter import N
import unittest
from xml.dom import NOT_FOUND_ERR

import pickle_data as data
from models import Shipment, Package, Dimensions, SetOfPackages, SetOfShipments

class TestDecorator(unittest.TestCase):

    def test_add_shipment(self):
        data.load("filename_test.txt")

        shipment = Shipment("status", SetOfPackages(), "adressee", "sender")
        data.shipments = SetOfShipments([shipment])
        shipment.set_of_packages.add(Package(Dimensions(1,2,3), "arrived", "classic", "machin")) 

        data.load("filename_test.txt")
        packages2, shipments2 = data.packages, data.shipments
        self.assertEqual(shipments2, SetOfShipments([shipment]))
        self.assertEqual(packages2, None)

    def tearDown(self):
        data.unload()
