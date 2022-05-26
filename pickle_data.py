import pickle

packages = None
shipments = None
_file = None

def load(file):
	global packages
	global shipments
	global _file
	with open(file, 'rb') as f:
		packages, shipments = pickle.load(f)
	_file = file

def unload():
	global packages
	global shipments
	global _file

	packages = None
	shipments = None
	_file = None


def save(file = None):
	global _file
	global packages
	global shipments
	if file is None:
		file = _file
	if file is None:
		raise FileNotFoundError
	with open(file, 'wb') as f:
		pickle.dump((packages, shipments), f)

def with_save(func):
	def decorated(self, *args):
		func(self, *args)
		save(_file)
		return None
	return decorated