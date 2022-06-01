import pickle

set_of_packages = None
set_of_shipments = None
_file = None

def load(file):
	global set_of_packages
	global set_of_shipments
	global _file
	with open(file, 'rb') as f:
		set_of_packages, set_of_shipments = pickle.load(f)
	_file = file

def unload():
	global set_of_packages
	global set_of_shipments
	global _file

	set_of_packages = None
	set_of_shipments = None
	_file = None


def save(file = None):
	global _file
	global set_of_packages
	global set_of_shipments
	if file is None:
		file = _file
	if file is None:
		raise FileNotFoundError
	with open(file, 'wb') as f:
		pickle.dump((set_of_packages, set_of_shipments), f)

def with_save(func):
	def decorated(self, *args, **kwargs):
		func(self, *args, **kwargs)
		save(_file)
		return None
	return decorated