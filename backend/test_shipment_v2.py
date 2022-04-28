from shipment_v2 import Shipment
from package_v2 import *
import unittest

class TestShipment(unittest.TestCase):
    
    def setUp(self):
        self.first_id = get_max_id() + 1
        self.database = Shipment( [Package( dimensions=Dimensions(1,2,4), status="shipped", package_type="classic"),
                        Package(dimensions=Dimensions(1,2,3), status="delivered", package_type="classic"),
                        Package(dimensions=Dimensions(1,2,3), status="shipped", package_type="big-bag"),
        ])
    

    

    def test_get_item(self):
        package = Package(dimensions=Dimensions(1,2,3), status="delivered", package_type="big-bag")
        package.id = self.first_id
        self.assertEqual(self.database[self.first_id], package)
        with self.assertRaises(KeyError) as err:
            self.database[get_max_id()+1]
        self.assertEqual(err.exception.args[0], "This id does not exist")

    def test_remove(self):
        package_to_remove = self.database[self.first_id]
        self.database.remove_package(self.first_id)
        self.assertFalse(package_to_remove in self.database )
        with self.assertRaises(KeyError) as err:
            self.database.remove_package(get_max_id()+1)
        self.assertEqual(err.exception.args[0], "This id does not exist")

    def test_package_filter(self):
        filter_dict = { "dimensions": [Dimensions(1,2,4)], "package_type": ["classic", "big-bag"] }
        package = Package(dimensions=Dimensions(1,2,4), status="shipped", package_type="classic")
        package.id = self.first_id 
        expected_database = Shipment( [package])
        self.assertEqual(self.database.package_filter(filter_dict), expected_database)




    def tearDown(self):
        set_max_id(self.first_id-1)