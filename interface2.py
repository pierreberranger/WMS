from importlib.resources import Package
import os
from datetime import date

""" Attention du code est écrit en commentaire car nous n'avons merge les fichiers et les fonctions sont donc encore indisponibles"""

# créer la variable globale
# PACKAGE_DATABASE = txt_to_shipment()

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
        #dimensions = Dimensions(length, width, height)
        status = input("status : ")
        package_type = input("package_type : ")
        
        print(f"You entered the package : {name}, {length}, {width}, {height}, {status}, {package_type}")
        sure = input("Do you want to add the package ? [y/n] ")
        
        if sure == "y" :
            #new_package = Package(name, dimensions, status, package_type)
            #PACKAGE_DATABASE.add(new_package)
            ...
        else :
            os.system('clear')
        

    elif action == "delete_package" :
        identity = int(input("package id : "))
        answer = input("Are you sure to delete the data ? [y/n]")
        if answer == "y" :
            ...
            #delete_package(identity)
        else :
            os.system('clear')

    elif action == "changestatus_package" :
        identity = int(input("package id : "))
        newstatus = input("Which status do you want to apply ? ")
        print(f"\n You want to change the status of {identity} : {newstatus}")
        answer = input("Do you want to change the status of the package ? [y/n] ")
        if answer == "y" :
            ...
            #package = PACKAGE_DATABASE.get(identity) (à revoir pour avoir la bonne méthode codée par les autres)
            #package.status = newstatus
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
            #inshipment_packages = Set_of_packages()
            for i in range(products_number) :
                quantity = input("The number")
                for j in range(quantity) :
                    # Features
                    name = input("Description of the package : ")
                    length = float(input("length : "))
                    width = float(input("width : "))
                    height = float(input("height : "))
                    #dimensions = Dimensions(length, width, height)
                    status = input("status : ")
                    package_type = input("package_type : ")
                    id_inshipment = None
                    id_outshipment = None
                    print(f"You entered the package : {name}, {length}, {width}, {height}, {status}, {package_type}, {id_inshipment}, {id_outshipment}")
                    sure = input("Do you want to add the package ? [y/n] ")
                    if sure == "y" :
                        #new_package = Package(name, dimensions, status, package_type, Nan, Nan)
                        #PACKAGE_DATABASE.add(new_package)
                        #inshipment_packages.add(new_package)
                        ...
                    else :
                        os.system('clear') # what does it do ?
            sender = input("Who is the sender of the shipment ? ")
            dispatch_date = date.fromisoformat(input("Dispatch date (YYYY-MM-DD)"))
            expected_delivery_date = date.fromisoformat(input("Expected delivery date (YYYY-MM-DD)"))
            status = "Pending"
            #new_inshipment = Inshipment(inshipment_packages, sender, dispatch_date, expected_delivery_date, status, delivery_date) 
            #Why not create a set of shipment like with the set of packages ? To have a data base with the shipment
            #id_shipment = new_inshipment.id
            # for packages in inshipment_packages :
            #   packages.id_inshipment = id_shipment
            if answer == "u" :
                print("Your inshipment is arrived.")
                id_inshipment = input("What inshipment do you want to look ?")
                #inshipment = set_of_shipments.get(id_inshipment)
                recieved_date = date.fromisoformat(input("What is the date ? YYYY-MM-DD "))
                #inshipment.status = "warehouse"
                #inshipment.recieved_date = recieved_date
                #for package in inshipment.packages :
                #   package.status = "warehouse"

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