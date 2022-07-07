import unittest

import data.pickle_data as database
from pickle import dump

from models import Package, Shipment, TypedSet, Container, Groupage, Trip, DropOff

TEST_DATA_FILE = 'test/testdata'

class TestPickleDataPersistence(unittest.TestCase):

	def setUp(self):
		with open(TEST_DATA_FILE, 'wb') as f:
			dump((TypedSet(Package), TypedSet(DropOff), TypedSet(Shipment), TypedSet(Container),TypedSet(Groupage), TypedSet(Trip)), f)

	def test_load(self):
		self.assertTrue(database.set_of_packages is None)
		self.assertTrue(database.set_of_dropoffs is None)
		self.assertTrue(database.set_of_shipments is None)
		self.assertTrue(database.set_of_groupages is None)
		self.assertTrue(database.set_of_containers is None)
		self.assertTrue(database.set_of_trips is None)


		database.load(TEST_DATA_FILE)
		
		self.assertFalse(database.set_of_packages is None)
		self.assertFalse(database.set_of_dropoffs is None)
		self.assertFalse(database.set_of_shipments is None)
		self.assertFalse(database.set_of_groupages is None)
		self.assertFalse(database.set_of_containers is None)
		self.assertFalse(database.set_of_trips is None)

	def test_unload(self):
		database.load(TEST_DATA_FILE)
		database.unload()

		self.assertTrue(database.set_of_packages is None)
		self.assertTrue(database.set_of_dropoffs is None)
		self.assertTrue(database.set_of_shipments is None)
		self.assertTrue(database.set_of_groupages is None)
		self.assertTrue(database.set_of_containers is None)
		self.assertTrue(database.set_of_trips is None)

	def test_save(self):
		database.load(TEST_DATA_FILE)
		package = Package(None, None, None, None, description="ADDED_PACK")
		database.set_of_packages.add(package)
	
		shipment = Shipment(None, None, description="ADDED_SHIPMENT_SENDER")
		database.set_of_shipments.add(shipment)
		database.save()
		database.unload()
		database.load(TEST_DATA_FILE)
		self.assertTrue(any([package.description == "ADDED_PACK" for package in database.set_of_packages]))
		self.assertTrue(any([shipment.description == "ADDED_SHIPMENT_SENDER" for shipment in database.set_of_shipments]))