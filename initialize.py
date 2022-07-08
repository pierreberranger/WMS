from pickle import dump
import os, shutil
from models import Package, Shipment, Container, Groupage, Trip, TypedSet, DropOff
path = "output/trips"
files = ["MAX_ID_Containers.txt", "MAX_ID_Packages.txt", "MAX_ID_Groupages.txt", "MAX_ID_Shipments.txt", "MAX_ID_Trips.txt", "MAX_ID_DropOffs.txt"]


datafiles = ['test/testdata',
                'test/filename_test.txt',
                'test/testdata_loading',
                'data/database.txt',
            ]

for file in files:
    with open(f"data/{file}", "w") as f:
        f.write("0")
for file in datafiles:
    with open(file, 'wb') as f:
        dump((TypedSet(Package), 
        TypedSet(DropOff), 
        TypedSet(Shipment), 
        TypedSet(Container),
        TypedSet(Groupage), 
        TypedSet(Trip)), f)

for folder in os.listdir(path):
    if folder[0] != "." :  #folder not hidden
        shutil.rmtree(f"{path}/{folder}")