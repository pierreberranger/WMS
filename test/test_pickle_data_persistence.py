import os
import unittest
import pickle_data as data
from pickle import dump

from models import Package, Shipment, SetOfPackages, SetOfShipments

TEST_DATA_FILE = 'testdata'

class TestPickleDataPersistence(unittest.TestCase):

	def setUp(self):
		with open(TEST_DATA_FILE, 'wb') as f:
			dump((SetOfPackages(), SetOfShipments()), f)

	def test_load(self):
		self.assertTrue(data.packages is None)
		self.assertTrue(data.shipments is None)

		data.load(TEST_DATA_FILE)
		
		self.assertFalse(data.packages is None)
		self.assertFalse(data.shipments is None)

	def test_unload(self):
		data.load(TEST_DATA_FILE)
		data.unload()

		self.assertTrue(data.packages is None)
		self.assertTrue(data.shipments is None)

	def test_save(self):
		data.load(TEST_DATA_FILE)
		package = Package(None, None, None, "ADDED_PACK")
		data.packages.add(package)
		
		shipment = Shipment(None, None, None, "ADDED_SHIPMENT_SENDER")
		data.shipments.add(shipment)
		data.save()
		data.unload()
		data.load(TEST_DATA_FILE)

		self.assertTrue(any([package.description == "ADDED_PACK" for package in data.packages]))
		self.assertTrue(any([shipment.sender == "ADDED_SHIPMENT_SENDER" for shipment in data.shipments]))