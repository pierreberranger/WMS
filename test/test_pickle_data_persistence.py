import unittest

import pickle_data as data
from pickle import dump

from models import Package, Shipment, SetOfPackages, SetOfShipments, SetOfBundles, SetOfContainers, SetOfTrips

TEST_DATA_FILE = 'testdata'

class TestPickleDataPersistence(unittest.TestCase):

	def setUp(self):
		with open(TEST_DATA_FILE, 'wb') as f:
			dump((SetOfPackages(), SetOfShipments(), SetOfContainers(), SetOfBundles(), SetOfTrips()), f)

	def test_load(self):
		self.assertTrue(data.set_of_packages is None)
		self.assertTrue(data.set_of_shipments is None)
		self.assertTrue(data.set_of_bundles is None)
		self.assertTrue(data.set_of_containers is None)
		self.assertTrue(data.set_of_trips is None)


		data.load(TEST_DATA_FILE)
		
		self.assertFalse(data.set_of_packages is None)
		self.assertFalse(data.set_of_shipments is None)
		self.assertFalse(data.set_of_bundles is None)
		self.assertFalse(data.set_of_containers is None)
		self.assertFalse(data.set_of_trips is None)

	def test_unload(self):
		data.load(TEST_DATA_FILE)
		data.unload()

		self.assertTrue(data.set_of_packages is None)
		self.assertTrue(data.set_of_shipments is None)
		self.assertTrue(data.set_of_bundles is None)
		self.assertTrue(data.set_of_containers is None)
		self.assertTrue(data.set_of_trips is None)

	def test_save(self):
		data.load(TEST_DATA_FILE)
		package = Package(None, None, None, None, "ADDED_PACK")
		data.set_of_packages.add(package)
		
		shipment = Shipment(None, None, None, "ADDED_SHIPMENT_SENDER")
		data.set_of_shipments.add(shipment)
		data.save()
		data.unload()
		data.load(TEST_DATA_FILE)

		self.assertTrue(any([package.description == "ADDED_PACK" for package in data.set_of_packages]))
		self.assertTrue(any([shipment.sender == "ADDED_SHIPMENT_SENDER" for shipment in data.set_of_shipments]))