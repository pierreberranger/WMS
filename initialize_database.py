from pickle import dump
from models import Package, Shipment, Container, Groupage, Trip, TypedSet, DropOff

datafiles = ['test/testdata',
                'test/filename_test.txt',
                'testdata_loading',
                'database.txt',
            ]
    
for file in datafiles:
    with open(file, 'wb') as f:
        dump((TypedSet(Package), 
        TypedSet(DropOff), 
        TypedSet(Shipment), 
        TypedSet(Container),
        TypedSet(Groupage), 
        TypedSet(Trip)), f)