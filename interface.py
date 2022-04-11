

import argparse 
import csv

parser = argparse.ArgumentParser()

parser.add_argument("-information",
                    help="write the optional argument to indiquate the action you want and add the appropriate input")

parser.add_argument("-add", 
                    help="input : longueur,largeur,hauteur,statut,type / to add a new package in the data base")

parser.add_argument("-delete", 
                    help="input : id / to delete a package in the data base")

parser.add_argument("-status", 
                    help = "input : id,status / to change the status of a package")

parser.add_argument("-data", 
                    help="no input / to print the current data ordered by id")

args = parser.parse_args()

if args.add :
    package_informations = args.add.split(",")
    if len(package_informations) != 5: #MAGNIFIQUE un superbe cas d'usage pour le pattern matching de python 3.10 :) 
        print("You didn't give the right arguments look at the documentation with -h")
    lengh = package_informations[0]
    width = package_informations[1]
    height = package_informations[2]
    status = package_informations[3]
    package_type = package_informations[4]
    #add_package(lengh, width, height, status, package_type, dic?)
    print(lengh, width, height, status, package_type)

elif args.delete :
    identity = args.delete
    answer = input("Are you sure to delete the data ? [y/N]")
    if answer == "y" :
        #delete_package(identity)
        ...
    else :
        print("Don't worry, the delete has been canceled.")
    print(args.delete)

elif args.status :
    package_new_informations = args.status.split(",")
    identity = package_new_informations[0]
    new_status = package_new_informations[1]
    #change_package_status(identity, new_status, dic?)
    print(args.status)

elif args.data :
    print("base de données")
