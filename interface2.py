import os

# créer la variable globale
in_out = True
print("Welcome ! \n")
print("This plateform allows you to manage your packages within many actions")
print("If you want to quit, input -quit- \n")


while (in_out) :
    print("\n Actions : quit / add / delete / changestatus / view / trip / status")
    action = input("Which action do you want to use ? ")

    if action == "add" :
        # tester si il met bien des chiffres pour les dimensions
        length = float(input("length : "))
        width = float(input("width : "))
        height = float(input("height : "))
        status = input("status : ")
        package_type = input("package_type : ")
        print(f"You entered the package : {length}, {width}, {height}, {status}, {package_type}")
        sure = input("Do you want to add the package ? [y/n] ")
        if sure == "y" :
            ...
            #add_package(lengh, width, height, status, package_type, dic?)
        else :
            os.system('clear')
        

    elif action == "delete" :
        identity = int(input("package id : "))
        answer = input("Are you sure to delete the data ? [y/n]")
        if answer == "y" :
            ...
            #delete_package(identity)
        else :
            os.system('clear')

    elif action == "changestatus" :
        identity = int(input("package id : "))
        newstatus = input("Which status do you want to apply ? ")
        print(f"\n You want to change the status of {identity} : {newstatus}")
        answer = input("Do you want to add the package ? [y/n] ")
        if answer == "y" :
            ...
            #change_package_status(identity, new_status, dic?)
        else :
            os.system('clear')
    
    elif action == "view" :
        print("view of the data base")
    
    elif action == "trip" :
        id_trip = int(input("Which trip do you want to look ? "))
        #add a method to see the packages of the trip
        print("trip")
    
    elif action == "status" :
        #view of the packages with the status given
        # we have to define the status we can give to a package
        print("status")
    
    elif action == "quit" :
        #save the data in a text file
        in_out = False
    
    else :
        print("The action doesn't exit yet")