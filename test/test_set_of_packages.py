import unittest

from models import SetOfPackages, Package, Dimensions, packages_ids
import pickle_data as data

class TestSetOfPackages(unittest.TestCase):

    def setUp(self):
        self.TEST_DATA_FILE = 'testdata'
        data.load(self.TEST_DATA_FILE)
        self.first_id = "P"+str(next(packages_ids) + 1)
        self.database = SetOfPackages([Package(dimensions=Dimensions(1, 2, 4), weight=10, status="shipped", package_type="classic"),
                                       Package(dimensions=Dimensions(
                                           1, 2, 3), weight=10, status="delivered", package_type="classic"),
                                       Package(dimensions=Dimensions(
                                           1, 2, 3), weight=10, status="shipped", package_type="big-bag"),
                                       ])

    def test_get_item(self):
        package = Package(dimensions=Dimensions(1, 2, 3), weight=10, 
                          status="delivered", package_type="big-bag")
        package.id = self.first_id
        self.assertEqual(self.database[self.first_id], package)
        with self.assertRaises(KeyError) as err:
            self.database[next(packages_ids)]
        self.assertEqual(err.exception.args[0], "This id does not exist")

    def test_remove(self):
        package_to_remove = self.database[self.first_id]
        self.database.remove(self.first_id)
        self.assertFalse(package_to_remove in self.database)
        with self.assertRaises(KeyError) as err:
            self.database.remove("P"+str(next(packages_ids)))
        self.assertEqual(err.exception.args[0], "This id does not exist")

    def tearDown(self):
        data.unload()