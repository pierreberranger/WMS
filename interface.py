import imp
from models import SetOfPackages, Package, Dimensions, InBoundShipment, Shipment, OutBoundShipment, PickleRepository
""" import numpy as np """
import os
from datetime import datetime
from pickle import load, dump

""" Attention du code est écrit en commentaire car nous n'avons merge les fichiers et les fonctions sont donc encore indisponibles"""

# créer la variable globale
filename = "database.txt"
database : PickleRepository = load(filename) # attention : préciser le fichier dans lequel la datebase est gardée en memoire
# shipment_database = txt_to_set_of_shipments()
# set_of_shipments = set() , a suppirmer car du coup on ne peut pas récupérer les shipment par les id ?

in_out = True
print("Welcome ! \n")
print("This plateform allows you to manage your packages within many actions")
print("If you want to quit, input -quit- \n")


while (in_out) :
    print("\n Actions : quit / package / inBoundShipment / outBoundShipment / view")
    # add_package / delete_package / changestatus_package 
    action = input("On what element do you want to focus on ? ")

    if action ==  "package":
        action2 = input("More precisely : add package [add], delete package [del], or change package status [sta] ")
        if action2 == "add" :
            # Feature
            name = input("Description of the package : ")
            length = float(input("length : "))
            width = float(input("width : "))
            height = float(input("height : "))
            dimensions = Dimensions(length, width, height)
            status = input("status : ")
            package_type = input("package_type : ")
            
            print(f"You entered the package : {name}, {length}, {width}, {height}, {status}, {package_type}")
            sure = input("Do you want to add the package ? [y/n] ")
            
            if sure == "y" :
                new_package = Package(dimensions, status, package_type) 
                database.add(new_package)
            else :
                os.system('clear')
            

        elif action2 == "del" :
            identity = int(input("package id : ")) # attention au cas où aucun id n'est donné : catch error
            answer = input("Are you sure to delete the data ? [y/n]")
            if answer == "y" :
                database.remove(identity) 
            else :
                os.system('clear')

        elif action2 == "sta" :
            identity = int(input("package id : ")) # idem si aucun id
            newstatus = input("Which status do you want to apply ? ")
            print(f"\n You want to change the status of {identity} : {newstatus}")
            answer = input("Do you want to change the status of the package ? [y/n] ")
            if answer == "y" :
                package = database[identity]
                package.status = newstatus
            else :
                os.system('clear')
    
    elif action == "view" :
        print("view of the data base")
    
    elif action == "inBoundShipment" :
        print("Do you to declare a new inshipment (answer : d) or do you want to update an inshipment (answer : u) ?")
        answer = input()
        if answer == "d" :
            arrival_date = datetime.fromisoformat(input("Arrival date (YYYY-MM-DD HH:MM)") + ":00")
            status = "on hold"
            inshipment_packages = SetOfPackages()
            sender = input("Who is the sender of the shipment ? ")
            adressee = input("Who is the adressee of the shipment ? ")

            print("Write the packages below")
            print("If you have a set of the same packages, please declare")
            products_number = input("How many products do you want to declare in the shipment ?")
            for i in range(products_number) :
                quantity = input("The number")
                for j in range(quantity) :
                    # Features
                    name = input("Description of the package : ")
                    length = float(input("length : "))
                    width = float(input("width : "))
                    height = float(input("height : "))
                    dimensions = Dimensions(length, width, height)
                    status = "in transit"
                    package_type = input("package_type : ")
                    print(f"You entered the package : {name}, {length}, {width}, {height}, {status}, {package_type}, {id_inshipment}, {id_outshipment}")
                    sure = input("Do you want to add the package ? [y/n] ")
                    if sure == "y" :
                        new_package = Package(name, dimensions, status, package_type) # np.nan, np.nan
                        database.add(new_package)
                        inshipment_packages.add(new_package)
                    else :
                        os.system('clear') # what does it do ?
            new_inshipment = InBoundShipment(arrival_date, status, id, inshipment_packages, sender, adressee)
            database.add(new_inshipment) #
            #Why not create a set of shipment like with the set of packages ? To have a data base with the shipment
            id_shipment = new_inshipment.id 
            for package in inshipment_packages:
                package.shipment_id = id_shipment

            if answer == "u" :
                print("Your inshipment is arrived.")
                id_inshipment = input("What inshipment do you want to look ?")
                inshipment = database[id_inshipment] # à créer !
                arrival_date = datetime.fromisoformat(input("Arrival date (YYYY-MM-DD HH:MM)") + ":00")
                inshipment.status = "warehouse" 
                inshipment.arrival_date = arrival_date 
                for package in inshipment.set_of_packages : 
                   package.status = "warehouse"

            else :
                print("This option is not known...")
                os.system('clear') # not sure
    
    elif action == "outBoundShipment" :
        print("Do you to declare a new outshipment (answer : d) or do you want to update an outshipment (answer : u) ?")
        answer = input()
        if answer == "d" :
            departure_date = datetime.fromisoformat(input("Departure date (YYYY-MM-DD HH:MM)") + ":00")
            expected_arrival_date = datetime.fromisoformat(input("Expected arrival date (YYYY-MM-DD HH:MM)") + ":00")
            status = "on hold"
            outshipment_packages = SetOfPackages()
            sender = input("Who is the sender of the shipment ? ")
            adressee = input("Who is the adressee of the shipment ? ")
            print("Write the packages below")
            print("If you have a set of the same packages, please declare")
            products_number = input("How many products do you want to declare in the shipment ?")
            for i in range(products_number) :
                quantity = input("The number")
                for j in range(quantity) :
                    # Features
                    id_package = input("What is the id of the package ?")
                    print(f"You entered the package : {id_package}")
                    sure = input("Do you want to add the package to the outshipment ? [y/n] ")
                    if sure == "y" :
                        new_package = database[id_package]
                        new_package.status = "exit"
                        outshipment_packages.add(new_package) 
                    else :
                        os.system('clear') # what does it do ?
            new_outshipment = OutBoundShipment(outshipment_packages, receiver,status, expected_dispatch_date ,dispatch_date, expected_delivery_date, delivery_date) #
            #Why not create a set of shipment like with the set of packages ? To have a data base with the shipment
            database.add(new_outshipment)
            id_shipment = new_outshipment.id 
            for package in outshipment_packages :
               package.shipment_id = id_shipment

            if answer == "u" :
                answer2 = input("Do you want to declare the actual exist of the outshipment [e] or to declare its actual arrival ? [a] ")
                if answer2 =="e":
                    print("Your outshipment is on its way.")
                    id_outshipment = input("What outshipment do you want to look ?")
                    #outshipment = set_of_shipments[id_outshipment] 
                    departure_date = date.fromisoformat(input("What is the departure date ? (YYYY-MM-DD HH:MM)") + ":00")
                    outshipment.status = "sent" 
                    outshipment.departure_date = departure_date 
                    for package in outshipment.set_of_packages:
                       package.status = "sent"

                elif answer2 =="a":
                    print("Your outshipment is arrived to the receiver.")
                    id_outshipment = input("What outshipment do you want to look ?")
                    outshipment = database[id_outshipment]
                    arrival_date = date.fromisoformat(input("What is the arrival date ? (YYYY-MM-DD HH:MM)") + ":00") 
                    outshipment.status = "delivered"
                    outshipment.expected_arrival_date = arrival_date
                    for package in outshipment.set_of_packages :
                       package.status = "delivered"

            else :
                print("This option is not known...")
                os.system('clear') # not sure
    

    elif action == "quit" :
        #save the data in a text file
        with open(filename, "wb") as file :
            dump(file, database)
        in_out = False
    
    else :
        print("The action doesn't exit yet")

""" elif action == "trip" :
        id_trip = int(input("Which trip do you want to look ? "))
        #add a method to see the packages of the trip
        print("trip")
    
    elif action == "status" :
        #view of the packages with the status given
        # we have to define the status we can give to a package
        print("status") 
"""



