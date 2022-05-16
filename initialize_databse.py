from pickle import dump, load

from models import PickleRepository, SetOfPackages, SetOfShipments

with open("database.txt", 'wb') as file:
    dump(PickleRepository("database.txt", SetOfPackages(), SetOfShipments()), file)