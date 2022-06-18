from pickle import dump
from models import Package, Shipment, Container, Groupage, Trip, TypedSet, DropOff

# 'test/testdata'
# 'test/filename_test.txt'
# 'database.txt'

with open('database.txt', 'wb') as f:
    dump((TypedSet(Package), 
    TypedSet(DropOff), 
    TypedSet(Shipment), 
    TypedSet(Container),
    TypedSet(Groupage), 
    TypedSet(Trip)), f)