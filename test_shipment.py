import unittest

from shipment import *


class TestPackages(unittest.TestCase):

    def setUp(self) -> None:
        self.available_id_list = [6, 3, 2, 5] # ??? On aurait une liste d'ids possible prédéfinie 
        self.shipment = {0: packageConstructor(id=0, size=(1,2,3), status="shipped", kind="classic"),
                        1: packageConstructor(id=1, size=(1,2,3), status="delivered", kind="classic"),
                        4: packageConstructor(id=4, size=(1,2,3), status="shipped", kind="big-bag"),
                        }

    def test_attributeId(self) -> None:
        # Élégant, mais souvenez-vous : "premature optimization is worse than no optimization"
        # Vous n'économisez pas de mémoire en vous prenant la tête sur la numérotation
        # Et surtout, vous prenez le risque de double numéroter à l'avenir si on supprime des
        # éléments !
        
        l_id_1 = self.available_id_list
        id, new_list = attributeId(l_id_1)
        self.assertTrue(id in l_id_1)
        self.assertTrue(id not in new_list)
        if len(l_id_1) == 1:
            self.assertEqual(new_list, [l_id_1[0] + 1])
        else:
            self.assertEqual(new_list[0], l_id_1[0])

    def test_addPackage(self) -> None:
        width, length, height, status, kind = 1, 2, 3, "refused", "classic"
        initial_shipment = self.shipment
        _, new_shipment = addPackage(initial_shipment, self.available_id_list, width, length, height, status, kind) # Dans ce genre de cas il est d'usage d'utiliser une variable jetable pour clarifier
        new_id = attributeId(self.available_id_list)[0]
        initial_shipment[new_id] = {new_id: packageConstructor(id=new_id, size=(1,2,3), status="refused", kind="classic")}
        self.assertEqual(new_shipment, initial_shipment) # Pourquoi ce [1] ?

    def tearDown(self) -> None:
        pass

class TestPackagesRefactored(unittest.TestCase):
    def setUp(self):
        self.shipment = set([Package(id=0, dimensions=(1,2,3), status="shipped", type="classic"),
                        Package(id=1, dimensions=(1,2,3), status="delivered", type="classic"),
                        Package(id=4, dimensions=(1,2,3), status="shipped", type="big-bag")])

    def test_attribute_id(self):
        attributed_ids = {package.id for package in self.shipment} # set comprehension
        new_id = next(available_ids)
        self.assertTrue(new_id not in attributed_ids)

    def test_add_package(self):
        l = len(self.shipment)

        width, length, height, status, kind = 1, 2, 3, "refused", "classic"
        dims = Dimensions(width,length,height)
        new_shipment = add_package(self.shipment, dims, status, kind)
        
        self.assertEqual(len(new_shipment), l+1) # We added something
        self.assertTrue(all([isinstance(package,Package) for package in new_shipment])) # Everything in the shipment is a package
        self.assertEqual(len({package.id for package in new_shipment}), l+1) # The new id is really new





