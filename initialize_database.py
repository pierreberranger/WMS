from pickle import dump
from models import Package, Shipment, Container, Groupage, Trip, TypedSet

with open('test/filename_test.txt', 'wb') as f:
    dump((TypedSet(Package), TypedSet(Shipment), TypedSet(Container),TypedSet(Groupage), TypedSet(Trip)), f)