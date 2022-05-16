import pickle
from models import PickleRepository, SetOfPackages, SetOfShipments

with open("database.txt", "wb") as file:
    pickle.dump(PickleRepository("database.txt",
                SetOfPackages(), SetOfShipments()), file)
