from datetime import datetime
import os

from models import SetOfPackages, Package, Dimensions, InBoundShipment, Shipment, OutBoundShipment
from inputoutput import set_of_packages_to_txt, txt_to_set_of_packages, display_packages

import click

""" import numpy as np """

""" Attention du code est écrit en commentaire car nous n'avons merge les fichiers et les fonctions sont donc encore indisponibles"""

# créer la variable globale
package_database = txt_to_set_of_packages() # attention : préciser le fichier dans lequel la datebase est gardée en memoire
# shipment_database = txt_to_set_of_shipments()
# set_of_shipments = set() , a suppirmer car du coup on ne peut pas récupérer les shipment par les id ?

statuses = click.Choice(Package.statuses, case_sensitive=False)
types = click.Choice(Package.types, case_sensitive=False)

def package_id_prompt():
    return int(click.prompt("package id ",type=click.Choice(list((str(p.id) for p in package_database))), show_choices=False))

def interactive():
    in_out = True
    print("Welcome ! \n")
    print("This plateform allows you to manage your packages within many actions")
    print("If you want to quit, input -quit- \n")


    while (in_out) :
        print("\n Actions : quit / package / inBoundShipment / outBoundShipment / view")
        # add_package / delete_package / changestatus_package 
        action = input("On what element do you want to focus on ? ")

        if action ==  "package":
            action2 = click.prompt("More precisely : add package, delete package, or change package status", default='add', type=click.Choice(("add","del","sta")))
            if action2 == "add" :
                # Feature
                name = click.prompt("Description of the package")
                length = click.prompt("Length",type=float)
                width = click.prompt("Width",type=float)
                height = click.prompt("Height",type=float)
                dimensions = Dimensions(length, width, height)
                status = click.prompt("status", default=Package.statuses[0], type=statuses)
                package_type = click.prompt("Package Type", default=Package.types[0], type=types)
                
                click.echo(f"You entered the package : {name}, {length}, {width}, {height}, {status}, {package_type}")
                sure = click.confirm("Do you want to add the package ?",default=True)
                
                if sure:
                    new_package = Package(dimensions, status, package_type) 
                    package_database.add(new_package)
                else :
                    os.system('clear')
                

            elif action2 == "del" :
                identity =  package_id_prompt()
                answer = click.confirm("Are you sure to delete the data ?", default=False)
                if answer:
                    package_database.remove(identity) 
                else :
                    os.system('clear')

            elif action2 == "sta" :
                identity = package_id_prompt()
                newstatus = click.prompt("New status", default=Package.statuses[2], type=statuses)
                answer = click.confirm(f"You want to change the status of package {identity} to {newstatus}")
                if answer:
                    package_database[identity].status = newstatus
                else :
                    os.system('clear')
        
        elif action == "view" :
            display_packages(package_database)

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
                            package_database.add(new_package)
                            inshipment_packages.add(new_package)
                        else :
                            os.system('clear') # what does it do ?
                new_inshipment = InBoundShipment(arrival_date, status, id, set_of_packages, sender, adressee)
                #shipment_database.add(new_inshipment)
                #Why not create a set of shipment like with the set of packages ? To have a data base with the shipment
                id_shipment = new_inshipment.id 
                for package in inshipment_packages:
                    package.shipment_id = id_shipment

                if answer == "u" :
                    print("Your inshipment is arrived.")
                    id_inshipment = input("What inshipment do you want to look ?")
                    #inshipment = set_of_shipments[id_inshipment] # à créer !
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
                            new_package = package_database[id_package]
                            new_package.status = "exit"
                            outshipment_packages.add(new_package) 
                        else :
                            os.system('clear') # what does it do ?
                new_outshipment = OutBoundShipment(outshipment_packages, receiver,status, expected_dispatch_date ,dispatch_date, expected_delivery_date, delivery_date) #
                #Why not create a set of shipment like with the set of packages ? To have a data base with the shipment
                #shipment_database.add(new_outshipment)
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
                        #outshipment = set_of_shipments[id_outshipment]
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
            set_of_packages_to_txt(package_database)
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

if __name__ == "__main__":
    interactive()