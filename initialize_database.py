from pickle import dump
from models import *

with open('database.txt', 'wb') as f:
    dump((SetOfPackages(), SetOfShipments), f)