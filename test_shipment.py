import unittest

from shipment import addPackage, attributeId, packageConstructor


class TestPackages(unittest.TestCase):

    def setUp(self) -> None:
        self.available_id_list = [6, 3, 2, 5]
        self.shipment = {0: packageConstructor(id=0, size=(1,2,3), status="shipped", kind="classic"),
                        1: packageConstructor(id=1, size=(1,2,3), status="delivered", kind="classic"),
                        4: packageConstructor(id=4, size=(1,2,3), status="shipped", kind="big-bag"),
                        }

    def test_attributeId(self) -> None:
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
        new_shipment = addPackage(initial_shipment, self.available_id_list, width, length, height, status, kind)
        new_id = attributeId(self.available_id_list)[0]
        initial_shipment[new_id] = {new_id: packageConstructor(id=new_id, size=(1,2,3), status="refused", kind="classic")}
        self.assertEqual(new_shipment[1], initial_shipment)

    def tearDown(self) -> None:
        pass

