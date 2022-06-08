import pickle

set_of_packages = None
set_of_shipments = None
set_of_containers = None
set_of_groupages = None
set_of_trips = None
_file = None

def load(file):
	global set_of_packages
	global set_of_shipments
	global set_of_containers
	global set_of_groupages
	global set_of_trips
	global _file
	with open(file, 'rb') as f:
		set_of_packages, set_of_shipments, set_of_containers, set_of_groupages, set_of_trips = pickle.load(f)
	_file = file

def unload():
	global set_of_packages
	global set_of_shipments
	global set_of_containers
	global set_of_groupages
	global set_of_trips
	global _file

	set_of_packages = None
	set_of_shipments = None
	set_of_containers = None
	set_of_groupages = None
	set_of_trips = None
	_file = None


def save(file = None):
	global _file
	global set_of_packages
	global set_of_shipments
	global set_of_containers
	global set_of_groupages
	global set_of_trips
	
	if file is None:
		file = _file
	if file is None:
		raise FileNotFoundError
	with open(file, 'wb') as f:
		pickle.dump((set_of_packages, set_of_shipments, set_of_containers, set_of_groupages, set_of_trips), f)


def with_save(func):
	def decorated(self, *args, **kwargs):
		func(self, *args, **kwargs)
		save(_file)
		return None
	return decorated