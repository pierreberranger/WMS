from tkinter import Pack
import unittest
from package import *
from itertools import count

class TestPackage(unittest.TestCase):

    def setUp(self):
        shipment = {0: Package(dimensions=(1,2,3), status="shipped", package_type="classic"),
                    1: Package(dimensions=(1,2,3), status="delivered", package_type="classic"),
                    2: Package(dimensions=(1,2,3), status="shipped", package_type="big-bag"),
                    }
        self.package = Package(Dimensions(4, 5, 6), "shipped", "classic")

        Package.set_shipment(count(start=3), shipment=shipment) 
        
    def test_attribute_id(self):
        dimensions, status, package_type = Dimensions(1, 2, 3), "shipped", "classic"
        Package.add_package(dimensions, status, package_type)
        self.assertEqual(list(Package.get_shipment().keys()), [0, 1, 2, 3])

    def test_add_package(self):
        dimensions, status, package_type = Dimensions(4, 5, 6), "shipped", "classic"
        Package.add_package(dimensions, status, package_type)
        shipment = Package.get_shipment()
        self.assertTrue(self.package in shipment.values()) # Ids unicity is tested by test_attribute_id

    def test_delete(self):
        Package.delete(2)
        shipment = Package.get_shipment()
        self.assertEqual(shipment[0], {0: Package(dimensions=(1,2,3), status="shipped", package_type="classic")}[0])
        with self.assertRaises(KeyError) as err:
            Package.delete(2)
        self.assertEqual(err.exception.args[0], "The shipment does not contain the id")

    def test_set_attributs(self):
        dimensions, status, package_type = Dimensions(1, 2, 3), "delivered", "small"
        self.package.set_dimensions(dimensions)
        self.package.set_status(status)
        self.package.set_package_type(package_type)
        package_aimed = Package(dimensions, status, package_type) 
        self.assertEqual(self.package, package_aimed)

class TestTrips(unittest.TestCase):

    def test_add(self):
        trip = {1, 2, 4}
        add_package_trip(trip, 5)
        self.assertEqual(trip, {1, 2, 4, 5})

    def test_remove(self):
        trip = {1, 2, 4}
        remove_package_trip(trip, 2)
        self.assertEqual(trip, {1, 4})
        with self.assertRaises(KeyError) as err:
            remove_package_trip(trip, 2)
        self.assertEqual(err.exception.args[0], "The trip does not contain this id")