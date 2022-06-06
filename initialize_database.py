from pickle import dump
from models import *

with open('test/testdata', 'wb') as f:
    dump((TypedSet(Package), TypedSet(Shipment), TypedSet(Container),TypedSet(Bundle), TypedSet(Trip)), f)