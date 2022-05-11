from .shipment import Shipment
from .package import Package, packages_ids, Dimensions
import unittest
from .transformation import shipment_to_txt, txt_to_shipment

class TestTransformation (unittest.TestCase) :
      
    def setUp(self):
        self.first_id = next(packages_ids)
        self.database = Shipment( [Package( dimensions=Dimensions(1,2,4), status="shipped", package_type="classic"),
                        Package(dimensions=Dimensions(1,2,3), status="delivered", package_type="classic"),
                        Package(dimensions=Dimensions(1,2,3), status="shipped", package_type="big-bag"),
        ])

    def test_transformation (self) :
        shipment_to_txt(self.database)
        database_transformed = txt_to_shipment()
        for id in range(self.first_id, self.first_id+3) :
            message = f"The transformation of the package {id} is not correct"
            self.assertEqual(self.database[id], database_transformed[id], message)
