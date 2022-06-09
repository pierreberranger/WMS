from pickle import dump
from models import Package, Shipment, Container, Groupage, Trip, TypedSet, DropOff

with open('test/testdata', 'wb') as f:
    dump((TypedSet(Package), TypedSet(DropOff), TypedSet(Shipment), TypedSet(Container),TypedSet(Groupage), TypedSet(Trip)), f)