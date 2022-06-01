import unittest

from models import Package, Dimensions, packages_ids
import pickle_data as data

class TestPackages(unittest.TestCase):

    def setUp(self):
        self.TEST_DATA_FILE = 'testdata'
        data.load(self.TEST_DATA_FILE)

    def test_attribute_id(self):
        dimensions, status, package_type = Dimensions(
            1, 2, 3), "shipped", "classic"
        future_max_id = "P" + str(next(packages_ids) + 1)
        new_package = Package(dimensions, status, package_type)
        self.assertEqual(future_max_id, new_package.id)
        self.assertEqual(future_max_id, "P"+str(next(packages_ids)-1))

    def test_eq(self):
        dimensions, status, package_type = Dimensions(
            1, 2, 3), "shipped", "classic"
        new_package = Package(dimensions, status, package_type)
        new_package2 = Package(Dimensions(2, 2, 2), status, package_type)
        self.assertFalse(new_package == new_package2)
        new_package2.id = new_package.id
        self.assertTrue(new_package == new_package2)

    def test_is_same_shipment(self):
        dimensions, status, package_type = Dimensions(
            1, 2, 3), "shipped", "classic"
        new_package = Package(dimensions, status, package_type)
        new_package2 = Package(dimensions, status, package_type)
        self.assertFalse(new_package.is_same_package(new_package2))
        new_package2.id = new_package.id
        self.assertTrue(new_package.is_same_package(new_package2))
        new_package2.dimensions = Dimensions(2, 2, 2)
        self.assertFalse(new_package.is_same_package(new_package2))

    def tearDown(self):
        data.unload()