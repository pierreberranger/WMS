import unittest

import data.pickle_data as database
from models import Dimensions, Package
from container_optimisation.container_opti import define_positions, package_extrema 


class TestOptimisation(unittest.TestCase):

    def setUp(self) -> None:
        self.package1 = Package(Dimensions(1, 2, 1), None, None, None)
        self.package2 = Package(Dimensions(1, 0.7, 1), None, None, None)
        self.package3 = Package(Dimensions(1, 1.1, 1), None, None, None)
        self.package4 = Package(Dimensions(1, 0.9, 1), None, None, None)
        self.package5 = Package(Dimensions(1, 0.9, 1), None, None, None)
        self.package6 = Package(Dimensions(1, 1.5, 1), None, None, None)
        self.package7 = Package(Dimensions(1, 1.5, 1), None, None, None)

    def test_optimisation2D_pos(self):
        args = {0: [self.package1.id], 1: [self.package2.id, self.package3.id], 2: [self.package4.id, self.package5.id, self.package6.id], 3: [self.package7.id]}
        res = define_positions(args)

        for id_to_check, priority_to_check, x, y, is_turned in res:
            package_to_check: Package = database.set_of_packages[other_id]
            x_length, y_length = package_extrema(package_to_check, is_turned)
            for other_id, other_priority, other_x, other_y, other_is_turned in res:
                if other_priority < priority_to_check:
                    other_package: Package = database.set_of_packages[other_id]
                    other_x_length, other_y_length = package_extrema(other_package, other_is_turned)

    def test_opti_1D(self):
        args = {0: [self.package1.id], 1: [self.package3.id, self.package2.id], 2: [self.package6.id, self.package4.id, self.package5.id], 3: [self.package7.id]}
        res = define_positions(args)

        self.assertAlmostEqual(res, [(self.package1.id, 0, 0, 0, False),
                                    (self.package2.id, 0, 2, 0, False), 
                                    (self.package3.id, 1, 0, 0, False), 
                                    (self.package4.id, 1, 1.1, 0, False), 
                                    (self.package5.id, 1, 2, 0, False), 
                                    (self.package6.id, 2, 0, 0, False), 
                                    (self.package7.id, 2, 1.5, 0, False), 
            ]
        )