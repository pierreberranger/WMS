from backend import SetOfPackages, Package, Dimensions, InBoundShipment, Shipment, OutBoundShipment, set_of_packages_to_txt, txt_to_set_of_packages
import numpy as np
import os
from datetime import date

""" Attention du code est écrit en commentaire car nous n'avons merge les fichiers et les fonctions sont donc encore indisponibles"""

# créer la variable globale
package_database = txt_to_set_of_packages()
set_of_shipments = set()

in_out = True
print("Welcome ! \n")
print("This plateform allows you to manage your packages within many actions")
print("If you want to quit, input -quit- \n")


while (in_out) :
    print("\n Actions : quit / add_package / delete_package / changestatus_package / inshipment / outshipment / view")
    action = input("Which action do you want to use ? ")

    if action == "add_package" :
        # Features
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
            new_package = Package(name, dimensions, status, package_type) #
            package_database.add(new_package) #
            ...
        else :
            os.system('clear')
        

    elif action == "delete_package" :
        identity = int(input("package id : "))
        answer = input("Are you sure to delete the data ? [y/n]")
        if answer == "y" :
            ...
            package_database.remove(identity) #
        else :
            os.system('clear')

    elif action == "changestatus_package" :
        identity = int(input("package id : "))
        newstatus = input("Which status do you want to apply ? ")
        print(f"\n You want to change the status of {identity} : {newstatus}")
        answer = input("Do you want to change the status of the package ? [y/n] ")
        if answer == "y" :
            ...
            package = package_database[identity] #
            package.status = newstatus #
        else :
            os.system('clear')
    
    elif action == "view" :
        print("view of the data base")
    
    elif action == "inshipment" :
        print("Do you to declare a new inshipment (answer : d) or do you want to update an inshipment (answer : u) ?")
        answer = input()
        if answer == "d" :
            print("Write the packages below")
            print("If you have a set of the same packages, please declare")
            products_number = input("How many products do you want to declare in the shipment ?")
            inshipment_packages = InBoundShipment() #
            for i in range(products_number) :
                quantity = input("The number")
                for j in range(quantity) :
                    # Features
                    name = input("Description of the package : ")
                    length = float(input("length : "))
                    width = float(input("width : "))
                    height = float(input("height : "))
                    dimensions = Dimensions(length, width, height) #
                    status = "on hold for inshipment"
                    package_type = input("package_type : ")
                    id_inshipment = None
                    id_outshipment = None
                    print(f"You entered the package : {name}, {length}, {width}, {height}, {status}, {package_type}, {id_inshipment}, {id_outshipment}")
                    sure = input("Do you want to add the package ? [y/n] ")
                    if sure == "y" :
                        new_package = Package(name, dimensions, status, package_type, np.nan, np.nan) #
                        package_database.add(new_package)
                        inshipment_packages.set_of_packages.add(new_package)
                        ...
                    else :
                        os.system('clear') # what does it do ?
            sender = input("Who is the sender of the shipment ? ")
            dispatch_date = date.fromisoformat(input("Dispatch date (YYYY-MM-DD)"))
            expected_delivery_date = date.fromisoformat(input("Expected delivery date (YYYY-MM-DD)"))
            status = "on hold"
            new_inshipment = InBoundShipment(inshipment_packages, sender,status, dispatch_date, expected_delivery_date, status, delivery_date=None) #
            #Why not create a set of shipment like with the set of packages ? To have a data base with the shipment
            id_shipment = new_inshipment.id #
            for package in inshipment_packages.set_of_packages : #
                package.shipment_id = id_shipment #
            if answer == "u" :
                print("Your inshipment is arrived.")
                id_inshipment = input("What inshipment do you want to look ?")
                inshipment = set_of_shipments[id_inshipment] #
                recieved_date = date.fromisoformat(input("What is the date ? YYYY-MM-DD "))
                inshipment.status = "warehouse" #
                inshipment.arrival_date = recieved_date #
                for package in inshipment.set_of_packages : #
                   package.status = "warehouse" #

            else :
                print("This option is not known...")
                os.system('clear') # not sure
    
    elif action == "outshipment" :
        print("Do you to declare a new outshipment (answer : d) or do you want to update an outshipment (answer : u) ?")
        answer = input()
        if answer == "d" :
            print("Write the packages below")
            print("If you have a set of the same packages, please declare")
            products_number = input("How many products do you want to declare in the shipment ?")
            outshipment_packages = OutBoundShipment() #
            for i in range(products_number) :
                quantity = input("The number")
                for j in range(quantity) :
                    # Features
                    id_package = input("What is the id of the package ?")
                    print(f"You entered the package : {id_package}")
                    sure = input("Do you want to add the package to the outshipment ? [y/n] ")
                    if sure == "y" :
                        new_package = package_database[id_package] #
                        new_package.status = "on hold for outshipment" #
                        outshipment_packages.set_of_packages.add(new_package) #

                        ...
                    else :
                        os.system('clear') # what does it do ?
            receiver = input("Who is the receiver of the shipment ? ")
            expected_dispatch_date = date.fromisoformat(input("Dispatch date (YYYY-MM-DD)"))
            dispatch_date = None
            expected_delivery_date = date.fromisoformat(input("Expected delivery date (YYYY-MM-DD)"))
            delivery_date = None
            status = "on hold"
            new_outshipment = OutBoundShipment(outshipment_packages, receiver,status, expected_dispatch_date ,dispatch_date, expected_delivery_date, delivery_date) #
            #Why not create a set of shipment like with the set of packages ? To have a data base with the shipment
            id_shipment = new_outshipment.id #
            for package in outshipment_packages.set_of_packages : #
               package.shipment_id = id_shipment #

            if answer == "u" :
                answer2 = input("Do you want to declare the actual exist of the outshipment [e] or to declare its actual arrival ? [a] ")
                if answer2 =="e":
                    print("Your outshipment is on its way.")
                    id_outshipment = input("What outshipment do you want to look ?")
                    outshipment = set_of_shipments[id_outshipment] #
                    dispatch_date = date.fromisoformat(input("What is the dispatch date ? YYYY-MM-DD "))
                    outshipment.status = "sent" ""
                    outshipment.expected_arrival_date = dispatch_date #
                    for package in outshipment.set_of_packages : #
                       package.status = "sent" #

                elif answer2 =="a":
                    print("Your outshipment is arrived to the receiver.")
                    id_outshipment = input("What outshipment do you want to look ?")
                    outshipment = set_of_shipments[id_outshipment] #
                    arrival_date = date.fromisoformat(input("What is the arrival date ? YYYY-MM-DD "))
                    outshipment.status = "delivered" #
                    outshipment.expected_arrival_date = dispatch_date #
                    for package in outshipment.packages : #
                       package.status = "delivered" #

            else :
                print("This option is not known...")
                os.system('clear') # not sure
    

    elif action == "quit" :
        #save the data in a text file
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



