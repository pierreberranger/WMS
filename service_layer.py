from datetime import datetime

from models import SetOfPackages, Package, Dimensions, InBoundShipment, OutBoundShipment
from inputoutput import display_set_of_packages, display_set_of_shipments, display_shipment
import pickle_data as database

from user_questions import *

def add_packages_to_database(database) :
    if enter_packages_one_by_one() :
        for i in range(number_packages()) :
            package_informations = package_information_prompt()
            new_package = Package(package_informations[0], 
            package_informations[1], 
            package_informations[2], 
            package_informations[3])
            if confirm_package(new_package.description, 
            new_package.dimensions,new_package.status, new_package.package_type) :
                database.set_of_packages.add(new_package)
                save_id_package(new_package.id)
            print("\n")
    else :
        for i in range(number_references()) :
            packages_informations = package_information_prompt()
            nb_packages = number_packages()
            packages_id_per_reference = []

            if confirm_package_reference(packages_informations[0], 
                packages_informations[1], 
                packages_informations[2], 
                packages_informations[3], nb_packages) :
                
                for j in range(number_packages()) :
                    new_package = Package(packages_informations[0], 
                    packages_informations[1], 
                    packages_informations[2], 
                    packages_informations[3])
                    database.set_of_packages.add(new_package)
                    packages_id_per_reference.append(new_package.id)

                save_id_list_packages(packages_id_per_reference)
            
            


def del_packages_from_database(database):
    for i in range(number_packages()):
        identity = package_id_prompt(database)
        if confirm_del_objects(identity) :
            database.set_of_packages.remove(identity)
        print("\n")

def change_status_package(database) :
    package_id = package_id_prompt(database)
    new_status = new_package_status()
    if confirm_change_status(package_id, new_status) :
        database.set_of_packages[package_id].status = new_status
    print("\n")
