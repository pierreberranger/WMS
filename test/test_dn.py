import unittest
import datetime
import container_optimisation.dn as dn

class TestHarbourDuesCalculationMethods(unittest.TestCase):
	def test_ratio_reduction(self):
		self.assertEqual(dn.ratio_reduction(0.001),0.95)
		self.assertEqual(dn.ratio_reduction(1/40),0.6)
		self.assertEqual(dn.ratio_reduction(1),0)

	def test_frequency_reduction(self):
		self.assertEqual(dn.frequency_reduction(2),0)
		self.assertEqual(dn.frequency_reduction(8),0.1)
		self.assertEqual(dn.frequency_reduction(9),0.1)
		self.assertEqual(dn.frequency_reduction(56),0.7)
		self.assertEqual(dn.frequency_reduction(3),0)

	def test_garbage_tax(self):
		self.assertEqual(dn.garbage_tax(3),94.77)
		self.assertEqual(dn.garbage_tax(7),94.77)
		self.assertEqual(dn.garbage_tax(8),2*94.77)

	def test_days_in_port(self):
		date_1 = datetime.date(day=25,month=2,year=2022)
		date_2 = datetime.date(day=27,month=2,year=2022)
		self.assertEqual(dn.days_in_port(date_1,date_1),1)
		self.assertEqual(dn.days_in_port(date_1,date_2),3)

	def test_layup_days(self):
		date_1 = datetime.date(day=1,month=1,year=2022)
		date_2 = datetime.date(day=2,month=1,year=2022)
		date_3 = datetime.date(day=5,month=1,year=2022)
		date_4 = datetime.date(day=1,month=3,year=2022)

		self.assertEqual(dn.layup_days(date_1,date_2),0)
		self.assertEqual(dn.layup_days(date_1,date_3),2)
		self.assertEqual(dn.layup_days(date_1,date_4),57)
		self.assertRaises(ValueError,dn.layup_days,date_2,date_1)