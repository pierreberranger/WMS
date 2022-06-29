import unittest

from models import TypedSet, Shipment, Package
import pickle_data as database

class TestTypedSet(unittest.TestCase):

    def setUp(self):
        self.TEST_DATA_FILE = 'test/testdata'
        database.load(self.TEST_DATA_FILE)
        self.package = Package(None, None, None, None)
        self.package2 = Package(None, 1, None, None)
        self.shipment = Shipment(None)
        database.set_of_packages.add(self.package)
        database.set_of_packages.add(self.package2)

    def test_cls_constructor(self):
        TypedSet(Package)
        TypedSet(Package, [self.package])
        with self.assertRaises(TypeError) as err:
            TypedSet(Package, [self.shipment])
        self.assertEqual(err.exception.args[0], "Expected type: Package")

    def test_add(self):
        set_of_packages = TypedSet(Package)
        set_of_packages.add(self.package)
        self.assertTrue(self.package in set_of_packages)
        with self.assertRaises(TypeError) as err:
            set_of_packages.add(Shipment(None))
        self.assertEqual(err.exception.args[0], "Expected type: Package")

    def test_remove(self):
        set_of_packages = TypedSet(Package, [self.package])
        set_of_packages.remove(self.package.id)
        with self.assertRaises(KeyError) as err1:
            set_of_packages.remove(self.package.id)
        self.assertEqual(err1.exception.args[0], "This package id does not exist")
        with self.assertRaises(TypeError) as err2:
            set_of_packages.remove(self.shipment.id)
        self.assertEqual(err2.exception.args[0], "Expected id pattern : 'P*'")
        with self.assertRaises(TypeError) as err3:
            set_of_packages.remove(self.shipment)
        self.assertEqual(err3.exception.args[0], "The argument must be a string or a Package")

    def test_get_item(self):
        set_of_packages = TypedSet(Package, [self.package])
        package1 = set_of_packages[self.package.id]
        self.assertEqual(package1, self.package)
        with self.assertRaises(TypeError) as err1:
            set_of_packages[self.shipment.id]
        self.assertEqual(err1.exception.args[0], "Expected id pattern : 'P*'")
        package2 = Package(None, None, None, None)
        with self.assertRaises(KeyError) as err2:
            set_of_packages[package2.id]
        self.assertEqual(err2.exception.args[0], "This package id does not exist")

    def test_union(self):
        set_of_packages = TypedSet(Package, [self.package])
        set_of_shipments = TypedSet(Shipment, [self.shipment])
        with self.assertRaises(TypeError) as err1:
            set_of_packages.union(set_of_shipments)
        self.assertEqual(err1.exception.args[0], "Both TypedSet must be of the same class (Package different from Shipment)")
        set_of_packages2 = TypedSet(Package, [self.package2])
        unioned_packages_sets = set_of_packages.union(set_of_packages2)
        self.assertEqual(unioned_packages_sets, TypedSet(Package, [self.package, self.package2]))
        self.assertEqual(TypedSet(Package).union(), TypedSet(Package))

    def tearDown(self):
        database.unload()