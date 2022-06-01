from datetime import datetime

from models import SetOfPackages, Package, Dimensions, InBoundShipment, OutBoundShipment
from inputoutput import display_set_of_packages, display_set_of_shipments, display_shipment
import pickle_data as database

from user_questions import *

def add_one_package() :
    package_informations = package_information_prompt()
    new_package = Package(package_informations[0], 
    package_informations[1], 
    package_informations[2], 
    package_informations[3],
    package_informations[4])
    if confirm_package(new_package.description, 
    new_package.dimensions,new_package.weight, new_package.status, new_package.package_type) :
        database.set_of_packages.add(new_package)
        save_id_package(new_package.id)
    print("\n")

def add_packages_to_database(database) :
    if choose_enter_one_by_one() :
        for i in range(number_packages()) :
            add_one_package()
    else :
        # we have to separate the register of the informations about the package
        # and the creation of the nb same packages 
        for i in range(number_references()) :
            packages_informations = package_information_prompt()
            nb_packages = number_packages()
            packages_id_per_reference = []

            if confirm_package_reference(packages_informations[0], 
                packages_informations[1], 
                packages_informations[2], 
                packages_informations[3], 
                packages_informations[4], nb_packages) :
                
                for j in range(number_packages()) :
                    new_package = Package(packages_informations[0], 
                    packages_informations[1], 
                    packages_informations[2], 
                    packages_informations[3],
                    packages_informations[4])
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

def register_packages_inshipment(inshipment):
    shipment_packages = SetOfPackages() 

    if choose_enter_one_by_one() :

        for j in range(number_packages()):
            package_informations = package_information_prompt()
            new_package = Package(package_informations[0], 
            package_informations[1], 
            package_informations[2], 
            package_informations[3],
            package_informations[4])

            if confirm_package(new_package.description, 
            new_package.dimensions,new_package.weight, new_package.status, new_package.package_type) :
                database.set_of_packages.add(new_package)
                shipment_packages.add(new_package) 
                save_id_package(new_package.id)
            print("\n")

    else :
        # we have to separate the register of the informations about the package
        # and the creation of the nb same packages 
        for i in range(number_references()) :
            packages_informations = package_information_prompt()
            nb_packages = number_packages()
            packages_id_per_reference = []

            if confirm_package_reference(packages_informations[0], 
                packages_informations[1], 
                packages_informations[2], 
                packages_informations[3], 
                packages_informations[4], nb_packages) :
                
                for j in range(number_packages()) :
                    new_package = Package(packages_informations[0], 
                    packages_informations[1], 
                    packages_informations[2], 
                    packages_informations[3],
                    packages_informations[4])
                    database.set_of_packages.add(new_package)
                    shipment_packages.add(new_package)
                    packages_id_per_reference.append(new_package.id)

                save_id_list_packages(packages_id_per_reference)
    inshipment.set_of_packages = shipment_packages
        
def declare_inshipment(database) :
    inshipment_information = inshipment_information_prompt()
    inshipment = InBoundShipment(inshipment_information[0], inshipment_information[1], 
    inshipment_information[2], 
    inshipment_information[3],
    inshipment_information[4])
    register_packages_inshipment(inshipment)
    database.set_of_shipments.add(inshipment)
    save_id_shipment(inshipment.id)


def update_inshipment(database) :
    id_inshipment = shipment_id_prompt()
    inshipment = database.set_of_shipments[id_inshipment]
    arrival_date = datetime_prompt("Arrival date ")
    inshipment.status = InBoundShipment.statuses[0] 
    inshipment.arrival_date = arrival_date 
    inshipment_packages = inshipment.set_of_packages
    for package in inshipment_packages : 
        package.status = Package.statuses[0]

def del_shipments(database) :
    for i in range(number_packages()):
        identity = shipment_id_prompt(database)
        if confirm_del_objects() :
            database.set_of_shipments.remove(identity)
        print("\n")

def register_packages_outshipment(outshipment) :
    shipment_packages = SetOfPackages() 
    for j in range(number_packages()):
        identity = package_id_prompt()
        if confirm_pick_package(identity):
            package_picked = database.set_of_packages[identity]
            shipment_packages.add(package_picked)
            click.echo("Package picked")
        else:
            click.echo("Aborted")
    outshipment.set_of_packages = shipment_packages

def declare_outshipment(database) :
    outshipment_information = outshipment_information_prompt()
    outshipment = OutBoundShipment(outshipment_information[0], outshipment_information[1], 
    outshipment_information[2], 
    outshipment_information[3],
    outshipment_information[4],
    outshipment_information[5])
    register_packages_outshipment(outshipment)
    database.set_of_shipments.add(outshipment)
    save_id_shipment(outshipment.id)

def actual_exit_outboundshipment(database) :
    id_outshipment = shipment_id_prompt()
    outshipment = database.set_of_shipments[id_outshipment]
    outshipment.status = OutBoundShipment.statuses[0]
    outshipment_packages = outshipment.set_of_packages
    for package in outshipment_packages :
        package.status = Package.statuses[2]
    
def delivered_outboundshipment(database) :
    id_outshipment = shipment_id_prompt()
    outshipment = database.set_of_shipments[id_outshipment]
    arrival_date = datetime_prompt("Delivered date ")
    outshipment.expected_arrival_date = arrival_date
    outshipment.status = OutBoundShipment.statuses[2]
    outshipment_packages = outshipment.set_of_packages
    for package in outshipment_packages :
        package.status = Package.statuses[3]